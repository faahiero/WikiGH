import reflex as rx
from app.states.research_state import ResearchState


def nav_link(icon: str, label: str, view: str) -> rx.Component:
    is_active = ResearchState.active_view == view
    return rx.el.button(
        rx.icon(icon, class_name="h-3.5 w-3.5"),
        rx.el.span(label),
        on_click=lambda: ResearchState.set_active_view(view),
        class_name=rx.cond(
            is_active,
            rx.cond(
                ResearchState.dark_mode,
                "flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium transition-colors bg-blue-950/40 text-blue-400 border border-blue-900 w-full text-left",
                "flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium transition-colors bg-blue-50 text-blue-700 border border-blue-100 w-full text-left",
            ),
            rx.cond(
                ResearchState.dark_mode,
                "flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium transition-colors text-gray-400 hover:bg-gray-800 hover:text-gray-200 border border-transparent w-full text-left",
                "flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium transition-colors text-gray-700 hover:bg-gray-100 hover:text-gray-900 border border-transparent w-full text-left",
            ),
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("globe", class_name="h-5 w-5 text-white"),
                    class_name="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p(
                        "Wikipédia",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-medium text-gray-300 leading-none",
                            "text-xs font-medium text-gray-500 leading-none",
                        ),
                    ),
                    rx.el.p(
                        "GeoHist",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-lg font-bold text-gray-100 leading-tight",
                            "text-lg font-bold text-gray-900 leading-tight",
                        ),
                    ),
                    class_name="flex flex-col",
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "flex items-center gap-3 px-4 py-3 border-b border-gray-800",
                    "flex items-center gap-3 px-4 py-3 border-b border-gray-200",
                ),
            ),
            rx.el.nav(
                rx.el.p(
                    "Painel",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-400",
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-500",
                    ),
                ),
                nav_link("layout-dashboard", "Dashboard", "dashboard"),
                rx.el.p(
                    "Pesquisa",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-400",
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-500",
                    ),
                ),
                nav_link("search", "Buscar artigo", "research"),
                rx.el.p(
                    "Visualizações",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-400",
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-500",
                    ),
                ),
                nav_link("map", "Mapa geográfico", "map"),
                nav_link("calendar-clock", "Linha do tempo", "timeline"),
                nav_link("chart-pie", "Análises", "analytics"),
                rx.el.p(
                    "Composição",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-400",
                        "px-3 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-gray-500",
                    ),
                ),
                nav_link("table", "Tabela completa", "table"),
                class_name="flex flex-col px-2 pb-3 flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "info",
                        class_name="h-3.5 w-3.5 text-blue-400 shrink-0 mt-0.5",
                    ),
                    rx.el.p(
                        "Wikipédia em português e Wikidata.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[11px] text-gray-400 leading-snug",
                            "text-[11px] text-gray-600 leading-snug",
                        ),
                    ),
                    class_name="flex gap-1.5",
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "mx-2 mb-2 p-2 rounded-lg bg-gray-900/60 border border-gray-800",
                    "mx-2 mb-2 p-2 rounded-lg bg-blue-50/60 border border-blue-100",
                ),
            ),
            class_name="flex flex-col h-full min-h-0",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "w-60 shrink-0 bg-gray-900 border-r border-gray-800 h-screen sticky top-0 hidden lg:flex flex-col",
            "w-60 shrink-0 bg-white border-r border-gray-200 h-screen sticky top-0 hidden lg:flex flex-col",
        ),
    )