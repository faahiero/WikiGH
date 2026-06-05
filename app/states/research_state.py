import reflex as rx
import logging
import re
import html as _html
import asyncio
import requests
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import TypedDict


WIKI_API = "https://pt.wikipedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
USER_AGENT = (
    "WikipediaGeoHist/1.0 (https://reflex.dev; educational research app)"
)
HEADERS = {"User-Agent": USER_AGENT}

DB_PATH = Path("geohist.db")


def _format_br_date(raw: str) -> str:
    if not raw:
        return ""
    # Pass-through markers
    if raw in ("—", "Vivo(a)"):
        return raw
    s = raw.strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2}:\d{2})$", s)
    if m:
        y, mo, d, t = m.groups()
        return f"{d}/{mo}/{y} {t}"
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if m:
        y, mo, d = m.groups()
        return f"{d}/{mo}/{y}"
    m = re.match(r"^(\d{4})-(\d{2})$", s)
    if m:
        y, mo = m.groups()
        return f"{mo}/{y}"
    m = re.match(r"^(\d{4})$", s)
    if m:
        return s
    # Negative year (BC)
    m = re.match(r"^-(\d+)-(\d{2})-(\d{2})$", s)
    if m:
        y, mo, d = m.groups()
        return f"{d}/{mo}/{y} a.C."
    m = re.match(r"^-(\d+)$", s)
    if m:
        return f"{m.group(1)} a.C."
    return s


def _short_qid(qid: str) -> str:
    if not qid:
        return ""
    if len(qid) <= 10:
        return qid
    return qid[-8:]


def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id TEXT PRIMARY KEY,
                name TEXT,
                nationality TEXT,
                birth_date TEXT,
                death_date TEXT,
                birth_place TEXT,
                death_place TEXT,
                birth_lat REAL,
                birth_lng REAL,
                death_lat REAL,
                death_lng REAL,
                article_url TEXT,
                summary TEXT,
                searched_at TEXT,
                completeness INTEGER,
                image_url TEXT DEFAULT '',
                article_title TEXT DEFAULT '',
                is_living INTEGER DEFAULT 0,
                occupation TEXT DEFAULT '',
                description TEXT DEFAULT ''
            )
        """)
        # Safe migration: add new columns if missing on older DBs
        cursor.execute("PRAGMA table_info(people)")
        cols = [row[1] for row in cursor.fetchall()]
        if "image_url" not in cols:
            try:
                cursor.execute(
                    "ALTER TABLE people ADD COLUMN image_url TEXT DEFAULT ''"
                )
            except Exception as e:
                logging.exception(f"Erro ao migrar coluna image_url: {e}")
        if "article_title" not in cols:
            try:
                cursor.execute(
                    "ALTER TABLE people ADD COLUMN article_title TEXT DEFAULT ''"
                )
            except Exception as e:
                logging.exception(f"Erro ao migrar coluna article_title: {e}")
        if "is_living" not in cols:
            try:
                cursor.execute(
                    "ALTER TABLE people ADD COLUMN is_living INTEGER DEFAULT 0"
                )
            except Exception as e:
                logging.exception(f"Erro ao migrar coluna is_living: {e}")
        if "occupation" not in cols:
            try:
                cursor.execute(
                    "ALTER TABLE people ADD COLUMN occupation TEXT DEFAULT ''"
                )
            except Exception as e:
                logging.exception(f"Erro ao migrar coluna occupation: {e}")
        if "description" not in cols:
            try:
                cursor.execute(
                    "ALTER TABLE people ADD COLUMN description TEXT DEFAULT ''"
                )
            except Exception as e:
                logging.exception(f"Erro ao migrar coluna description: {e}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT,
                title TEXT,
                timestamp TEXT,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        logging.exception(f"Erro ao inicializar banco de dados SQLite: {e}")


def save_person_db(p: dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO people (
                id, name, nationality, birth_date, death_date, birth_place, death_place,
                birth_lat, birth_lng, death_lat, death_lng, article_url, summary, searched_at, completeness, image_url, article_title, is_living, occupation, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                p["id"],
                p["name"],
                p["nationality"],
                p["birth_date"],
                p["death_date"],
                p["birth_place"],
                p["death_place"],
                p["birth_lat"],
                p["birth_lng"],
                p["death_lat"],
                p["death_lng"],
                p["article_url"],
                p["summary"],
                p["searched_at"],
                p["completeness"],
                p.get("image_url", ""),
                p.get("article_title", ""),
                1 if p.get("is_living", False) else 0,
                p.get("occupation", ""),
                p.get("description", ""),
            ),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logging.exception(f"Erro ao salvar pessoa no SQLite: {e}")


def delete_person_db(pid: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM people WHERE id = ?", (pid,))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.exception(f"Erro ao excluir pessoa do SQLite: {e}")


def load_people_db() -> list:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people ORDER BY searched_at DESC")
        rows = cursor.fetchall()
        out = []
        col_names = rows[0].keys() if rows else []
        for r in rows:
            image_url = ""
            if "image_url" in col_names:
                image_url = r["image_url"] or ""
            article_title = ""
            if "article_title" in col_names:
                article_title = r["article_title"] or ""
            is_living = False
            if "is_living" in col_names:
                is_living = bool(r["is_living"])
            occupation = ""
            if "occupation" in col_names:
                occupation = r["occupation"] or ""
            description = ""
            if "description" in col_names:
                description = r["description"] or ""
            out.append(
                {
                    "id": r["id"],
                    "name": r["name"],
                    "nationality": r["nationality"],
                    "birth_date": r["birth_date"],
                    "death_date": r["death_date"],
                    "birth_place": r["birth_place"],
                    "death_place": r["death_place"],
                    "birth_lat": float(r["birth_lat"]),
                    "birth_lng": float(r["birth_lng"]),
                    "death_lat": float(r["death_lat"]),
                    "death_lng": float(r["death_lng"]),
                    "article_url": r["article_url"],
                    "summary": r["summary"],
                    "searched_at": r["searched_at"],
                    "completeness": int(r["completeness"]),
                    "image_url": image_url,
                    "article_title": article_title,
                    "is_living": is_living,
                    "occupation": occupation,
                    "description": description,
                }
            )
        conn.close()
        return out
    except Exception as e:
        logging.exception(f"Erro ao carregar pessoas do SQLite: {e}")
        return []


def save_history_db(h: dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO history (term, title, timestamp, status)
            VALUES (?, ?, ?, ?)
        """,
            (h["term"], h["title"], h["timestamp"], h["status"]),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logging.exception(f"Erro ao salvar historico no SQLite: {e}")


def clear_history_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history")
        conn.commit()
        conn.close()
    except Exception as e:
        logging.exception(f"Erro ao limpar historico no SQLite: {e}")


def load_history_db() -> list:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT term, title, timestamp, status FROM history ORDER BY id DESC LIMIT 50"
        )
        rows = cursor.fetchall()
        out = []
        for r in rows:
            out.append(
                {
                    "term": r["term"],
                    "title": r["title"],
                    "timestamp": r["timestamp"],
                    "status": r["status"],
                }
            )
        conn.close()
        return out
    except Exception as e:
        logging.exception(f"Erro ao carregar historico do SQLite: {e}")
        return []


class SearchResult(TypedDict):
    title: str
    snippet: str
    pageid: int


class PersonRecord(TypedDict):
    id: str
    name: str
    nationality: str
    birth_date: str
    death_date: str
    birth_place: str
    death_place: str
    birth_lat: float
    birth_lng: float
    death_lat: float
    death_lng: float
    article_url: str
    summary: str
    searched_at: str
    completeness: int
    image_url: str
    article_title: str
    is_living: bool
    occupation: str
    description: str


class HistoryEntry(TypedDict):
    term: str
    title: str
    timestamp: str
    status: str


def _strip_html(text: str) -> str:
    if not text:
        return ""
    original = text
    text = _html.unescape(text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Remove wiki templates and links remnants
    text = re.sub(r"\{\{[^{}]*\}\}", " ", text)
    text = re.sub(r"\[\[[^\[\]]*\]\]", " ", text)
    # Remove citation markers like [1], [2]
    text = re.sub(r"\[\d+\]", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Trim leading/trailing junk punctuation/quotes
    text = re.sub(r"^[\s,;:.\-—–·•\)\]\}\"'`]+", "", text)
    text = re.sub(r"[\s,;:\-—–·•\(\[\{\"'`]+$", "", text)
    if not text:
        return ""
    leading_stopwords = (
        "da ",
        "de ",
        "do ",
        "dos ",
        "das ",
        "e ",
        "em ",
        "no ",
        "na ",
        "nos ",
        "nas ",
        "ao ",
        "aos ",
        "à ",
        "às ",
        "por ",
        "para ",
        "com ",
        "que ",
        "se ",
        "um ",
        "uma ",
        "uns ",
        "umas ",
    )
    starts_fragment = text[0].islower() or text.lower().startswith(
        leading_stopwords
    )
    if starts_fragment:
        # Strategy 1: advance to a sentence boundary followed by uppercase/digit
        m = re.search(r"[.!?…]\s+(?:[-–—]\s*)?([A-ZÁÉÍÓÚÂÊÔÃÕÇÀ0-9])", text)
        if m:
            text = text[m.start(1) :].strip()
        else:
            # Strategy 2: drop leading fragment through first suitable separator
            candidates = list(re.finditer(r"(?:[.!?…;:]|\s[-–—]\s|,\s)", text))
            for sep in candidates[:6]:
                tail = text[sep.end() :].strip()
                tail = re.sub(r"^[\s,;:.\-—–·•\)\]\}\"'`]+", "", tail)
                if tail and (tail[0].isupper() or tail[0].isdigit()):
                    text = tail
                    break
    # Normalize whitespace and punctuation spacing
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([.!?…]){2,}", r"\1", text)
    # Trim again any leading junk after manipulation
    text = re.sub(r"^[\s,;:.\-—–·•\)\]\}\"'`]+", "", text)
    text = re.sub(r"[\s,;:\-—–·•\(\[\{\"'`]+$", "", text)
    if not text:
        # Last resort: fall back to raw cleaned version of original
        fallback = re.sub(r"<[^>]+>", " ", _html.unescape(original))
        fallback = re.sub(r"\s+", " ", fallback).strip()
        fallback = re.sub(r"^[\s,;:.\-—–·•\)\]\}\"'`]+", "", fallback)
        fallback = re.sub(r"[\s,;:\-—–·•\(\[\{\"'`]+$", "", fallback)
        text = fallback
    if not text:
        return ""
    # Prefer first coherent sentence
    sentences = re.split(r"(?<=[.!?…])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇÀ0-9])", text)
    first = sentences[0].strip() if sentences else text
    starts_bad = first and (
        first[0].islower() or first.lower().startswith(leading_stopwords)
    )
    if first and 20 <= len(first) <= 280 and not starts_bad:
        if first[-1] not in ".!?…":
            first = first + "."
        return first
    # Fall back to a coherent trimmed excerpt
    excerpt = text
    if len(excerpt) > 240:
        cut = excerpt[:240].rsplit(" ", 1)[0]
        cut = cut.rstrip(",;:-—–·• ")
        excerpt = cut + "…"
    else:
        excerpt = excerpt.rstrip(",;:-—–·• ")
        if excerpt and excerpt[-1] not in ".!?…":
            excerpt = excerpt + "…"
    return excerpt


def _format_preview_extract(raw_text: str, max_chars: int = 520) -> str:
    if not raw_text:
        return ""
    text = _html.unescape(raw_text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\{\{[^{}]*\}\}", " ", text)
    text = re.sub(r"\[\[[^\[\]]*\]\]", " ", text)
    text = re.sub(r"\[\d+\]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[\s,;:.\-—–·•\)\]\}\"'`]+", "", text)
    text = re.sub(r"[\s,;:\-—–·•\(\[\{\"'`]+$", "", text)
    if not text:
        return ""
    leading_stopwords = (
        "da ",
        "de ",
        "do ",
        "dos ",
        "das ",
        "e ",
        "em ",
        "no ",
        "na ",
        "nos ",
        "nas ",
        "ao ",
        "aos ",
        "à ",
        "às ",
        "por ",
        "para ",
        "com ",
        "que ",
        "se ",
        "um ",
        "uma ",
    )
    if text[0].islower() or text.lower().startswith(leading_stopwords):
        m = re.search(r"[.!?…]\s+(?:[-–—]\s*)?([A-ZÁÉÍÓÚÂÊÔÃÕÇÀ0-9])", text)
        if m:
            text = text[m.start(1) :].strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([.!?…]){2,}", r"\1", text)
    if len(text) <= max_chars:
        if text and text[-1] not in ".!?…":
            text = text + "."
        return text
    truncated = text[:max_chars]
    boundaries = [m.end() for m in re.finditer(r"[.!?…](?:\s|$)", truncated)]
    if boundaries:
        last = boundaries[-1]
        result = truncated[:last].rstrip()
        if result and result[-1] not in ".!?…":
            result = result + "."
        if len(result) >= 100:
            return result
    cut = truncated.rsplit(" ", 1)[0].rstrip(",;:-—–·• ")
    if cut and cut[-1] not in ".!?…":
        cut = cut + "…"
    return cut


def _parse_wd_time(time_str: str) -> str:
    if not time_str:
        return ""
    try:
        clean = time_str.lstrip("+-").split("T")[0]
        return clean
    except Exception:
        logging.exception("Unexpected error")
        return time_str


def _api_get(url: str, params: dict, timeout: int = 10) -> dict | None:
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.exception(f"API request failed: {e}")
        return None


def _sort_by_index_helper(p: dict) -> int:
    return int(p.get("index", 999))


def _wiki_search(term: str, limit: int = 8) -> list[dict] | None:
    data = _api_get(
        WIKI_API,
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": term,
            "gsrnamespace": "0",
            "gsrlimit": str(limit),
            "prop": "extracts|pageprops",
            "exintro": 1,
            "explaintext": 1,
            "exchars": 320,
            "exlimit": str(limit),
            "ppprop": "wikibase_item|disambiguation",
            "format": "json",
        },
    )
    if data is None:
        return None
    pages = data.get("query", {}).get("pages", {}) or {}
    if not pages:
        return []
    items = list(pages.values())
    items.sort(key=_sort_by_index_helper)
    out = []
    for p in items:
        out.append(
            {
                "title": p.get("title", ""),
                "snippet": _strip_html(p.get("snippet", "")),
                "pageid": int(p.get("pageid", 0)),
            }
        )
    return out


def _wiki_article(title: str) -> dict | None:
    data = _api_get(
        WIKI_API,
        {
            "action": "query",
            "titles": title,
            "prop": "extracts|pageprops|info|pageimages",
            "exintro": 1,
            "explaintext": 1,
            "exchars": 1500,
            "ppprop": "wikibase_item|disambiguation",
            "inprop": "url",
            "piprop": "thumbnail|original|name",
            "pithumbsize": "400",
            "redirects": 1,
            "format": "json",
        },
    )
    if data is None:
        return None
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return {}
    return next(iter(pages.values()))


def _wd_entity(
    qid: str, props: str = "labels|descriptions|claims"
) -> dict | None:
    data = _api_get(
        WIKIDATA_API,
        {
            "action": "wbgetentities",
            "ids": qid,
            "props": props,
            "languages": "pt|en",
            "format": "json",
        },
    )
    if data is None:
        return None
    return data.get("entities", {}).get(qid)


def _wd_entities(qids: list[str]) -> dict[str, dict]:
    if not qids:
        return {}
    out: dict[str, dict] = {}
    for i in range(0, len(qids), 40):
        chunk = qids[i : i + 40]
        data = _api_get(
            WIKIDATA_API,
            {
                "action": "wbgetentities",
                "ids": "|".join(chunk),
                "props": "labels|claims",
                "languages": "pt|en",
                "format": "json",
            },
        )
        if data is None:
            continue
        out.update(data.get("entities", {}) or {})
    return out


def _label_of(entity: dict | None) -> str:
    if not entity:
        return ""
    labels = entity.get("labels", {}) or {}
    return (
        labels.get("pt", {}).get("value")
        or labels.get("en", {}).get("value")
        or ""
    )


def _coords_of(entity: dict | None) -> tuple[float, float] | None:
    if not entity:
        return None
    claims = entity.get("claims", {}) or {}
    p625 = claims.get("P625") or []
    if not p625:
        return None
    try:
        snak = p625[0].get("mainsnak", {}) or {}
        if snak.get("snaktype") != "value":
            return None
        v = snak.get("datavalue", {}).get("value", {}) or {}
        if "latitude" not in v or "longitude" not in v:
            return None
        return float(v["latitude"]), float(v["longitude"])
    except (KeyError, TypeError, ValueError, IndexError):
        logging.exception("Unexpected error")
        return None
    except Exception as e:
        logging.exception(f"Unexpected error parsing coordinates: {e}")
        return None


def _claim_qid(claims: dict, prop: str) -> str:
    if not claims or not isinstance(claims, dict):
        return ""
    entries = claims.get(prop) or []
    if not entries:
        return ""
    try:
        snak = entries[0].get("mainsnak", {}) or {}
        if snak.get("snaktype") != "value":
            return ""
        value = snak.get("datavalue", {}).get("value", {}) or {}
        return value.get("id", "") or ""
    except (KeyError, TypeError, IndexError, AttributeError):
        logging.exception("Unexpected error")
        return ""
    except Exception as e:
        logging.exception(f"Unexpected error reading claim qid for {prop}: {e}")
        return ""


def _claim_time(claims: dict, prop: str) -> str:
    if not claims or not isinstance(claims, dict):
        return ""
    entries = claims.get(prop) or []
    if not entries:
        return ""
    try:
        snak = entries[0].get("mainsnak", {}) or {}
        if snak.get("snaktype") != "value":
            return ""
        value = snak.get("datavalue", {}).get("value", {}) or {}
        time_str = value.get("time", "") or ""
        if not time_str:
            return ""
        return _parse_wd_time(time_str)
    except (KeyError, TypeError, IndexError, AttributeError):
        logging.exception("Unexpected error")
        return ""
    except Exception as e:
        logging.exception(
            f"Unexpected error reading claim time for {prop}: {e}"
        )
        return ""


async def _fallback_coords(
    place_qid: str, ref_entities: dict
) -> tuple[float, float] | None:
    if not place_qid:
        return None
    place_entity = ref_entities.get(place_qid)
    if not place_entity:
        return None
    place_claims = place_entity.get("claims", {}) or {}
    country_qid = _claim_qid(place_claims, "P17")
    if not country_qid:
        return None
    country_entity = await asyncio.to_thread(_wd_entity, country_qid)
    return _coords_of(country_entity)


def _full_place(place_qid: str, base_label: str, ref_entities: dict) -> str:
    if not place_qid or not base_label:
        return base_label
    place_entity = ref_entities.get(place_qid)
    if not place_entity:
        return base_label
    country_qid = _claim_qid(place_entity.get("claims", {}) or {}, "P17")
    if not country_qid:
        return base_label
    country_entity = ref_entities.get(country_qid)
    country_label = _label_of(country_entity)
    if country_label and country_label.lower() not in base_label.lower():
        return f"{base_label}, {country_label}"
    return base_label


class MapPoint(TypedDict):
    id: str
    qid: str
    name: str
    place: str
    date: str
    date_br: str
    lat: float
    lng: float
    kind: str
    image_url: str
    context_label: str
    is_homonym: bool
    short_id: str
    display_name: str
    nationality: str
    article_url: str
    birth_date_br: str
    death_date_br: str
    birth_place: str
    death_place: str
    is_living: bool
    occupation: str
    summary: str


class EnrichedPerson(TypedDict):
    id: str
    name: str
    nationality: str
    birth_date: str
    death_date: str
    birth_date_br: str
    death_date_br: str
    birth_place: str
    death_place: str
    birth_lat: float
    birth_lng: float
    death_lat: float
    death_lng: float
    article_url: str
    summary: str
    searched_at: str
    searched_at_br: str
    completeness: int
    image_url: str
    article_title: str
    is_living: bool
    context_label: str
    is_homonym: bool
    short_id: str
    display_name: str


class MapConnection(TypedDict):
    id: str
    name: str
    birth_lat: float
    birth_lng: float
    death_lat: float
    death_lng: float
    is_selected: bool


class TimelineEvent(TypedDict):
    id: str
    person_id: str
    qid: str
    name: str
    year: int
    date: str
    date_br: str
    place: str
    kind: str
    context_label: str
    is_homonym: bool
    short_id: str
    display_name: str


class EnrichedHistoryEntry(TypedDict):
    term: str
    title: str
    timestamp: str
    timestamp_br: str
    status: str
    short_id: str
    qid: str
    context_label: str


class DistRow(TypedDict):
    label: str
    count: int


SUGGESTION_POOL: list[str] = [
    "Fernando Pessoa",
    "Machado de Assis",
    "Marie Curie",
    "Carlos Drummond de Andrade",
    "Clarice Lispector",
    "Albert Einstein",
    "Cecília Meireles",
    "Jorge Amado",
    "Graciliano Ramos",
    "Guimarães Rosa",
    "Nelson Mandela",
    "Frida Kahlo",
    "Leonardo da Vinci",
    "Galileu Galilei",
    "Isaac Newton",
    "Charles Darwin",
    "Sigmund Freud",
    "Tom Jobim",
    "Heitor Villa-Lobos",
    "Oscar Niemeyer",
    "Tarsila do Amaral",
    "Cândido Portinari",
    "Lima Barreto",
    "Mário de Andrade",
    "Olavo Bilac",
    "Castro Alves",
    "José de Alencar",
    "Eça de Queirós",
    "Camilo Castelo Branco",
    "Luís de Camões",
    "Sophia de Mello Breyner",
    "José Saramago",
    "Florbela Espanca",
    "Almeida Garrett",
    "Antero de Quental",
    "Pablo Picasso",
    "Vincent van Gogh",
    "Salvador Dalí",
    "Frédéric Chopin",
    "Ludwig van Beethoven",
    "Wolfgang Amadeus Mozart",
    "Johann Sebastian Bach",
    "Mahatma Gandhi",
    "Martin Luther King Jr.",
    "Winston Churchill",
    "Napoleão Bonaparte",
    "Simone de Beauvoir",
    "Virginia Woolf",
    "Jane Austen",
    "Emily Dickinson",
    "Gabriel García Márquez",
    "Pablo Neruda",
    "Jorge Luis Borges",
    "Octavio Paz",
    "Princesa Isabel",
    "Dom Pedro II",
    "Tiradentes",
    "Zumbi dos Palmares",
    "Anita Garibaldi",
    "Chiquinha Gonzaga",
    "Santos Dumont",
    "Juscelino Kubitschek",
    "Getúlio Vargas",
]


SUGGESTION_CATEGORIES: list[str] = [
    "Categoria:Escritores do Brasil",
    "Categoria:Poetas do Brasil",
    "Categoria:Pintores do Brasil",
    "Categoria:Cientistas do Brasil",
    "Categoria:Políticos do Brasil",
    "Categoria:Compositores do Brasil",
    "Categoria:Atores do Brasil",
    "Categoria:Escritores de Portugal",
    "Categoria:Poetas de Portugal",
    "Categoria:Cientistas de Portugal",
    "Categoria:Físicos",
    "Categoria:Matemáticos",
    "Categoria:Filósofos",
    "Categoria:Músicos do Brasil",
    "Categoria:Cantores do Brasil",
    "Categoria:Arquitetos do Brasil",
    "Categoria:Historiadores do Brasil",
    "Categoria:Jornalistas do Brasil",
    "Categoria:Astrônomos",
    "Categoria:Inventores",
    "Categoria:Exploradores",
]


_LOWQUALITY_RE = re.compile(
    r"\b(lista|anexo|categoria|wikipédia|wikipedia|desambiguação|índice)\b",
    re.IGNORECASE,
)


def _fetch_dynamic_suggestions(target_count: int = 7) -> list[str]:
    import random

    chosen_cats = random.sample(
        SUGGESTION_CATEGORIES, k=min(5, len(SUGGESTION_CATEGORIES))
    )
    collected: list[str] = []
    seen: set[str] = set()
    for cat in chosen_cats:
        try:
            data = _api_get(
                WIKI_API,
                {
                    "action": "query",
                    "generator": "categorymembers",
                    "gcmtitle": cat,
                    "gcmnamespace": "0",
                    "gcmlimit": "20",
                    "prop": "pageprops",
                    "ppprop": "wikibase_item|disambiguation",
                    "format": "json",
                },
                timeout=8,
            )
            if not data:
                continue
            pages = list(
                (data.get("query", {}).get("pages", {}) or {}).values()
            )
            for p in pages:
                title = (p.get("title") or "").strip()
                if not title or title in seen:
                    continue
                if _LOWQUALITY_RE.search(title):
                    continue
                if ":" in title:
                    continue
                pp = p.get("pageprops", {}) or {}
                if "disambiguation" in pp:
                    continue
                if not pp.get("wikibase_item"):
                    continue
                seen.add(title)
                collected.append(title)
        except Exception as e:
            logging.exception(f"Erro ao buscar sugestões em {cat}: {e}")
            continue
    if len(collected) < target_count:
        fallback = [s for s in SUGGESTION_POOL if s not in seen]
        random.shuffle(fallback)
        collected.extend(fallback[: target_count - len(collected)])
    random.shuffle(collected)
    return collected[:target_count]


class ResearchState(rx.State):
    dark_mode: bool = False
    search_query: str = ""
    is_searching: bool = False
    landing_mode: bool = True
    dynamic_suggestions: list[str] = [
        "Fernando Pessoa",
        "Machado de Assis",
        "Marie Curie",
        "Carlos Drummond de Andrade",
        "Clarice Lispector",
        "Albert Einstein",
        "Cecília Meireles",
    ]

    @rx.event
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

    @rx.event
    def enter_app(self):
        self.landing_mode = False

    @rx.event
    def enter_landing(self):
        self.landing_mode = True

    is_loading_article: bool = False
    is_extracting: bool = False
    is_disambiguation: bool = False
    is_human: bool = False
    error_message: str = ""
    info_message: str = ""

    search_results: list[SearchResult] = []
    selected_preview: dict[str, str] = {
        "title": "",
        "extract": "",
        "url": "",
        "wikidata_id": "",
        "image_url": "",
    }
    has_preview: bool = False
    people: list[PersonRecord] = []
    history: list[HistoryEntry] = []

    active_view: str = "dashboard"
    timeline_filter: str = "all"
    selected_person_id: str = ""
    table_search: str = ""
    storage_ready: bool = False
    last_persist_action: str = ""

    @rx.event
    async def load_data(self):
        import random

        await asyncio.to_thread(init_db)
        try:
            live = await asyncio.to_thread(_fetch_dynamic_suggestions, 7)
            if live and len(live) >= 4:
                self.dynamic_suggestions = live
            else:
                self.dynamic_suggestions = random.sample(SUGGESTION_POOL, k=7)
        except Exception as e:
            logging.exception(f"Erro ao gerar sugestões dinâmicas: {e}")
            try:
                self.dynamic_suggestions = random.sample(SUGGESTION_POOL, k=7)
            except Exception as e2:
                logging.exception(f"Erro no fallback de sugestões: {e2}")
        try:
            self.people = await asyncio.to_thread(load_people_db)
            self.history = await asyncio.to_thread(load_history_db)
            self.storage_ready = True
            self.last_persist_action = "carregado"
            people_count = len(self.people)
            history_count = len(self.history)
            if people_count > 0 or history_count > 0:
                yield rx.toast(
                    title="Dados restaurados",
                    description=f"{people_count} pessoa(s) e {history_count} busca(s) carregados do armazenamento local.",
                    position="bottom-right",
                    duration=4000,
                    close_button=True,
                )
            else:
                yield rx.toast(
                    title="Armazenamento local pronto",
                    description="Nenhum registro salvo ainda. Sua primeira pesquisa confirmada será salva automaticamente.",
                    position="bottom-right",
                    duration=3500,
                    close_button=True,
                )
        except Exception as e:
            logging.exception(f"Erro ao carregar dados persistidos: {e}")
            self.storage_ready = False
            yield rx.toast(
                title="Falha ao restaurar dados",
                description="Não foi possível ler do armazenamento local. A sessão começará vazia.",
                position="bottom-right",
                duration=5000,
                close_button=True,
            )

    @rx.event
    def set_active_view(self, view: str):
        self.active_view = view

    @rx.event
    def set_timeline_filter(self, value: str):
        self.timeline_filter = value

    @rx.event
    def select_person(self, person_id: str):
        self.selected_person_id = person_id

    @rx.event
    def set_table_search(self, value: str):
        self.table_search = value

    def _build_context_label(self, person: dict) -> str:
        max_len = 42

        profession_tokens = (
            "escritor",
            "escritora",
            "poeta",
            "poetisa",
            "romancista",
            "novelista",
            "ensaísta",
            "dramaturgo",
            "cronista",
            "contista",
            "tradutor",
            "tradutora",
            "jornalista",
            "editor",
            "editora",
            "historiador",
            "historiadora",
            "filósofo",
            "filósofa",
            "filosofo",
            "filosofa",
            "sociólogo",
            "socióloga",
            "antropólogo",
            "antropóloga",
            "linguista",
            "professor",
            "professora",
            "pesquisador",
            "pesquisadora",
            "cientista",
            "físico",
            "física",
            "fisico",
            "fisica",
            "químico",
            "química",
            "quimico",
            "quimica",
            "biólogo",
            "bióloga",
            "biologo",
            "biologa",
            "matemático",
            "matemática",
            "matematico",
            "matematica",
            "astrônomo",
            "astrônoma",
            "astronomo",
            "astronoma",
            "engenheiro",
            "engenheira",
            "arquiteto",
            "arquiteta",
            "médico",
            "médica",
            "medico",
            "medica",
            "advogado",
            "advogada",
            "jurista",
            "magistrado",
            "magistrada",
            "juiz",
            "juíza",
            "promotor",
            "promotora",
            "diplomata",
            "político",
            "política",
            "politico",
            "politica",
            "presidente",
            "ministro",
            "ministra",
            "senador",
            "senadora",
            "deputado",
            "deputada",
            "governador",
            "governadora",
            "prefeito",
            "prefeita",
            "ativista",
            "militante",
            "líder",
            "lider",
            "revolucionário",
            "revolucionária",
            "rei",
            "rainha",
            "imperador",
            "imperatriz",
            "príncipe",
            "princesa",
            "monarca",
            "papa",
            "santo",
            "santa",
            "religioso",
            "religiosa",
            "padre",
            "freira",
            "bispo",
            "arcebispo",
            "teólogo",
            "teóloga",
            "militar",
            "general",
            "coronel",
            "almirante",
            "marechal",
            "soldado",
            "guerreiro",
            "guerreira",
            "explorador",
            "exploradora",
            "navegador",
            "navegadora",
            "aviador",
            "aviadora",
            "astronauta",
            "inventor",
            "inventora",
            "empresário",
            "empresária",
            "empresario",
            "empresaria",
            "economista",
            "banqueiro",
            "banqueira",
            "industrial",
            "comerciante",
            "filantropo",
            "filantropa",
            "ator",
            "atriz",
            "cineasta",
            "diretor",
            "diretora",
            "produtor",
            "produtora",
            "roteirista",
            "apresentador",
            "apresentadora",
            "humorista",
            "comediante",
            "músico",
            "música",
            "musico",
            "musica",
            "cantor",
            "cantora",
            "compositor",
            "compositora",
            "maestro",
            "instrumentista",
            "pianista",
            "violonista",
            "guitarrista",
            "baterista",
            "rapper",
            "dj",
            "pintor",
            "pintora",
            "escultor",
            "escultora",
            "fotógrafo",
            "fotógrafa",
            "fotografo",
            "fotografa",
            "ilustrador",
            "ilustradora",
            "designer",
            "estilista",
            "modelo",
            "atleta",
            "futebolista",
            "jogador",
            "jogadora",
            "tenista",
            "boxeador",
            "boxeadora",
            "lutador",
            "lutadora",
            "treinador",
            "treinadora",
            "técnico",
            "técnica",
            "tecnico",
            "tecnica",
            "piloto",
            "nadador",
            "nadadora",
            "ginasta",
            "skatista",
            "surfista",
            "programador",
            "programadora",
            "desenvolvedor",
            "desenvolvedora",
            "hacker",
            "writer",
            "poet",
            "novelist",
            "essayist",
            "playwright",
            "journalist",
            "editor",
            "translator",
            "historian",
            "philosopher",
            "sociologist",
            "anthropologist",
            "linguist",
            "professor",
            "researcher",
            "scientist",
            "physicist",
            "chemist",
            "biologist",
            "mathematician",
            "astronomer",
            "engineer",
            "architect",
            "physician",
            "doctor",
            "lawyer",
            "jurist",
            "judge",
            "diplomat",
            "politician",
            "president",
            "minister",
            "senator",
            "governor",
            "activist",
            "leader",
            "revolutionary",
            "king",
            "queen",
            "emperor",
            "empress",
            "prince",
            "princess",
            "monarch",
            "pope",
            "saint",
            "priest",
            "nun",
            "bishop",
            "theologian",
            "soldier",
            "general",
            "admiral",
            "explorer",
            "navigator",
            "aviator",
            "astronaut",
            "inventor",
            "businessman",
            "businesswoman",
            "entrepreneur",
            "economist",
            "banker",
            "actor",
            "actress",
            "filmmaker",
            "director",
            "producer",
            "screenwriter",
            "presenter",
            "comedian",
            "musician",
            "singer",
            "composer",
            "conductor",
            "pianist",
            "guitarist",
            "drummer",
            "painter",
            "sculptor",
            "photographer",
            "illustrator",
            "designer",
            "model",
            "athlete",
            "footballer",
            "player",
            "tennis",
            "boxer",
            "fighter",
            "coach",
            "pilot",
            "swimmer",
            "gymnast",
            "programmer",
            "developer",
        )

        def _normalize(s: str) -> str:
            s = re.sub(r"\s+", " ", s or "").strip()
            s = re.sub(r"\s*[/;|]\s*", ", ", s)
            s = re.sub(r"\s*,\s*", ", ", s)
            s = re.sub(r"(?:,\s*){2,}", ", ", s)
            s = s.strip(" ,.;:-—–·•")
            return s

        def _shorten(s: str) -> str:
            s = _normalize(s)
            if not s:
                return ""
            if len(s) <= max_len:
                return s
            parts = [p.strip() for p in s.split(",") if p.strip()]
            if parts:
                acc = parts[0]
                for nxt in parts[1:]:
                    candidate = f"{acc}, {nxt}"
                    if len(candidate) <= max_len:
                        acc = candidate
                    else:
                        break
                if len(acc) <= max_len:
                    return acc
            cut = s[:max_len]
            for sep in (", ", " e ", " "):
                idx = cut.rfind(sep)
                if idx >= 16:
                    return cut[:idx].rstrip(" ,.;:-—–·•")
            return cut.rstrip(" ,.;:-—–·•")

        def _looks_like_year(s: str) -> bool:
            return bool(
                re.fullmatch(r"\s*-?\d{1,4}\s*[-–—]?\s*-?\d{0,4}\s*", s or "")
            )

        def _has_profession_token(s: str) -> bool:
            if not s:
                return False
            tokens = re.findall(r"[a-záéíóúâêôãõçà]+", s.lower())
            for tok in tokens:
                if tok in profession_tokens:
                    return True
            return False

        def _extract_profession_phrase(text: str) -> str:
            if not text:
                return ""
            cleaned = _normalize(
                re.sub(
                    r"^(?:é\s+)?(?:um|uma|uns|umas|o|a|os|as|the|an|a)\s+",
                    "",
                    text,
                    flags=re.IGNORECASE,
                )
            )
            spans = re.split(r"[,;\-–—\(\)]", cleaned)
            best: str = ""
            for sp in spans:
                sp_norm = _normalize(sp)
                if not sp_norm:
                    continue
                if _has_profession_token(sp_norm):
                    trimmed = sp_norm
                    if len(trimmed) > max_len:
                        m = re.search(
                            r"\b("
                            + "|".join(re.escape(t) for t in profession_tokens)
                            + r")\b",
                            trimmed,
                            re.IGNORECASE,
                        )
                        if m:
                            tail = trimmed[: m.end()]
                            trimmed = _normalize(tail)
                    if not best or len(trimmed) < len(best):
                        best = trimmed
            if best:
                return _shorten(best)
            head = re.split(r"[,;\-–—\(]", cleaned, 1)[0]
            head = _normalize(head)
            return _shorten(head) if head else ""

        name = (person.get("name") or "").strip()
        title = (person.get("article_title") or "").strip()
        nationality = _normalize(person.get("nationality") or "")
        nat_lower = nationality.lower()

        occ = _normalize(person.get("occupation") or "")
        if occ:
            return _shorten(occ)

        if title and title.lower() != name.lower():
            m = re.search(r"\(([^)]+)\)", title)
            if m:
                paren = _normalize(m.group(1))
                if paren and not _looks_like_year(paren):
                    if _has_profession_token(paren) or len(paren) <= 24:
                        if paren.lower() != nat_lower:
                            return _shorten(paren)

        desc_raw = (person.get("description") or "").strip()
        if desc_raw:
            phrase = _extract_profession_phrase(desc_raw)
            if phrase and phrase.lower() != nat_lower:
                if _has_profession_token(phrase) or len(phrase) <= 28:
                    return phrase

        if nationality and nationality != "—":
            return _shorten(nationality)

        return ""

    @rx.var
    def people_enriched(self) -> list[EnrichedPerson]:
        name_counts: dict[str, int] = {}
        for p in self.people:
            key = (p.get("name") or "").strip().lower()
            if key:
                name_counts[key] = name_counts.get(key, 0) + 1
        out: list[EnrichedPerson] = []
        for p in self.people:
            key = (p.get("name") or "").strip().lower()
            is_hom = name_counts.get(key, 0) > 1
            ctx = self._build_context_label(p)
            pid = p.get("id") or ""
            short_id = _short_qid(pid)
            display_name = p.get("name") or "—"
            if is_hom and ctx:
                display_name = f"{display_name} ({ctx})"
            out.append(
                {
                    "id": p["id"],
                    "name": p["name"],
                    "nationality": p["nationality"],
                    "birth_date": p["birth_date"],
                    "death_date": p["death_date"],
                    "birth_date_br": _format_br_date(p["birth_date"]),
                    "death_date_br": _format_br_date(p["death_date"]),
                    "birth_place": p["birth_place"],
                    "death_place": p["death_place"],
                    "birth_lat": float(p["birth_lat"]),
                    "birth_lng": float(p["birth_lng"]),
                    "death_lat": float(p["death_lat"]),
                    "death_lng": float(p["death_lng"]),
                    "article_url": p["article_url"],
                    "summary": p["summary"],
                    "searched_at": p["searched_at"],
                    "searched_at_br": _format_br_date(p["searched_at"]),
                    "completeness": int(p["completeness"]),
                    "image_url": p.get("image_url", ""),
                    "article_title": p.get("article_title", ""),
                    "is_living": bool(p.get("is_living", False)),
                    "context_label": ctx,
                    "is_homonym": is_hom,
                    "short_id": short_id,
                    "display_name": display_name,
                }
            )
        return out

    @rx.var
    def enriched_history(self) -> list[EnrichedHistoryEntry]:
        title_index: dict[str, list[dict]] = {}
        for ep in self.people_enriched:
            t = (
                (ep.get("article_title") or ep.get("name") or "")
                .strip()
                .lower()
            )
            if not t:
                continue
            title_index.setdefault(t, []).append(
                {
                    "qid": ep["id"],
                    "ctx": ep.get("context_label", ""),
                    "is_homonym": bool(ep.get("is_homonym", False)),
                }
            )
        name_index: dict[str, list[dict]] = {}
        for ep in self.people_enriched:
            n = (ep.get("name") or "").strip().lower()
            if not n:
                continue
            name_index.setdefault(n, []).append(
                {
                    "qid": ep["id"],
                    "ctx": ep.get("context_label", ""),
                    "is_homonym": bool(ep.get("is_homonym", False)),
                }
            )
        out: list[EnrichedHistoryEntry] = []
        for h in self.history:
            title = (h.get("title") or "").strip()
            key_t = title.lower()
            short = ""
            full_qid = ""
            ctx = ""
            matches = title_index.get(key_t) or name_index.get(key_t) or []
            if len(matches) >= 1:
                full_qid = matches[0]["qid"]
                short = _short_qid(full_qid)
                if matches[0].get("is_homonym"):
                    ctx = matches[0]["ctx"]
            out.append(
                {
                    "term": h.get("term", ""),
                    "title": title,
                    "timestamp": h.get("timestamp", ""),
                    "timestamp_br": _format_br_date(h.get("timestamp", "")),
                    "status": h.get("status", ""),
                    "short_id": short,
                    "qid": full_qid,
                    "context_label": ctx,
                }
            )
        return out

    def _enriched_lookup(self) -> dict[str, EnrichedPerson]:
        return {ep["id"]: ep for ep in self.people_enriched}

    @rx.var
    def map_points(self) -> list[MapPoint]:
        points: list[MapPoint] = []
        focus_id = self.selected_person_id
        enriched = self.people_enriched
        if focus_id:
            enriched_iter = [p for p in enriched if p["id"] == focus_id]
        else:
            enriched_iter = enriched
        offset = 0.0065
        for p in enriched_iter:
            has_birth = p["birth_lat"] != 0.0 or p["birth_lng"] != 0.0
            has_death = p["death_lat"] != 0.0 or p["death_lng"] != 0.0
            overlap = False
            if has_birth and has_death:
                if (
                    abs(p["birth_lat"] - p["death_lat"]) < 0.001
                    and abs(p["birth_lng"] - p["death_lng"]) < 0.001
                ):
                    overlap = True
            ctx = p.get("context_label", "")
            is_hom = bool(p.get("is_homonym", False))
            short_id = p.get("short_id", "")
            display_name = p.get("display_name", p["name"])
            occupation_val = p.get("occupation", "") or ""
            nationality_val = p.get("nationality", "") or ""
            article_url_val = p.get("article_url", "") or ""
            summary_val = p.get("summary", "") or ""
            birth_date_br_val = p.get("birth_date_br", "") or ""
            death_date_br_val = p.get("death_date_br", "") or ""
            birth_place_val = p.get("birth_place", "") or ""
            death_place_val = p.get("death_place", "") or ""
            is_living_val = bool(p.get("is_living", False))
            if has_birth:
                blat = p["birth_lat"]
                blng = p["birth_lng"]
                if overlap:
                    blat = blat + offset
                    blng = blng - offset
                points.append(
                    {
                        "id": f"{p['id']}_b",
                        "qid": p["id"],
                        "name": p["name"],
                        "place": p["birth_place"],
                        "date": p["birth_date"],
                        "date_br": _format_br_date(p["birth_date"]),
                        "lat": blat,
                        "lng": blng,
                        "kind": "Nascimento",
                        "image_url": p.get("image_url", ""),
                        "context_label": ctx,
                        "is_homonym": is_hom,
                        "short_id": short_id,
                        "display_name": display_name,
                        "nationality": nationality_val,
                        "article_url": article_url_val,
                        "birth_date_br": birth_date_br_val,
                        "death_date_br": death_date_br_val,
                        "birth_place": birth_place_val,
                        "death_place": death_place_val,
                        "is_living": is_living_val,
                        "occupation": occupation_val,
                        "summary": summary_val,
                    }
                )
            if has_death:
                dlat = p["death_lat"]
                dlng = p["death_lng"]
                if overlap:
                    dlat = dlat - offset
                    dlng = dlng + offset
                points.append(
                    {
                        "id": f"{p['id']}_d",
                        "qid": p["id"],
                        "name": p["name"],
                        "place": p["death_place"],
                        "date": p["death_date"],
                        "date_br": _format_br_date(p["death_date"]),
                        "lat": dlat,
                        "lng": dlng,
                        "kind": "Falecimento",
                        "image_url": p.get("image_url", ""),
                        "context_label": ctx,
                        "is_homonym": is_hom,
                        "short_id": short_id,
                        "display_name": display_name,
                        "nationality": nationality_val,
                        "article_url": article_url_val,
                        "birth_date_br": birth_date_br_val,
                        "death_date_br": death_date_br_val,
                        "birth_place": birth_place_val,
                        "death_place": death_place_val,
                        "is_living": is_living_val,
                        "occupation": occupation_val,
                        "summary": summary_val,
                    }
                )
        return points

    @rx.var
    def map_connections(self) -> list[MapConnection]:
        focus_id = self.selected_person_id
        people_iter = self.people
        if focus_id:
            people_iter = [p for p in self.people if p["id"] == focus_id]
        connections: list[MapConnection] = []
        offset = 0.0065
        for p in people_iter:
            has_birth = p["birth_lat"] != 0.0 or p["birth_lng"] != 0.0
            has_death = p["death_lat"] != 0.0 or p["death_lng"] != 0.0
            if not (has_birth and has_death):
                continue
            blat = p["birth_lat"]
            blng = p["birth_lng"]
            dlat = p["death_lat"]
            dlng = p["death_lng"]
            overlap = abs(blat - dlat) < 0.001 and abs(blng - dlng) < 0.001
            if overlap:
                blat = blat + offset
                blng = blng - offset
                dlat = dlat - offset
                dlng = dlng + offset
            connections.append(
                {
                    "id": p["id"],
                    "name": p["name"],
                    "birth_lat": blat,
                    "birth_lng": blng,
                    "death_lat": dlat,
                    "death_lng": dlng,
                    "is_selected": p["id"] == focus_id,
                }
            )
        return connections

    @rx.var
    def is_map_focused(self) -> bool:
        return self.selected_person_id != ""

    @rx.var
    def total_map_points(self) -> int:
        return len(self.map_points)

    @rx.var
    def map_center_lat(self) -> float:
        pts = self.map_points
        if not pts:
            return 20.0
        return sum(p["lat"] for p in pts) / len(pts)

    @rx.var
    def map_center_lng(self) -> float:
        pts = self.map_points
        if not pts:
            return 0.0
        return sum(p["lng"] for p in pts) / len(pts)

    @rx.var
    def timeline_events(self) -> list[TimelineEvent]:
        events: list[TimelineEvent] = []
        enriched = self.people_enriched
        for p in enriched:
            ctx = p.get("context_label", "")
            is_hom = bool(p.get("is_homonym", False))
            short_id = p.get("short_id", "")
            display_name = p.get("display_name", p["name"])
            if p["birth_date"] and p["birth_date"] != "—":
                try:
                    year = int(p["birth_date"][:4])
                    events.append(
                        {
                            "id": f"{p['id']}_b",
                            "person_id": p["id"],
                            "qid": p["id"],
                            "name": p["name"],
                            "year": year,
                            "date": p["birth_date"],
                            "date_br": _format_br_date(p["birth_date"]),
                            "place": p["birth_place"],
                            "kind": "Nascimento",
                            "context_label": ctx,
                            "is_homonym": is_hom,
                            "short_id": short_id,
                            "display_name": display_name,
                        }
                    )
                except ValueError:
                    pass
            if p["death_date"] and p["death_date"] != "—":
                try:
                    year = int(p["death_date"][:4])
                    events.append(
                        {
                            "id": f"{p['id']}_d",
                            "person_id": p["id"],
                            "qid": p["id"],
                            "name": p["name"],
                            "year": year,
                            "date": p["death_date"],
                            "date_br": _format_br_date(p["death_date"]),
                            "place": p["death_place"],
                            "kind": "Falecimento",
                            "context_label": ctx,
                            "is_homonym": is_hom,
                            "short_id": short_id,
                            "display_name": display_name,
                        }
                    )
                except ValueError:
                    pass
        events.sort(key=lambda e: e["year"])
        if self.timeline_filter == "birth":
            events = [e for e in events if e["kind"] == "Nascimento"]
        elif self.timeline_filter == "death":
            events = [e for e in events if e["kind"] == "Falecimento"]
        return events

    @rx.var
    def total_timeline_events(self) -> int:
        return len(self.timeline_events)

    @rx.var
    def selected_person(self) -> dict[str, str]:
        for p in self.people_enriched:
            if p["id"] == self.selected_person_id:
                return {
                    "id": p["id"],
                    "qid": p["id"],
                    "name": p["name"],
                    "nationality": p["nationality"],
                    "birth_date": p.get("birth_date_br") or p["birth_date"],
                    "death_date": p.get("death_date_br") or p["death_date"],
                    "birth_place": p["birth_place"],
                    "death_place": p["death_place"],
                    "summary": p["summary"],
                    "article_url": p["article_url"],
                    "image_url": p.get("image_url", ""),
                    "context_label": p.get("context_label", ""),
                    "short_id": p.get("short_id", ""),
                    "display_name": p.get("display_name", p["name"]),
                    "is_homonym": "true" if p.get("is_homonym") else "false",
                    "article_title": p.get("article_title", ""),
                    "occupation": p.get("occupation", ""),
                    "is_living": "true" if p.get("is_living") else "false",
                }
        return {
            "id": "",
            "qid": "",
            "name": "",
            "nationality": "",
            "birth_date": "",
            "death_date": "",
            "birth_place": "",
            "death_place": "",
            "summary": "",
            "article_url": "",
            "image_url": "",
            "context_label": "",
            "short_id": "",
            "display_name": "",
            "is_homonym": "false",
            "article_title": "",
            "occupation": "",
            "is_living": "false",
        }

    @rx.var
    def has_selected_person(self) -> bool:
        return self.selected_person_id != "" and any(
            p["id"] == self.selected_person_id for p in self.people
        )

    @rx.var
    def nationality_distribution(self) -> list[DistRow]:
        counts: dict[str, int] = {}
        for p in self.people:
            key = (
                p["nationality"]
                if p["nationality"] and p["nationality"] != "—"
                else "Desconhecida"
            )
            counts[key] = counts.get(key, 0) + 1
        items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
        return [{"label": k, "count": v} for k, v in items]

    @rx.var
    def century_distribution(self) -> list[DistRow]:
        counts: dict[int, int] = {}
        for p in self.people:
            if p["birth_date"] and p["birth_date"] != "—":
                try:
                    y = int(p["birth_date"][:4])
                    century = (y - 1) // 100 + 1 if y > 0 else 0
                    counts[century] = counts.get(century, 0) + 1
                except ValueError:
                    pass
        items = sorted(counts.items())
        out: list[DistRow] = []
        for c, v in items:
            label = f"Século {c}" if c > 0 else "Antigo"
            out.append({"label": label, "count": v})
        return out

    @rx.var
    def total_living(self) -> int:
        return sum(1 for p in self.people if p.get("is_living"))

    @rx.var
    def total_deceased(self) -> int:
        return sum(1 for p in self.people if not p.get("is_living"))

    @rx.var
    def completeness_buckets(self) -> list[DistRow]:
        buckets = {"100%": 0, "75-99%": 0, "50-74%": 0, "<50%": 0}
        for p in self.people:
            c = p["completeness"]
            if c == 100:
                buckets["100%"] += 1
            elif c >= 75:
                buckets["75-99%"] += 1
            elif c >= 50:
                buckets["50-74%"] += 1
            else:
                buckets["<50%"] += 1
        return [{"label": k, "count": v} for k, v in buckets.items()]

    @rx.var
    def avg_completeness(self) -> int:
        if not self.people:
            return 0
        return int(
            round(
                sum(p["completeness"] for p in self.people) / len(self.people)
            )
        )

    @rx.var
    def dashboard_latest_people(self) -> list[EnrichedPerson]:
        return self.people_enriched[:5]

    @rx.var
    def dashboard_recent_history(self) -> list[EnrichedHistoryEntry]:
        return self.enriched_history[:6]

    @rx.var
    def dashboard_top_nationalities(self) -> list[DistRow]:
        return self.nationality_distribution[:5]

    @rx.var
    def lifespan_distribution(self) -> list[DistRow]:
        buckets = {"<40": 0, "40-59": 0, "60-79": 0, "80+": 0}
        for p in self.people:
            if (
                p["birth_date"]
                and p["birth_date"] != "—"
                and p["death_date"]
                and p["death_date"] != "—"
            ):
                try:
                    by = int(p["birth_date"][:4])
                    dy = int(p["death_date"][:4])
                    age = dy - by
                    if age < 0:
                        continue
                    if age < 40:
                        buckets["<40"] += 1
                    elif age < 60:
                        buckets["40-59"] += 1
                    elif age < 80:
                        buckets["60-79"] += 1
                    else:
                        buckets["80+"] += 1
                except ValueError:
                    pass
        return [{"label": k, "count": v} for k, v in buckets.items()]

    @rx.var
    def average_lifespan(self) -> int:
        ages: list[int] = []
        for p in self.people:
            if (
                p["birth_date"]
                and p["birth_date"] != "—"
                and p["death_date"]
                and p["death_date"] != "—"
            ):
                try:
                    by = int(p["birth_date"][:4])
                    dy = int(p["death_date"][:4])
                    age = dy - by
                    if age >= 0:
                        ages.append(age)
                except ValueError:
                    pass
        if not ages:
            return 0
        return int(round(sum(ages) / len(ages)))

    @rx.var
    def oldest_person_name(self) -> str:
        best = -1
        name = "—"
        for p in self.people:
            if (
                p["birth_date"]
                and p["birth_date"] != "—"
                and p["death_date"]
                and p["death_date"] != "—"
            ):
                try:
                    age = int(p["death_date"][:4]) - int(p["birth_date"][:4])
                    if age > best:
                        best = age
                        name = p["name"]
                except ValueError:
                    pass
        return name

    @rx.var
    def youngest_person_name(self) -> str:
        best = 10**6
        name = "—"
        for p in self.people:
            if (
                p["birth_date"]
                and p["birth_date"] != "—"
                and p["death_date"]
                and p["death_date"] != "—"
            ):
                try:
                    age = int(p["death_date"][:4]) - int(p["birth_date"][:4])
                    if 0 <= age < best:
                        best = age
                        name = p["name"]
                except ValueError:
                    pass
        return name

    @rx.var
    def total_movers(self) -> int:
        count = 0
        for p in self.people:
            bp = (p["birth_place"] or "").strip()
            dp = (p["death_place"] or "").strip()
            if bp and dp and bp != "—" and dp != "—" and bp != dp:
                count += 1
        return count

    @rx.var
    def total_stayers(self) -> int:
        count = 0
        for p in self.people:
            bp = (p["birth_place"] or "").strip()
            dp = (p["death_place"] or "").strip()
            if bp and dp and bp != "—" and dp != "—" and bp == dp:
                count += 1
        return count

    @rx.var
    def mobility_distribution(self) -> list[DistRow]:
        return [
            {"label": "Mudaram de local", "count": self.total_movers},
            {"label": "Mesmo local", "count": self.total_stayers},
        ]

    @rx.var
    def missing_fields_distribution(self) -> list[DistRow]:
        counts = {
            "Nacionalidade": 0,
            "Nascimento (data)": 0,
            "Falecimento (data)": 0,
            "Nascimento (local)": 0,
            "Falecimento (local)": 0,
        }
        for p in self.people:
            living = bool(p.get("is_living"))
            if not p["nationality"] or p["nationality"] == "—":
                counts["Nacionalidade"] += 1
            if not p["birth_date"] or p["birth_date"] == "—":
                counts["Nascimento (data)"] += 1
            if not living and (not p["death_date"] or p["death_date"] == "—"):
                counts["Falecimento (data)"] += 1
            if not p["birth_place"] or p["birth_place"] == "—":
                counts["Nascimento (local)"] += 1
            if not living and (not p["death_place"] or p["death_place"] == "—"):
                counts["Falecimento (local)"] += 1
        return [{"label": k, "count": v} for k, v in counts.items()]

    @rx.var
    def top_birth_places(self) -> list[DistRow]:
        counts: dict[str, int] = {}
        for p in self.people:
            place = (p["birth_place"] or "").strip()
            if place and place != "—":
                counts[place] = counts.get(place, 0) + 1
        items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:8]
        return [{"label": k, "count": v} for k, v in items]

    @rx.var
    def top_death_places(self) -> list[DistRow]:
        counts: dict[str, int] = {}
        for p in self.people:
            place = (p["death_place"] or "").strip()
            if place and place != "—":
                counts[place] = counts.get(place, 0) + 1
        items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:8]
        return [{"label": k, "count": v} for k, v in items]

    @rx.var
    def total_unique_nationalities(self) -> int:
        s = set()
        for p in self.people:
            n = (p["nationality"] or "").strip()
            if n and n != "—":
                s.add(n)
        return len(s)

    @rx.var
    def peak_century(self) -> str:
        dist = self.century_distribution
        if not dist:
            return "—"
        best = max(dist, key=lambda d: d["count"])
        return best["label"]

    @rx.var
    def peak_century_count(self) -> int:
        dist = self.century_distribution
        if not dist:
            return 0
        return max(d["count"] for d in dist)

    @rx.var
    def earliest_birth_year(self) -> int:
        years = []
        for p in self.people:
            if p["birth_date"] and p["birth_date"] != "—":
                try:
                    years.append(int(p["birth_date"][:4]))
                except ValueError:
                    pass
        return min(years) if years else 0

    @rx.var
    def latest_death_year(self) -> int:
        years = []
        for p in self.people:
            if p["death_date"] and p["death_date"] != "—":
                try:
                    years.append(int(p["death_date"][:4]))
                except ValueError:
                    pass
        return max(years) if years else 0

    @rx.var
    def total_with_coordinates(self) -> int:
        count = 0
        for p in self.people:
            if (p["birth_lat"] != 0.0 or p["birth_lng"] != 0.0) or (
                p["death_lat"] != 0.0 or p["death_lng"] != 0.0
            ):
                count += 1
        return count

    @rx.var
    def total_fully_geocoded(self) -> int:
        count = 0
        for p in self.people:
            has_birth = p["birth_lat"] != 0.0 or p["birth_lng"] != 0.0
            has_death = p["death_lat"] != 0.0 or p["death_lng"] != 0.0
            if has_birth and has_death:
                count += 1
        return count

    @rx.var
    def geocoding_coverage(self) -> int:
        if not self.people:
            return 0
        return int(round(self.total_with_coordinates * 100 / len(self.people)))

    @rx.var
    def decade_distribution(self) -> list[DistRow]:
        counts: dict[int, int] = {}
        for p in self.people:
            if p["birth_date"] and p["birth_date"] != "—":
                try:
                    y = int(p["birth_date"][:4])
                    decade = (y // 10) * 10
                    counts[decade] = counts.get(decade, 0) + 1
                except ValueError:
                    pass
        items = sorted(counts.items())
        return [{"label": f"{d}s", "count": v} for d, v in items]

    @rx.var
    def gender_balance_unknown(self) -> int:
        return len(self.people)

    @rx.var
    def filtered_people(self) -> list[EnrichedPerson]:
        q = self.table_search.strip().lower()
        enriched = self.people_enriched
        if not q:
            return enriched
        return [
            p
            for p in enriched
            if q in p["name"].lower()
            or q in p["nationality"].lower()
            or q in p["birth_place"].lower()
            or q in p["death_place"].lower()
            or q in (p.get("context_label") or "").lower()
            or q in (p.get("article_title") or "").lower()
        ]

    @rx.event
    def export_csv(self):
        import csv
        import io

        buf = io.StringIO()
        writer = csv.writer(buf, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [
                "Nome",
                "Titulo do Artigo",
                "Wikidata ID",
                "Nacionalidade",
                "Nascimento",
                "Local Nascimento",
                "Falecimento",
                "Local Falecimento",
                "Status",
                "Completude (%)",
                "URL Wikipedia",
                "Pesquisado em",
            ]
        )
        for p in self.people:
            living = bool(p.get("is_living"))
            writer.writerow(
                [
                    p.get("name", ""),
                    p.get("article_title", "") or p.get("name", ""),
                    p.get("id", ""),
                    p.get("nationality", ""),
                    _format_br_date(p.get("birth_date", "")),
                    p.get("birth_place", ""),
                    "Vivo(a)"
                    if living
                    else _format_br_date(p.get("death_date", "")),
                    "—" if living else p.get("death_place", ""),
                    "Vivo(a)" if living else "Falecido(a)",
                    p.get("completeness", 0),
                    p.get("article_url", ""),
                    _format_br_date(p.get("searched_at", "")),
                ]
            )
        return rx.download(
            data=buf.getvalue(),
            filename="geohist_composicao.csv",
        )

    @rx.var
    def total_people(self) -> int:
        return len(self.people)

    @rx.var
    def total_locations(self) -> int:
        places = set()
        for p in self.people:
            if p["birth_place"]:
                places.add(p["birth_place"])
            if p["death_place"]:
                places.add(p["death_place"])
        return len(places)

    @rx.var
    def timeline_span(self) -> str:
        years: list[int] = []
        for p in self.people:
            if p["birth_date"]:
                try:
                    years.append(int(p["birth_date"][:4]))
                except ValueError:
                    pass
            if p["death_date"]:
                try:
                    years.append(int(p["death_date"][:4]))
                except ValueError:
                    pass
        if not years:
            return "—"
        return f"{min(years)} – {max(years)}"

    @rx.var
    def total_history(self) -> int:
        return len(self.history)

    @rx.var
    def has_results(self) -> bool:
        return len(self.search_results) > 0

    @rx.event
    def set_search_query(self, value: str):
        self.search_query = value

    @rx.event
    def clear_search(self):
        self.search_query = ""
        self.search_results = []
        self.has_preview = False
        self.error_message = ""
        self.info_message = ""
        self.is_disambiguation = False
        self.is_human = False

    @rx.event
    async def search_for(self, term: str):
        self.search_query = term
        return ResearchState.perform_search

    @rx.event
    async def run_suggested_search(self, term: str):
        self.search_query = term
        self.error_message = ""
        self.info_message = ""
        self.has_preview = False
        self.is_disambiguation = False
        if not term.strip():
            self.error_message = "Digite um termo para iniciar a pesquisa."
            self.search_results = []
            return
        self.is_searching = True
        results = await asyncio.to_thread(_wiki_search, term.strip(), 8)
        self.is_searching = False
        if results is None:
            self.error_message = "Falha ao consultar a Wikipédia. Verifique sua conexão e tente novamente."
            self.search_results = []
            self._add_history(term, "—", "Erro de rede")
            return
        if not results:
            self.error_message = (
                f"Nenhum resultado encontrado para “{term}”. Tente outro termo."
            )
            self.search_results = []
            self._add_history(term, "—", "Sem resultados")
            return
        self.search_results = [
            {
                "title": r.get("title", ""),
                "snippet": _strip_html(r.get("snippet", "")),
                "pageid": int(r.get("pageid", 0)),
            }
            for r in results
        ]
        self.info_message = (
            f"{len(self.search_results)} resultados encontrados para “{term}”. "
            "Selecione um artigo para pré-visualizar."
        )

    @rx.event
    async def perform_search(self):
        term = self.search_query.strip()
        self.error_message = ""
        self.info_message = ""
        self.has_preview = False
        self.is_disambiguation = False
        if not term:
            self.error_message = "Digite um termo para iniciar a pesquisa."
            self.search_results = []
            self.is_searching = False
            return
        self.is_searching = True
        search_term = term

        results = await asyncio.to_thread(_wiki_search, search_term, 8)

        self.is_searching = False
        if results is None:
            self.error_message = "Falha ao consultar a Wikipédia. Verifique sua conexão e tente novamente."
            self.search_results = []
            self._add_history(search_term, "—", "Erro de rede")
            return
        if not results:
            self.error_message = f"Nenhum resultado encontrado para “{search_term}”. Tente outro termo."
            self.search_results = []
            self._add_history(search_term, "—", "Sem resultados")
            return
        self.search_results = [
            {
                "title": r.get("title", ""),
                "snippet": _strip_html(r.get("snippet", "")),
                "pageid": int(r.get("pageid", 0)),
            }
            for r in results
        ]
        self.info_message = (
            f"{len(self.search_results)} resultados encontrados para “{search_term}”. "
            "Selecione um artigo para pré-visualizar."
        )

    @rx.event
    async def select_article(self, title: str):
        self.is_loading_article = True
        self.error_message = ""
        self.info_message = ""
        self.has_preview = False
        self.is_disambiguation = False
        self.is_human = False
        chosen = title

        page = await asyncio.to_thread(_wiki_article, chosen)

        wikidata_id = ""
        is_disamb = False
        is_human = False
        extract = ""
        page_url = ""
        page_title = chosen

        if page is None:
            self.is_loading_article = False
            self.error_message = "Falha ao carregar o artigo. Verifique sua conexão e tente novamente."
            return

        if "missing" in page:
            self.is_loading_article = False
            self.error_message = (
                f"Artigo “{chosen}” não foi encontrado na Wikipédia."
            )
            return

        page_title = page.get("title", chosen)
        extract_raw = page.get("extract", "") or ""
        extract = (
            _format_preview_extract(extract_raw)
            or _strip_html(extract_raw)
            or extract_raw
        )
        page_url = page.get("fullurl") or (
            f"https://pt.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        )
        pageprops = page.get("pageprops", {}) or {}
        wikidata_id = pageprops.get("wikibase_item", "") or ""
        is_disamb = "disambiguation" in pageprops
        thumb = page.get("thumbnail", {}) or {}
        image_url = thumb.get("source", "") or ""

        entity = None
        if wikidata_id and not is_disamb:
            entity = await asyncio.to_thread(_wd_entity, wikidata_id)
            if entity:
                claims = entity.get("claims", {}) or {}
                try:
                    for c in claims.get("P31", []) or []:
                        snak = c.get("mainsnak", {}) or {}
                        if snak.get("snaktype") != "value":
                            continue
                        value = snak.get("datavalue", {}).get("value", {}) or {}
                        if value.get("id") == "Q5":
                            is_human = True
                            break
                except (KeyError, TypeError, AttributeError):
                    logging.exception("Unexpected error")
                    is_human = False

        self.selected_preview = {
            "title": page_title,
            "extract": extract or "Sem resumo disponível para este artigo.",
            "url": page_url,
            "wikidata_id": wikidata_id or "—",
            "image_url": image_url,
        }
        self.has_preview = True
        self.is_disambiguation = is_disamb
        self.is_human = is_human
        self.is_loading_article = False
        if is_disamb:
            self.error_message = "Esta é uma página de desambiguação. Escolha um resultado mais específico nos resultados acima."
        elif not wikidata_id:
            self.info_message = "Este artigo não possui vínculo com o Wikidata, portanto dados biográficos estruturados não estão disponíveis."
        elif not is_human:
            self.info_message = "Este artigo não parece se referir a uma pessoa. A extração biográfica é otimizada para pessoas (P31 = Q5)."
        else:
            self.info_message = "Pré-visualização carregada. Confirme para extrair informações biográficas estruturadas."
        yield rx.scroll_to("preview-anchor")

    @rx.event
    async def confirm_article(self):
        if not self.has_preview or self.is_disambiguation:
            self.error_message = "Selecione um artigo válido (não desambiguação) antes de confirmar."
            return
        preview = dict(self.selected_preview)
        search_term = self.search_query.strip() or preview.get("title", "")
        self.is_extracting = True
        self.error_message = ""

        qid = preview.get("wikidata_id", "")
        title = preview.get("title", "")
        url = preview.get("url", "")
        extract_text = preview.get("extract", "")

        if not qid or qid == "—":
            self.is_extracting = False
            self.error_message = "Este artigo não tem entidade no Wikidata; não é possível extrair dados estruturados."
            self._add_history(search_term, title, "Sem Wikidata")
            return

        entity = await asyncio.to_thread(_wd_entity, qid)
        if entity is None:
            self.is_extracting = False
            self.error_message = "Falha ao consultar o Wikidata. Verifique sua conexão e tente novamente."
            self._add_history(search_term, title, "Erro de rede")
            yield rx.toast(
                title="Erro ao consultar Wikidata",
                description="Não foi possível obter os dados estruturados. Tente novamente em instantes.",
                position="bottom-right",
                duration=4500,
                close_button=True,
            )
            return
        if not isinstance(entity, dict):
            self.is_extracting = False
            self.error_message = (
                "Resposta inválida do Wikidata. Tente novamente em instantes."
            )
            self._add_history(search_term, title, "Resposta inválida")
            yield rx.toast(
                title="Resposta inválida",
                description="O Wikidata retornou um formato inesperado para este artigo.",
                position="bottom-right",
                duration=4500,
                close_button=True,
            )
            return
        claims = entity.get("claims", {}) or {}
        if not isinstance(claims, dict) or not claims:
            self.is_extracting = False
            self.error_message = "Este artigo do Wikidata não possui declarações estruturadas (claims). Não é possível extrair dados biográficos."
            self._add_history(search_term, title, "Sem claims")
            yield rx.toast(
                title="Sem dados estruturados",
                description="A entidade Wikidata não tem claims utilizáveis para extração biográfica.",
                position="bottom-right",
                duration=4500,
                close_button=True,
            )
            return
        is_person = False
        for c in claims.get("P31", []) or []:
            try:
                snak = c.get("mainsnak", {}) or {}
                if snak.get("snaktype") != "value":
                    continue
                value = snak.get("datavalue", {}).get("value", {}) or {}
                if value.get("id") == "Q5":
                    is_person = True
                    break
            except (KeyError, TypeError, AttributeError):
                logging.exception("Unexpected error")
                continue

        if not is_person:
            self.is_extracting = False
            self.error_message = "Este artigo não é biográfico (não corresponde a uma pessoa no Wikidata). Selecione outro artigo."
            self._add_history(search_term, title, "Não-biográfico")
            return

        name = _label_of(entity) or title
        birth_date = _claim_time(claims, "P569")
        death_date = _claim_time(claims, "P570")
        birth_qid = _claim_qid(claims, "P19")
        death_qid = _claim_qid(claims, "P20")
        nat_qid = _claim_qid(claims, "P27")
        is_living = (not death_date) and (not death_qid)

        occupation_qids: list[str] = []
        for c in claims.get("P106", []) or []:
            try:
                snak = c.get("mainsnak", {}) or {}
                if snak.get("snaktype") != "value":
                    continue
                value = snak.get("datavalue", {}).get("value", {}) or {}
                qid_o = value.get("id", "") or ""
                if qid_o and qid_o not in occupation_qids:
                    occupation_qids.append(qid_o)
            except (KeyError, TypeError, AttributeError):
                logging.exception("Erro ao ler ocupação")
                continue
        occupation_qids = occupation_qids[:3]

        descriptions = entity.get("descriptions", {}) or {}
        wd_description = (
            (descriptions.get("pt", {}) or {}).get("value")
            or (descriptions.get("en", {}) or {}).get("value")
            or ""
        ).strip()

        ref_qids = [
            q for q in [birth_qid, death_qid, nat_qid] if q
        ] + occupation_qids
        ref_entities = (
            await asyncio.to_thread(_wd_entities, ref_qids) if ref_qids else {}
        )

        occupation_labels: list[str] = []
        for q in occupation_qids:
            lbl = _label_of(ref_entities.get(q))
            if lbl and lbl not in occupation_labels:
                occupation_labels.append(lbl)
        occupation = ", ".join(occupation_labels[:2])

        birth_place = (
            _label_of(ref_entities.get(birth_qid)) if birth_qid else ""
        )
        death_place = (
            _label_of(ref_entities.get(death_qid)) if death_qid else ""
        )
        nationality = _label_of(ref_entities.get(nat_qid)) if nat_qid else ""

        birth_coords = (
            _coords_of(ref_entities.get(birth_qid)) if birth_qid else None
        )
        death_coords = (
            _coords_of(ref_entities.get(death_qid)) if death_qid else None
        )

        if birth_qid and birth_coords is None:
            birth_coords = await _fallback_coords(birth_qid, ref_entities)
        if death_qid and death_coords is None:
            death_coords = await _fallback_coords(death_qid, ref_entities)

        country_qids = []
        for q in [birth_qid, death_qid]:
            if q and q in ref_entities:
                cq = _claim_qid(ref_entities[q].get("claims", {}) or {}, "P17")
                if cq and cq not in ref_entities:
                    country_qids.append(cq)
        if country_qids:
            extra = await asyncio.to_thread(_wd_entities, country_qids)
            ref_entities.update(extra)

        birth_place_full = _full_place(birth_qid, birth_place, ref_entities)
        death_place_full = _full_place(death_qid, death_place, ref_entities)

        if is_living:
            fields = [
                bool(name),
                bool(nationality),
                bool(birth_date),
                bool(birth_place_full),
            ]
        else:
            fields = [
                bool(name),
                bool(nationality),
                bool(birth_date),
                bool(death_date),
                bool(birth_place_full),
                bool(death_place_full),
            ]
        completeness = int(round(sum(fields) / len(fields) * 100))

        missing = []
        if not nationality:
            missing.append("nacionalidade")
        if not birth_date:
            missing.append("data de nascimento")
        if not is_living and not death_date:
            missing.append("data de falecimento")
        if not birth_place_full:
            missing.append("local de nascimento")
        if not is_living and not death_place_full:
            missing.append("local de falecimento")

        image_url = preview.get("image_url", "") or ""
        article_title = preview.get("title", "") or title
        record: PersonRecord = {
            "id": qid,
            "name": name,
            "nationality": nationality or "—",
            "birth_date": birth_date or "—",
            "death_date": "Vivo(a)" if is_living else (death_date or "—"),
            "birth_place": birth_place_full or "—",
            "death_place": "—" if is_living else (death_place_full or "—"),
            "birth_lat": birth_coords[0] if birth_coords else 0.0,
            "birth_lng": birth_coords[1] if birth_coords else 0.0,
            "death_lat": death_coords[0] if death_coords else 0.0,
            "death_lng": death_coords[1] if death_coords else 0.0,
            "article_url": url,
            "summary": extract_text or "—",
            "searched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completeness": completeness,
            "image_url": image_url,
            "article_title": article_title,
            "is_living": is_living,
            "occupation": occupation,
            "description": wd_description,
        }

        self.is_extracting = False
        existing_ids = {p["id"] for p in self.people}
        persist_ok = True
        try:
            await asyncio.to_thread(save_person_db, record)
        except Exception as e:
            logging.exception(f"Erro ao persistir pessoa: {e}")
            persist_ok = False
            self.error_message = "Não foi possível salvar este registro localmente. Os dados aparecerão somente nesta sessão."
        is_update = qid in existing_ids
        if is_update:
            self.people = [record if p["id"] == qid else p for p in self.people]
            self.info_message = f"“{name}” já estava na composição — registro atualizado com dados frescos e salvo localmente."
        else:
            self.people = [record, *self.people]
            if missing:
                self.info_message = f"“{name}” adicionado(a) e salvo(a) localmente. Campos ausentes: {', '.join(missing)}."
            else:
                self.info_message = f"“{name}” adicionado(a) com dados biográficos completos e salvo(a) localmente."
        status = (
            "Sucesso" if completeness == 100 else f"Parcial ({completeness}%)"
        )
        await self._persist_history(search_term, name, status)
        self.has_preview = False
        self.last_persist_action = "atualizado" if is_update else "salvo"
        if persist_ok:
            yield rx.toast(
                title=(
                    "Registro atualizado" if is_update else "Registro salvo"
                ),
                description=(
                    f"“{name}” {'foi atualizado' if is_update else 'foi salvo'} no armazenamento local (completude {completeness}%)."
                ),
                position="bottom-right",
                duration=3500,
                close_button=True,
            )
        else:
            yield rx.toast(
                title="Salvo apenas em sessão",
                description=f"Não foi possível persistir “{name}” localmente. O registro existirá apenas nesta sessão.",
                position="bottom-right",
                duration=4500,
                close_button=True,
            )

    def _add_history(self, term: str, title: str, status: str):
        entry: HistoryEntry = {
            "term": term or "—",
            "title": title or "—",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": status,
        }
        self.history = [entry, *self.history][:50]
        try:
            save_history_db(entry)
        except Exception as e:
            logging.exception(f"Erro ao persistir histórico: {e}")

    async def _persist_history(self, term: str, title: str, status: str):
        entry: HistoryEntry = {
            "term": term or "—",
            "title": title or "—",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": status,
        }
        self.history = [entry, *self.history][:50]
        try:
            await asyncio.to_thread(save_history_db, entry)
        except Exception as e:
            logging.exception(f"Erro ao persistir histórico: {e}")

    @rx.event
    async def remove_person(self, person_id: str):
        removed = next((p for p in self.people if p["id"] == person_id), None)
        self.people = [p for p in self.people if p["id"] != person_id]
        if self.selected_person_id == person_id:
            self.selected_person_id = ""
        name = removed["name"] if removed else "Registro"
        try:
            await asyncio.to_thread(delete_person_db, person_id)
            self.info_message = (
                "Registro removido da composição e do armazenamento local."
            )
            self.last_persist_action = "removido"
            yield rx.toast(
                title="Registro removed",
                description=f"“{name}” foi excluído do armazenamento local.",
                position="bottom-right",
                duration=3500,
                close_button=True,
            )
        except Exception as e:
            logging.exception(f"Erro ao remover pessoa: {e}")
            self.error_message = "Falha ao remover do armazenamento local; o registro foi removido apenas desta sessão."
            yield rx.toast(
                title="Remoção parcial",
                description=f"“{name}” foi removido(a) da sessão, mas permanece no armazenamento local.",
                position="bottom-right",
                duration=4500,
                close_button=True,
            )

    @rx.event
    async def clear_history(self):
        previous_count = len(self.history)
        self.history = []
        try:
            await asyncio.to_thread(clear_history_db)
            self.info_message = (
                "Histórico de pesquisa limpo (também no armazenamento local)."
            )
            self.last_persist_action = "histórico limpo"
            yield rx.toast(
                title="Histórico limpo",
                description=f"{previous_count} entrada(s) removida(s) do armazenamento local.",
                position="bottom-right",
                duration=3500,
                close_button=True,
            )
        except Exception as e:
            logging.exception(f"Erro ao limpar histórico: {e}")
            self.error_message = (
                "Falha ao limpar histórico no armazenamento local."
            )
            yield rx.toast(
                title="Falha ao limpar histórico",
                description="Não foi possível limpar o histórico no armazenamento local.",
                position="bottom-right",
                duration=4500,
                close_button=True,
            )

    @rx.event
    async def refresh_from_storage(self):
        try:
            self.people = await asyncio.to_thread(load_people_db)
            self.history = await asyncio.to_thread(load_history_db)
            self.info_message = "Dados recarregados do armazenamento local."
            self.last_persist_action = "recarregado"
            yield rx.toast(
                title="Dados sincronizados",
                description=f"{len(self.people)} pessoa(s) e {len(self.history)} busca(s) recarregados do armazenamento local.",
                position="bottom-right",
                duration=3500,
                close_button=True,
            )
        except Exception as e:
            logging.exception(f"Erro ao recarregar dados: {e}")
            self.error_message = "Falha ao recarregar do armazenamento local."
            yield rx.toast(
                title="Falha ao sincronizar",
                description="Não foi possível recarregar do armazenamento local.",
                position="bottom-right",
                duration=4500,
                close_button=True,
            )

    @rx.event
    def export_csv_with_feedback(self):
        yield rx.toast(
            title="Exportação iniciada",
            description=f"{len(self.people)} registro(s) persistido(s) sendo exportados como CSV.",
            position="bottom-right",
            duration=2500,
            close_button=True,
        )
        yield ResearchState.export_csv