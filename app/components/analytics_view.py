import reflex as rx
from app.states.research_state import ResearchState


def nationality_bar_row(item) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                item["label"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-semibold text-gray-200",
                    "text-xs font-semibold text-gray-700",
                ),
            ),
            rx.el.span(
                item["count"].to_string(),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-bold text-blue-400 font-mono",
                    "text-xs font-bold text-blue-600 font-mono",
                ),
            ),
            class_name="flex items-center justify-between mb-1.5",
        ),
        rx.el.div(
            rx.el.div(
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "h-3.5 rounded-full bg-blue-500 transition-all duration-500",
                    "h-3.5 rounded-full bg-blue-600 transition-all duration-500",
                ),
                style={
                    "width": rx.cond(
                        ResearchState.total_people > 0,
                        f"{item['count'] * 100 / ResearchState.total_people}%",
                        "0%",
                    )
                },
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "h-3.5 w-full rounded-full bg-gray-800 overflow-hidden",
                "h-3.5 w-full rounded-full bg-gray-100 overflow-hidden",
            ),
        ),
        class_name="w-full mb-4",
    )


def nationality_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Distribuição por nacionalidade",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-base font-bold text-gray-100",
                    "text-base font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                "Quantidade de pessoas pesquisadas por país de origem.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-5",
        ),
        rx.cond(
            ResearchState.nationality_distribution.length() > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.nationality_distribution, nationality_bar_row
                ),
                class_name="space-y-1 max-h-[280px] overflow-y-auto pr-1",
            ),
            rx.el.div(
                rx.icon(
                    "chart-bar", class_name="h-7 w-7 text-gray-500 mx-auto"
                ),
                rx.el.p(
                    "Sem dados",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-2",
                        "text-sm text-gray-500 text-center mt-2",
                    ),
                ),
                class_name="py-12",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def century_bar_row(item) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                item["label"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-semibold text-gray-200",
                    "text-xs font-semibold text-gray-700",
                ),
            ),
            rx.el.span(
                item["count"].to_string(),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-bold text-amber-400 font-mono",
                    "text-xs font-bold text-amber-500 font-mono",
                ),
            ),
            class_name="flex items-center justify-between mb-1.5",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-3.5 rounded-full bg-amber-500 transition-all duration-500",
                style={
                    "width": rx.cond(
                        ResearchState.total_people > 0,
                        f"{item['count'] * 100 / ResearchState.total_people}%",
                        "0%",
                    )
                },
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "h-3.5 w-full rounded-full bg-gray-800 overflow-hidden",
                "h-3.5 w-full rounded-full bg-gray-100 overflow-hidden",
            ),
        ),
        class_name="w-full mb-4",
    )


def century_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Distribuição por século",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-base font-bold text-gray-100",
                    "text-base font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                "Pessoas agrupadas pelo século de nascimento.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-5",
        ),
        rx.cond(
            ResearchState.century_distribution.length() > 0,
            rx.el.div(
                rx.foreach(ResearchState.century_distribution, century_bar_row),
                class_name="space-y-1 max-h-[280px] overflow-y-auto pr-1",
            ),
            rx.el.div(
                rx.icon(
                    "chart-bar", class_name="h-7 w-7 text-gray-500 mx-auto"
                ),
                rx.el.p(
                    "Sem dados",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-2",
                        "text-sm text-gray-500 text-center mt-2",
                    ),
                ),
                class_name="py-12",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def completeness_row(item) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                item["label"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-semibold text-gray-200",
                    "text-xs font-semibold text-gray-700",
                ),
            ),
            rx.el.span(
                item["count"].to_string(),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-mono text-gray-100",
                    "text-xs font-mono text-gray-900",
                ),
            ),
            class_name="flex items-center justify-between mb-1",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-2 rounded-full bg-blue-500",
                style={
                    "width": rx.cond(
                        ResearchState.total_people > 0,
                        f"{item['count'] * 100 / ResearchState.total_people}%",
                        "0%",
                    ),
                },
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "h-2 rounded-full bg-gray-800 w-full overflow-hidden",
                "h-2 rounded-full bg-gray-100 w-full overflow-hidden",
            ),
        ),
        class_name="mb-3",
    )


def completeness_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Completude dos dados",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-base font-bold text-gray-100",
                    "text-base font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                f"Média de completude da composição.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    ResearchState.avg_completeness.to_string() + "%",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-3xl font-bold text-gray-100",
                        "text-3xl font-bold text-gray-900",
                    ),
                ),
                rx.el.p(
                    "Média geral",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400",
                        "text-xs text-gray-500",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "mb-4 pb-4 border-b border-gray-800",
                    "mb-4 pb-4 border-b border-gray-100",
                ),
            ),
            rx.foreach(ResearchState.completeness_buckets, completeness_row),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def recent_searches_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Buscas recentes",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-base font-bold text-gray-100",
                    "text-base font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                "Últimas atividades de pesquisa nesta sessão.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-3",
        ),
        rx.cond(
            ResearchState.total_history > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.enriched_history,
                    lambda h: rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "search",
                                class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    h["term"],
                                    title=h["term"],
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-sm font-medium text-gray-100",
                                        "text-sm font-medium text-gray-900",
                                    ),
                                ),
                                rx.el.p(
                                    f"→ {h['title']}",
                                    title=h["title"],
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-xs text-gray-400 break-words",
                                        "text-xs text-gray-500 break-words",
                                    ),
                                ),
                                rx.cond(
                                    h["context_label"] != "",
                                    rx.el.p(
                                        h["context_label"],
                                        title=h["context_label"],
                                        class_name=rx.cond(
                                            ResearchState.dark_mode,
                                            "text-[10px] text-amber-300 italic break-words mt-0.5",
                                            "text-[10px] text-amber-700 italic break-words mt-0.5",
                                        ),
                                    ),
                                    rx.fragment(),
                                ),
                                rx.cond(
                                    h["short_id"] != "",
                                    rx.el.a(
                                        h["short_id"],
                                        rx.icon(
                                            "external-link",
                                            class_name="h-2 w-2 inline-block ml-0.5",
                                        ),
                                        href="https://www.wikidata.org/wiki/"
                                        + h["qid"],
                                        target="_blank",
                                        title=f"Abrir {h['qid']} no Wikidata",
                                        class_name=rx.cond(
                                            ResearchState.dark_mode,
                                            "inline-flex items-center text-[9px] font-mono text-blue-300 bg-blue-950/40 border border-blue-900 hover:border-blue-700 px-1.5 py-0.5 rounded mt-1",
                                            "inline-flex items-center text-[9px] font-mono text-blue-700 bg-blue-50 border border-blue-100 hover:border-blue-300 px-1.5 py-0.5 rounded mt-1",
                                        ),
                                    ),
                                    rx.fragment(),
                                ),
                                class_name="min-w-0 flex-1",
                            ),
                            class_name="flex items-start gap-2 min-w-0 flex-1",
                        ),
                        rx.el.div(
                            rx.el.span(
                                h["status"],
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-[10px] font-semibold text-blue-300 bg-blue-950/40 border border-blue-900 px-2 py-0.5 rounded-full",
                                    "text-[10px] font-semibold text-blue-700 bg-blue-50 border border-blue-100 px-2 py-0.5 rounded-full",
                                ),
                            ),
                            rx.el.span(
                                h["timestamp_br"],
                                title=h["timestamp"],
                                class_name="text-[10px] text-gray-400 font-mono mt-1 block",
                            ),
                            class_name="text-right shrink-0",
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "flex items-start justify-between gap-3 py-2.5 border-b border-gray-800 last:border-0",
                            "flex items-start justify-between gap-3 py-2.5 border-b border-gray-100 last:border-0",
                        ),
                    ),
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Sem buscas recentes.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center py-8",
                        "text-sm text-gray-500 text-center py-8",
                    ),
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def insight_card(
    icon: str,
    label: str,
    value,
    sublabel: str,
    accent: str,
    accent_dark: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4"),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    f"h-9 w-9 rounded-lg flex items-center justify-center {accent_dark}",
                    f"h-9 w-9 rounded-lg flex items-center justify-center {accent}",
                ),
            ),
            class_name="flex items-start",
        ),
        rx.el.p(
            label,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-xs font-medium text-gray-400 mt-3",
                "text-xs font-medium text-gray-500 mt-3",
            ),
        ),
        rx.el.p(
            value,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-xl font-bold text-gray-100 mt-0.5",
                "text-xl font-bold text-gray-900 mt-0.5",
            ),
        ),
        rx.el.p(
            sublabel,
            class_name="text-[10px] font-medium text-gray-400 mt-0.5 truncate",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-4",
            "bg-white border border-gray-200 rounded-xl p-4",
        ),
    )


def lifespan_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("hourglass", class_name="h-4 w-4 text-violet-600"),
                rx.el.h3(
                    "Distribuição de longevidade",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.p(
                f"Idade média: {ResearchState.average_lifespan} anos. Mais longevo(a): {ResearchState.oldest_person_name}.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-5",
        ),
        rx.cond(
            ResearchState.total_people > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.lifespan_distribution,
                    lambda item: rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                f"{item['label']} anos",
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-xs font-semibold text-gray-200",
                                    "text-xs font-semibold text-gray-700",
                                ),
                            ),
                            rx.el.span(
                                item["count"].to_string(),
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-xs font-bold text-violet-400 font-mono",
                                    "text-xs font-bold text-violet-600 font-mono",
                                ),
                            ),
                            class_name="flex items-center justify-between mb-1.5",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-3 rounded-full bg-violet-500 transition-all duration-500",
                                style={
                                    "width": rx.cond(
                                        ResearchState.total_people > 0,
                                        f"{item['count'] * 100 / ResearchState.total_people}%",
                                        "0%",
                                    )
                                },
                            ),
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "h-3 w-full rounded-full bg-gray-800 overflow-hidden",
                                "h-3 w-full rounded-full bg-gray-100 overflow-hidden",
                            ),
                        ),
                        class_name="mb-3",
                    ),
                ),
            ),
            rx.el.p(
                "Sem dados",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm text-gray-400 text-center py-8",
                    "text-sm text-gray-500 text-center py-8",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def mobility_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("plane", class_name="h-4 w-4 text-emerald-600"),
                rx.el.h3(
                    "Mobilidade geográfica",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.p(
                "Quem viveu em outro lugar do que nasceu vs. quem permaneceu.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("plane", class_name="h-4 w-4 text-emerald-600"),
                    rx.el.span(
                        "Mudaram",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-semibold text-gray-200",
                            "text-xs font-semibold text-gray-700",
                        ),
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.p(
                    ResearchState.total_movers.to_string(),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-2xl font-bold text-emerald-400 mt-1",
                        "text-2xl font-bold text-emerald-600 mt-1",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "p-3 rounded-lg bg-emerald-950/30 border border-emerald-900",
                    "p-3 rounded-lg bg-emerald-50 border border-emerald-100",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("home", class_name="h-4 w-4 text-blue-600"),
                    rx.el.span(
                        "Permaneceram",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-semibold text-gray-200",
                            "text-xs font-semibold text-gray-700",
                        ),
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.p(
                    ResearchState.total_stayers.to_string(),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-2xl font-bold text-blue-400 mt-1",
                        "text-2xl font-bold text-blue-600 mt-1",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "p-3 rounded-lg bg-blue-950/30 border border-blue-900",
                    "p-3 rounded-lg bg-blue-50 border border-blue-100",
                ),
            ),
            class_name="grid grid-cols-2 gap-3 mb-3",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-2 rounded-l-full bg-emerald-500",
                style={
                    "width": rx.cond(
                        (
                            ResearchState.total_movers
                            + ResearchState.total_stayers
                        )
                        > 0,
                        f"{ResearchState.total_movers * 100 / (ResearchState.total_movers + ResearchState.total_stayers)}%",
                        "0%",
                    )
                },
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "h-2 w-full rounded-full bg-blue-500 overflow-hidden flex",
                "h-2 w-full rounded-full bg-blue-500 overflow-hidden flex",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def missing_fields_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("circle_alert", class_name="h-4 w-4 text-rose-600"),
                rx.el.h3(
                    "Campos ausentes",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.p(
                "Onde a Wikipédia/Wikidata deixou lacunas na composição.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-5",
        ),
        rx.cond(
            ResearchState.total_people > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.missing_fields_distribution,
                    lambda item: rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                item["label"],
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-xs font-semibold text-gray-200",
                                    "text-xs font-semibold text-gray-700",
                                ),
                            ),
                            rx.el.span(
                                item["count"].to_string(),
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-xs font-bold text-rose-400 font-mono",
                                    "text-xs font-bold text-rose-600 font-mono",
                                ),
                            ),
                            class_name="flex items-center justify-between mb-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-2 rounded-full bg-rose-500",
                                style={
                                    "width": rx.cond(
                                        ResearchState.total_people > 0,
                                        f"{item['count'] * 100 / ResearchState.total_people}%",
                                        "0%",
                                    )
                                },
                            ),
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "h-2 w-full rounded-full bg-gray-800 overflow-hidden",
                                "h-2 w-full rounded-full bg-gray-100 overflow-hidden",
                            ),
                        ),
                        class_name="mb-2.5",
                    ),
                ),
            ),
            rx.el.p(
                "Sem dados",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm text-gray-400 text-center py-8",
                    "text-sm text-gray-500 text-center py-8",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def top_places_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("map-pinned", class_name="h-4 w-4 text-blue-600"),
                rx.el.h3(
                    "Top locais",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.p(
                "Locais de nascimento e falecimento mais frequentes.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("baby", class_name="h-3.5 w-3.5 text-emerald-600"),
                    rx.el.span(
                        "Nascimento",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-bold uppercase tracking-wider text-emerald-400",
                            "text-[10px] font-bold uppercase tracking-wider text-emerald-700",
                        ),
                    ),
                    class_name="flex items-center gap-1.5 mb-2",
                ),
                rx.cond(
                    ResearchState.top_birth_places.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            ResearchState.top_birth_places,
                            lambda item: rx.el.div(
                                rx.el.span(
                                    class_name="h-1.5 w-1.5 rounded-full bg-emerald-500 shrink-0",
                                ),
                                rx.el.span(
                                    item["label"],
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-xs text-gray-300 truncate flex-1",
                                        "text-xs text-gray-700 truncate flex-1",
                                    ),
                                ),
                                rx.el.span(
                                    item["count"].to_string(),
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-[10px] font-mono font-bold text-emerald-400 shrink-0",
                                        "text-[10px] font-mono font-bold text-emerald-600 shrink-0",
                                    ),
                                ),
                                class_name="flex items-center gap-1.5 py-1",
                            ),
                        ),
                    ),
                    rx.el.p(
                        "Sem dados",
                        class_name="text-[11px] text-gray-400 py-2",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("flower-2", class_name="h-3.5 w-3.5 text-red-600"),
                    rx.el.span(
                        "Falecimento",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-bold uppercase tracking-wider text-red-400",
                            "text-[10px] font-bold uppercase tracking-wider text-red-700",
                        ),
                    ),
                    class_name="flex items-center gap-1.5 mb-2",
                ),
                rx.cond(
                    ResearchState.top_death_places.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            ResearchState.top_death_places,
                            lambda item: rx.el.div(
                                rx.el.span(
                                    class_name="h-1.5 w-1.5 rounded-full bg-red-500 shrink-0",
                                ),
                                rx.el.span(
                                    item["label"],
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-xs text-gray-300 truncate flex-1",
                                        "text-xs text-gray-700 truncate flex-1",
                                    ),
                                ),
                                rx.el.span(
                                    item["count"].to_string(),
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-[10px] font-mono font-bold text-red-400 shrink-0",
                                        "text-[10px] font-mono font-bold text-red-600 shrink-0",
                                    ),
                                ),
                                class_name="flex items-center gap-1.5 py-1",
                            ),
                        ),
                    ),
                    rx.el.p(
                        "Sem dados",
                        class_name="text-[11px] text-gray-400 py-2",
                    ),
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def period_concentration_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="h-4 w-4 text-amber-600"),
                rx.el.h3(
                    "Concentração temporal",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.p(
                f"Pico: {ResearchState.peak_century} ({ResearchState.peak_century_count} pessoas). Período: {ResearchState.timeline_span}.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-5",
        ),
        rx.cond(
            ResearchState.decade_distribution.length() > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.decade_distribution,
                    lambda item: rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                item["label"],
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-[11px] font-mono text-gray-300 w-12 shrink-0",
                                    "text-[11px] font-mono text-gray-700 w-12 shrink-0",
                                ),
                            ),
                            rx.el.div(
                                rx.el.div(
                                    class_name="h-2.5 rounded-full bg-amber-500 transition-all duration-500",
                                    style={
                                        "width": rx.cond(
                                            ResearchState.peak_century_count
                                            > 0,
                                            f"{item['count'] * 100 / ResearchState.peak_century_count}%",
                                            "0%",
                                        )
                                    },
                                ),
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "h-2.5 flex-1 rounded-full bg-gray-800 overflow-hidden",
                                    "h-2.5 flex-1 rounded-full bg-gray-100 overflow-hidden",
                                ),
                            ),
                            rx.el.span(
                                item["count"].to_string(),
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-[11px] font-mono font-bold text-amber-400 w-6 text-right shrink-0",
                                    "text-[11px] font-mono font-bold text-amber-600 w-6 text-right shrink-0",
                                ),
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="mb-1.5",
                    ),
                ),
                class_name="max-h-[280px] overflow-y-auto pr-1",
            ),
            rx.el.p(
                "Sem dados temporais.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm text-gray-400 text-center py-8",
                    "text-sm text-gray-500 text-center py-8",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def geography_summary_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("globe_x", class_name="h-4 w-4 text-blue-600"),
                rx.el.h3(
                    "Cobertura geográfica",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.p(
                "Indicadores de geocodificação e diversidade.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Geocodificação",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs font-medium text-gray-300",
                        "text-xs font-medium text-gray-700",
                    ),
                ),
                rx.el.span(
                    f"{ResearchState.geocoding_coverage}%",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs font-bold text-blue-400 font-mono",
                        "text-xs font-bold text-blue-600 font-mono",
                    ),
                ),
                class_name="flex items-center justify-between mb-1.5",
            ),
            rx.el.div(
                rx.el.div(
                    class_name="h-2 rounded-full bg-blue-500 transition-all duration-500",
                    style={"width": f"{ResearchState.geocoding_coverage}%"},
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "h-2 w-full rounded-full bg-gray-800 overflow-hidden",
                    "h-2 w-full rounded-full bg-gray-100 overflow-hidden",
                ),
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Com coordenadas",
                    class_name="text-[10px] font-semibold uppercase text-gray-400",
                ),
                rx.el.p(
                    ResearchState.total_with_coordinates.to_string(),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100",
                        "text-lg font-bold text-gray-900",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "p-3 rounded-lg border border-gray-800",
                    "p-3 rounded-lg border border-gray-100 bg-gray-50",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Totalmente mapeados",
                    class_name="text-[10px] font-semibold uppercase text-gray-400",
                ),
                rx.el.p(
                    ResearchState.total_fully_geocoded.to_string(),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100",
                        "text-lg font-bold text-gray-900",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "p-3 rounded-lg border border-gray-800",
                    "p-3 rounded-lg border border-gray-100 bg-gray-50",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Nacionalidades",
                    class_name="text-[10px] font-semibold uppercase text-gray-400",
                ),
                rx.el.p(
                    ResearchState.total_unique_nationalities.to_string(),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100",
                        "text-lg font-bold text-gray-900",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "p-3 rounded-lg border border-gray-800",
                    "p-3 rounded-lg border border-gray-100 bg-gray-50",
                ),
            ),
            class_name="grid grid-cols-3 gap-2",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def analytics_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            insight_card(
                "users",
                "Pessoas",
                ResearchState.total_people.to_string(),
                "Total composto",
                "bg-blue-50 text-blue-600",
                "bg-blue-950/40 text-blue-400",
            ),
            insight_card(
                "calendar",
                "Eventos",
                ResearchState.total_timeline_events.to_string(),
                "Datados",
                "bg-amber-50 text-amber-600",
                "bg-amber-950/40 text-amber-400",
            ),
            insight_card(
                "map-pin",
                "Locais",
                ResearchState.total_locations.to_string(),
                "Únicos",
                "bg-emerald-50 text-emerald-600",
                "bg-emerald-950/40 text-emerald-400",
            ),
            insight_card(
                "circle-check",
                "Completude",
                f"{ResearchState.avg_completeness}%",
                "Média geral",
                "bg-violet-50 text-violet-600",
                "bg-violet-950/40 text-violet-400",
            ),
            insight_card(
                "hourglass",
                "Vida média",
                f"{ResearchState.average_lifespan} anos",
                f"Pico: {ResearchState.peak_century}",
                "bg-rose-50 text-rose-600",
                "bg-rose-950/40 text-rose-400",
            ),
            insight_card(
                "globe_x",
                "Geocodificação",
                f"{ResearchState.geocoding_coverage}%",
                f"{ResearchState.total_unique_nationalities} países",
                "bg-cyan-50 text-cyan-600",
                "bg-cyan-950/40 text-cyan-400",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-6 gap-3 mb-4",
        ),
        rx.el.div(
            nationality_chart(),
            century_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            lifespan_chart(),
            mobility_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            period_concentration_chart(),
            top_places_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            missing_fields_chart(),
            geography_summary_panel(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            completeness_chart(),
            recent_searches_panel(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
        ),
    )