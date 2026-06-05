import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.states.research_state import ResearchState


def connection_polyline(conn) -> rx.Component:
    return rxe.map.polyline(
        positions=[
            latlng(lat=conn["birth_lat"], lng=conn["birth_lng"]),
            latlng(lat=conn["death_lat"], lng=conn["death_lng"]),
        ],
        path_options=rxe.map.path_options(
            color=rx.cond(conn["is_selected"], "#2563eb", "#60a5fa"),
            weight=rx.cond(conn["is_selected"], 3, 2),
            opacity=rx.cond(conn["is_selected"], 0.9, 0.45),
            dash_array="6 8",
        ),
    )


def map_marker(point) -> rx.Component:
    return rxe.map.marker(
        rxe.map.popup(
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        point["image_url"] != "",
                        rx.el.img(
                            src=point["image_url"],
                            alt=point["name"],
                            class_name="h-10 w-10 rounded-full bg-gray-100 object-cover border border-gray-200 shrink-0",
                        ),
                        rx.el.img(
                            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={point['name']}",
                            class_name="h-10 w-10 rounded-full bg-gray-100 shrink-0",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            point["name"],
                            class_name="text-sm font-bold text-gray-900 leading-tight",
                        ),
                        rx.cond(
                            point["is_homonym"]
                            & (point["context_label"] != ""),
                            rx.el.div(
                                rx.icon(
                                    "split",
                                    class_name="h-2.5 w-2.5 text-amber-700",
                                ),
                                rx.el.span(
                                    point["context_label"],
                                    class_name="text-[10px] text-amber-800 truncate",
                                ),
                                class_name="inline-flex items-center gap-1 px-1.5 py-0.5 mt-0.5 rounded bg-amber-50 border border-amber-100 max-w-[180px]",
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            point["short_id"] != "",
                            rx.el.span(
                                point["short_id"],
                                class_name="text-[9px] font-mono text-blue-600 mt-0.5 block",
                            ),
                            rx.fragment(),
                        ),
                        class_name="min-w-0",
                    ),
                    class_name="flex items-start gap-2",
                ),
                rx.el.div(
                    rx.cond(
                        point["kind"] == "Nascimento",
                        rx.el.span(
                            "Nascimento",
                            class_name="inline-block text-[10px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-full",
                        ),
                        rx.el.span(
                            "Falecimento",
                            class_name="inline-block text-[10px] font-semibold text-red-700 bg-red-50 border border-red-100 px-2 py-0.5 rounded-full",
                        ),
                    ),
                    class_name="mt-2",
                ),
                rx.el.p(
                    point["place"],
                    class_name="text-xs text-gray-700 mt-2",
                ),
                rx.el.p(
                    point["date_br"],
                    title=point["date"],
                    class_name="text-[11px] text-gray-500 font-mono mt-0.5",
                ),
                class_name="min-w-[200px]",
            )
        ),
        rxe.map.tooltip(point["display_name"]),
        position=latlng(lat=point["lat"], lng=point["lng"]),
    )


def map_stats_overlay() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-3.5 w-3.5 text-blue-600"),
                rx.el.span(
                    "Pontos",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                class_name="flex items-center gap-1",
            ),
            rx.el.p(
                ResearchState.total_map_points.to_string(),
                class_name="text-xl font-bold text-gray-900 leading-none mt-1",
            ),
            class_name="px-3 py-2 border-r border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("users", class_name="h-3.5 w-3.5 text-emerald-600"),
                rx.el.span(
                    "Pessoas",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                class_name="flex items-center gap-1",
            ),
            rx.el.p(
                ResearchState.total_people.to_string(),
                class_name="text-xl font-bold text-gray-900 leading-none mt-1",
            ),
            class_name="px-3 py-2 border-r border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("globe", class_name="h-3.5 w-3.5 text-amber-600"),
                rx.el.span(
                    "Cobertura",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                class_name="flex items-center gap-1",
            ),
            rx.el.p(
                f"{ResearchState.geocoding_coverage}%",
                class_name="text-xl font-bold text-gray-900 leading-none mt-1",
            ),
            class_name="px-3 py-2",
        ),
        class_name="absolute top-3 left-3 z-[1000] flex items-center bg-white/95 backdrop-blur-md rounded-xl border border-gray-200 shadow-lg overflow-hidden",
    )


def map_top_places_overlay() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("trending-up", class_name="h-3.5 w-3.5 text-blue-600"),
            rx.el.span(
                "Locais mais frequentes",
                class_name="text-[10px] font-bold uppercase tracking-wider text-gray-700",
            ),
            class_name="flex items-center gap-1.5 mb-2 pb-2 border-b border-gray-100",
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
                            class_name="text-[11px] text-gray-700 truncate flex-1",
                        ),
                        rx.el.span(
                            item["count"].to_string(),
                            class_name="text-[10px] font-mono font-bold text-blue-600 shrink-0",
                        ),
                        class_name="flex items-center gap-1.5 py-1",
                    ),
                ),
                class_name="space-y-0",
            ),
            rx.el.p(
                "Sem dados",
                class_name="text-[11px] text-gray-400 text-center py-2",
            ),
        ),
        class_name="absolute bottom-3 left-3 z-[1000] w-56 bg-white/95 backdrop-blur-md rounded-xl border border-gray-200 shadow-lg p-3",
    )


def map_legend_floating() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("layers", class_name="h-3.5 w-3.5 text-gray-600"),
            rx.el.span(
                "Legenda",
                class_name="text-[10px] font-bold uppercase tracking-wider text-gray-700",
            ),
            class_name="flex items-center gap-1.5 mb-2 pb-2 border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.span(
                class_name="h-3 w-3 rounded-full bg-emerald-500 ring-2 ring-emerald-100"
            ),
            rx.el.span(
                "Nascimento",
                class_name="text-[11px] font-medium text-gray-700",
            ),
            class_name="flex items-center gap-2 py-1",
        ),
        rx.el.div(
            rx.el.span(
                class_name="h-3 w-3 rounded-full bg-red-500 ring-2 ring-red-100"
            ),
            rx.el.span(
                "Falecimento",
                class_name="text-[11px] font-medium text-gray-700",
            ),
            class_name="flex items-center gap-2 py-1",
        ),
        class_name="absolute top-3 right-3 z-[1000] bg-white/95 backdrop-blur-md rounded-xl border border-gray-200 shadow-lg p-3",
    )


def selected_location_overlay() -> rx.Component:
    return rx.cond(
        ResearchState.has_selected_person,
        rx.el.div(
            rx.el.div(
                rx.cond(
                    ResearchState.selected_person["image_url"] != "",
                    rx.el.img(
                        src=ResearchState.selected_person["image_url"],
                        alt=ResearchState.selected_person["name"],
                        class_name="h-12 w-12 rounded-full bg-gray-100 object-cover border-2 border-white shadow shrink-0",
                    ),
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/notionists/svg?seed={ResearchState.selected_person['name']}",
                        class_name="h-12 w-12 rounded-full bg-gray-100 border-2 border-white shadow shrink-0",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        ResearchState.selected_person["name"],
                        class_name="text-sm font-bold text-gray-900 truncate",
                    ),
                    rx.cond(
                        (ResearchState.selected_person["is_homonym"] == "true")
                        & (
                            ResearchState.selected_person["context_label"] != ""
                        ),
                        rx.el.div(
                            rx.icon(
                                "split",
                                class_name="h-2.5 w-2.5 text-amber-700 shrink-0 mt-0.5",
                            ),
                            rx.el.span(
                                ResearchState.selected_person["context_label"],
                                title=ResearchState.selected_person[
                                    "context_label"
                                ],
                                class_name="text-[10px] text-amber-800 break-words",
                            ),
                            title=ResearchState.selected_person[
                                "context_label"
                            ],
                            class_name="inline-flex items-start gap-1 px-1.5 py-0.5 mt-0.5 rounded bg-amber-50 border border-amber-100 max-w-full",
                        ),
                        rx.el.p(
                            ResearchState.selected_person["nationality"],
                            class_name="text-xs text-gray-500 truncate",
                        ),
                    ),
                    rx.cond(
                        ResearchState.selected_person["short_id"] != "",
                        rx.el.span(
                            ResearchState.selected_person["short_id"],
                            class_name="text-[10px] font-mono text-blue-600 mt-0.5 block",
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex-1 min-w-0",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-3.5 w-3.5"),
                    on_click=lambda: ResearchState.select_person(""),
                    class_name="text-gray-400 hover:text-gray-700 p-1 shrink-0",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("baby", class_name="h-3 w-3 text-emerald-600"),
                    rx.el.span(
                        ResearchState.selected_person["birth_place"],
                        class_name="text-[11px] text-gray-700 truncate",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.div(
                    rx.icon("flower-2", class_name="h-3 w-3 text-red-600"),
                    rx.el.span(
                        ResearchState.selected_person["death_place"],
                        class_name="text-[11px] text-gray-700 truncate",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                class_name="mt-2 pt-2 border-t border-gray-100 space-y-1",
            ),
            class_name="absolute bottom-3 right-3 z-[1000] w-72 bg-white/95 backdrop-blur-md rounded-xl border border-gray-200 shadow-lg p-3",
        ),
        rx.fragment(),
    )


def selectable_person_chip(person) -> rx.Component:
    return rx.el.button(
        rx.cond(
            person["image_url"] != "",
            rx.el.img(
                src=person["image_url"],
                alt=person["name"],
                class_name="h-6 w-6 rounded-full bg-gray-100 object-cover border border-gray-200 shrink-0",
            ),
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={person['name']}",
                class_name="h-6 w-6 rounded-full bg-gray-100 shrink-0",
            ),
        ),
        rx.el.span(
            person["name"],
            class_name="text-xs font-medium truncate max-w-[140px]",
        ),
        rx.cond(
            person["is_homonym"] & (person["context_label"] != ""),
            rx.el.span(
                person["context_label"],
                class_name=rx.cond(
                    ResearchState.selected_person_id == person["id"],
                    "text-[9px] font-medium px-1.5 py-0.5 rounded bg-white/20 text-white truncate max-w-[80px]",
                    rx.cond(
                        ResearchState.dark_mode,
                        "text-[9px] font-medium px-1.5 py-0.5 rounded bg-amber-950/60 border border-amber-900 text-amber-200 truncate max-w-[80px]",
                        "text-[9px] font-medium px-1.5 py-0.5 rounded bg-amber-50 border border-amber-100 text-amber-800 truncate max-w-[80px]",
                    ),
                ),
            ),
            rx.fragment(),
        ),
        on_click=rx.cond(
            ResearchState.selected_person_id == person["id"],
            ResearchState.select_person(""),
            ResearchState.select_person(person["id"]),
        ),
        class_name=rx.cond(
            ResearchState.selected_person_id == person["id"],
            "inline-flex items-center gap-1.5 px-2 py-1 rounded-full bg-blue-600 text-white border border-blue-700 shrink-0",
            rx.cond(
                ResearchState.dark_mode,
                "inline-flex items-center gap-1.5 px-2 py-1 rounded-full bg-gray-800 border border-gray-700 hover:border-blue-700 text-gray-300 shrink-0",
                "inline-flex items-center gap-1.5 px-2 py-1 rounded-full bg-white border border-gray-200 hover:border-blue-300 text-gray-700 shrink-0",
            ),
        ),
    )


def focus_banner() -> rx.Component:
    return rx.cond(
        ResearchState.is_map_focused,
        rx.el.div(
            rx.el.div(
                rx.icon("focus", class_name="h-3.5 w-3.5 text-blue-600"),
                rx.el.span(
                    "Foco ativo: ",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[11px] font-semibold text-gray-300",
                        "text-[11px] font-semibold text-gray-700",
                    ),
                ),
                rx.el.span(
                    ResearchState.selected_person["name"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[11px] font-bold text-blue-300",
                        "text-[11px] font-bold text-blue-700",
                    ),
                ),
                rx.cond(
                    (ResearchState.selected_person["is_homonym"] == "true")
                    & (ResearchState.selected_person["context_label"] != ""),
                    rx.el.span(
                        ResearchState.selected_person["context_label"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-medium px-1.5 py-0.5 rounded bg-amber-950/40 border border-amber-900 text-amber-200 truncate max-w-[140px]",
                            "text-[10px] font-medium px-1.5 py-0.5 rounded bg-amber-50 border border-amber-100 text-amber-800 truncate max-w-[140px]",
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name="flex items-center gap-1.5 min-w-0",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3 w-3"),
                rx.el.span("Mostrar todos"),
                on_click=lambda: ResearchState.select_person(""),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "inline-flex items-center gap-1 text-[11px] font-semibold text-blue-300 hover:text-blue-100 px-2 py-1 rounded shrink-0",
                    "inline-flex items-center gap-1 text-[11px] font-semibold text-blue-700 hover:text-blue-900 px-2 py-1 rounded shrink-0",
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "flex items-center justify-between gap-2 mb-3 px-3 py-2 rounded-lg bg-blue-950/30 border border-blue-900/60",
                "flex items-center justify-between gap-2 mb-3 px-3 py-2 rounded-lg bg-blue-50/70 border border-blue-200",
            ),
        ),
        rx.fragment(),
    )


def map_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("compass", class_name="h-4 w-4 text-white"),
                    class_name="h-9 w-9 rounded-lg bg-gradient-to-br from-emerald-500 to-emerald-700 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.span(
                        "Cartografia biográfica",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-bold tracking-widest text-emerald-400 uppercase",
                            "text-[10px] font-bold tracking-widest text-emerald-700 uppercase",
                        ),
                    ),
                    rx.el.h2(
                        "Mapa geográfico imersivo",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-lg font-bold text-gray-100 leading-tight",
                            "text-lg font-bold text-gray-900 leading-tight",
                        ),
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Total",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-semibold uppercase text-gray-400",
                            "text-[10px] font-semibold uppercase text-gray-500",
                        ),
                    ),
                    rx.el.p(
                        f"{ResearchState.total_map_points} pontos",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-bold text-gray-100",
                            "text-sm font-bold text-gray-900",
                        ),
                    ),
                    class_name="text-right",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex items-center justify-between mb-4 flex-wrap gap-3",
        ),
        rx.cond(
            ResearchState.people.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "user-round-search",
                        class_name="h-3.5 w-3.5 text-gray-400 shrink-0",
                    ),
                    rx.el.span(
                        "Foco rápido:",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-bold uppercase tracking-wider text-gray-400 shrink-0",
                            "text-[10px] font-bold uppercase tracking-wider text-gray-500 shrink-0",
                        ),
                    ),
                    rx.el.div(
                        rx.foreach(
                            ResearchState.people_enriched,
                            selectable_person_chip,
                        ),
                        class_name="flex items-center gap-1.5 overflow-x-auto pb-1",
                    ),
                    class_name="flex items-center gap-2 mb-3",
                ),
            ),
            rx.fragment(),
        ),
        focus_banner(),
        rx.cond(
            ResearchState.total_map_points > 0,
            rx.el.div(
                map_stats_overlay(),
                map_legend_floating(),
                map_top_places_overlay(),
                selected_location_overlay(),
                rxe.map(
                    rxe.map.tile_layer(
                        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
                        attribution="&copy; OpenStreetMap &copy; CARTO",
                    ),
                    rx.foreach(
                        ResearchState.map_connections, connection_polyline
                    ),
                    rx.foreach(ResearchState.map_points, map_marker),
                    id="geo-map",
                    center=latlng(
                        lat=ResearchState.map_center_lat,
                        lng=ResearchState.map_center_lng,
                    ),
                    zoom=2.0,
                    height="500px",
                    width="100%",
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "relative rounded-2xl overflow-hidden border-2 border-gray-800 shadow-xl",
                    "relative rounded-2xl overflow-hidden border-2 border-gray-200 shadow-xl",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("map", class_name="h-10 w-10 text-emerald-600"),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-20 w-20 rounded-full bg-emerald-950/40 border border-emerald-900 flex items-center justify-center mx-auto",
                        "h-20 w-20 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center mx-auto",
                    ),
                ),
                rx.el.p(
                    "Sem dados geográficos",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-semibold text-gray-100 text-center mt-4",
                        "text-base font-semibold text-gray-900 text-center mt-4",
                    ),
                ),
                rx.el.p(
                    "Pesquise pessoas com locais de nascimento ou falecimento para visualizar no mapa imersivo.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-1 max-w-md mx-auto",
                        "text-sm text-gray-500 text-center mt-1 max-w-md mx-auto",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "bg-gray-900 border border-dashed border-gray-700 rounded-2xl py-20",
                    "bg-white border border-dashed border-gray-300 rounded-2xl py-20",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-2xl p-5",
            "bg-white border border-gray-200 rounded-2xl p-5 shadow-sm",
        ),
    )