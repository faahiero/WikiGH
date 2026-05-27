import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.states.research_state import ResearchState


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
                    rx.el.p(
                        point["name"],
                        class_name="text-sm font-bold text-gray-900",
                    ),
                    class_name="flex items-center gap-2",
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
                    point["date"],
                    class_name="text-[11px] text-gray-500 font-mono mt-0.5",
                ),
                class_name="min-w-[200px]",
            )
        ),
        rxe.map.tooltip(point["name"]),
        position=latlng(lat=point["lat"], lng=point["lng"]),
    )


def map_legend() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(class_name="h-2.5 w-2.5 rounded-full bg-emerald-500"),
            rx.el.span(
                "Nascimento",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-medium text-gray-100",
                    "text-xs font-medium text-gray-700",
                ),
            ),
            class_name="inline-flex items-center gap-1.5",
        ),
        rx.el.div(
            rx.el.span(class_name="h-2.5 w-2.5 rounded-full bg-red-500"),
            rx.el.span(
                "Falecimento",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-medium text-gray-100",
                    "text-xs font-medium text-gray-700",
                ),
            ),
            class_name="inline-flex items-center gap-1.5",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "absolute top-3 right-3 z-[1000] flex items-center gap-3 bg-gray-900/95 backdrop-blur-sm px-3 py-2 rounded-lg border border-gray-700",
            "absolute top-3 right-3 z-[1000] flex items-center gap-3 bg-white/95 backdrop-blur-sm px-3 py-2 rounded-lg border border-gray-200",
        ),
    )


def map_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Mapa geográfico",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100",
                        "text-lg font-bold text-gray-900",
                    ),
                ),
                rx.el.p(
                    "Visualização dos locais de nascimento e falecimento extraídos da Wikipédia.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 mt-0.5",
                        "text-sm text-gray-500 mt-0.5",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.span(
                    ResearchState.total_map_points.to_string(),
                    rx.el.span(
                        " pontos",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-400 ml-1",
                            "text-xs text-gray-500 ml-1",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-bold text-gray-100 px-3 py-1 rounded-full bg-gray-800 border border-gray-700",
                        "text-sm font-bold text-gray-900 px-3 py-1 rounded-full bg-gray-100 border border-gray-200",
                    ),
                ),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.cond(
            ResearchState.total_map_points > 0,
            rx.el.div(
                map_legend(),
                rxe.map(
                    rxe.map.tile_layer(
                        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
                        attribution="&copy; OpenStreetMap &copy; CARTO",
                    ),
                    rx.foreach(ResearchState.map_points, map_marker),
                    id="geo-map",
                    center=latlng(
                        lat=ResearchState.map_center_lat,
                        lng=ResearchState.map_center_lng,
                    ),
                    zoom=2.0,
                    height="600px",
                    width="100%",
                ),
                class_name="relative rounded-xl overflow-hidden border border-gray-200",
            ),
            rx.el.div(
                rx.icon("map", class_name="h-10 w-10 text-gray-500 mx-auto"),
                rx.el.p(
                    "Sem dados geográficos",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-semibold text-gray-100 text-center mt-3",
                        "text-base font-semibold text-gray-900 text-center mt-3",
                    ),
                ),
                rx.el.p(
                    "Pesquise pessoas com locais de nascimento ou falecimento para visualizar no mapa.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-1 max-w-md mx-auto",
                        "text-sm text-gray-500 text-center mt-1 max-w-md mx-auto",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "bg-gray-900 border border-dashed border-gray-700 rounded-xl py-16",
                    "bg-white border border-dashed border-gray-300 rounded-xl py-16",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )