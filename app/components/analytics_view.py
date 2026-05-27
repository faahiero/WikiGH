import reflex as rx
from app.states.research_state import ResearchState


def stat_card(
    label: str, value, hint: str, icon: str, accent: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4"),
                class_name=f"h-9 w-9 rounded-lg flex items-center justify-center {accent}",
            ),
            rx.el.span(
                hint,
                class_name="text-[10px] font-semibold uppercase text-gray-400",
            ),
            class_name="flex items-start justify-between",
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
                "text-2xl font-bold text-gray-100 mt-0.5",
                "text-2xl font-bold text-gray-900 mt-0.5",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-4",
            "bg-white border border-gray-200 rounded-xl p-4",
        ),
    )


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
                    ResearchState.history,
                    lambda h: rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "search", class_name="h-3.5 w-3.5 text-gray-400"
                            ),
                            rx.el.div(
                                rx.el.p(
                                    h["term"],
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-sm font-medium text-gray-100",
                                        "text-sm font-medium text-gray-900",
                                    ),
                                ),
                                rx.el.p(
                                    f"→ {h['title']}",
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-xs text-gray-400",
                                        "text-xs text-gray-500",
                                    ),
                                ),
                            ),
                            class_name="flex items-start gap-2",
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
                                h["timestamp"],
                                class_name="text-[10px] text-gray-400 font-mono mt-1 block",
                            ),
                            class_name="text-right",
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "flex items-center justify-between py-2.5 border-b border-gray-800 last:border-0",
                            "flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0",
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


def analytics_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card(
                "Pessoas",
                ResearchState.total_people.to_string(),
                "Total",
                "users",
                "bg-blue-50 text-blue-600",
            ),
            stat_card(
                "Eventos",
                ResearchState.total_timeline_events.to_string(),
                "Datados",
                "calendar",
                "bg-amber-50 text-amber-600",
            ),
            stat_card(
                "Locais",
                ResearchState.total_locations.to_string(),
                "Únicos",
                "map-pin",
                "bg-emerald-50 text-emerald-600",
            ),
            stat_card(
                "Completude",
                f"{ResearchState.avg_completeness}%",
                "Média",
                "circle-check",
                "bg-violet-50 text-violet-600",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-4",
        ),
        rx.el.div(
            nationality_chart(),
            century_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4",
        ),
        rx.el.div(
            completeness_chart(),
            recent_searches_panel(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
        ),
    )