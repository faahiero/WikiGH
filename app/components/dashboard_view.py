import reflex as rx
from app.states.research_state import ResearchState
from app.states.auth_state import AuthState


def metric_card(
    icon: str, label: str, value, hint: str, accent: str, accent_dark: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-5 w-5"),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    f"h-10 w-10 rounded-lg flex items-center justify-center {accent_dark}",
                    f"h-10 w-10 rounded-lg flex items-center justify-center {accent}",
                ),
            ),
            rx.el.span(
                hint,
                class_name="text-[10px] font-semibold uppercase tracking-wider text-gray-400",
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.p(
            label,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-xs font-medium text-gray-400 mt-4",
                "text-xs font-medium text-gray-500 mt-4",
            ),
        ),
        rx.el.p(
            value,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-2xl font-bold text-gray-100 mt-1 tracking-tight",
                "text-2xl font-bold text-gray-900 mt-1 tracking-tight",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-blue-900 transition-colors",
            "bg-white border border-gray-200 rounded-xl p-5 hover:border-blue-200 transition-colors",
        ),
    )


def quick_action(
    icon: str, label: str, description: str, view: str, accent: str
) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5"),
            class_name=f"h-10 w-10 rounded-lg flex items-center justify-center {accent} shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                label,
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm font-semibold text-gray-100 text-left",
                    "text-sm font-semibold text-gray-900 text-left",
                ),
            ),
            rx.el.p(
                description,
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 text-left mt-0.5",
                    "text-xs text-gray-500 text-left mt-0.5",
                ),
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.icon("chevron-right", class_name="h-4 w-4 text-gray-400 shrink-0"),
        on_click=lambda: ResearchState.set_active_view(view),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex items-center gap-3 p-4 rounded-xl border border-gray-800 hover:border-blue-800 hover:bg-blue-950/30 transition-colors w-full",
            "flex items-center gap-3 p-4 rounded-xl border border-gray-200 hover:border-blue-300 hover:bg-blue-50/40 transition-colors w-full",
        ),
    )


def quick_actions_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Ações rápidas",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-base font-bold text-gray-100",
                    "text-base font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                "Acesse rapidamente as principais funcionalidades.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            quick_action(
                "search",
                "Nova pesquisa",
                "Buscar artigo na Wikipédia",
                "research",
                "bg-blue-50 text-blue-600",
            ),
            quick_action(
                "map",
                "Mapa geográfico",
                "Visualizar locais",
                "map",
                "bg-emerald-50 text-emerald-600",
            ),
            quick_action(
                "calendar-clock",
                "Linha do tempo",
                "Eventos cronológicos",
                "timeline",
                "bg-amber-50 text-amber-600",
            ),
            quick_action(
                "chart-pie",
                "Análises",
                "Estatísticas e gráficos",
                "analytics",
                "bg-violet-50 text-violet-600",
            ),
            quick_action(
                "table",
                "Tabela completa",
                "Composição e exportação",
                "table",
                "bg-rose-50 text-rose-600",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def latest_person_row(person) -> rx.Component:
    return rx.el.button(
        rx.cond(
            person["image_url"] != "",
            rx.el.img(
                src=person["image_url"],
                alt=person["name"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "h-10 w-10 rounded-full bg-gray-800 object-cover border border-gray-700 shrink-0",
                    "h-10 w-10 rounded-full bg-gray-100 object-cover border border-gray-200 shrink-0",
                ),
            ),
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={person['name']}",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "h-10 w-10 rounded-full bg-gray-800 shrink-0",
                    "h-10 w-10 rounded-full bg-gray-100 shrink-0",
                ),
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    person["name"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-semibold text-gray-100 text-left truncate",
                        "text-sm font-semibold text-gray-900 text-left truncate",
                    ),
                ),
                rx.cond(
                    person["is_homonym"],
                    rx.el.span(
                        rx.icon(
                            "split", class_name="h-2.5 w-2.5 text-amber-600"
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "inline-flex items-center justify-center h-4 w-4 rounded-full bg-amber-950/40 border border-amber-900 shrink-0",
                            "inline-flex items-center justify-center h-4 w-4 rounded-full bg-amber-50 border border-amber-100 shrink-0",
                        ),
                        title="Personalidade homônima",
                    ),
                    rx.fragment(),
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.cond(
                person["is_homonym"] & (person["context_label"] != ""),
                rx.el.p(
                    person["context_label"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[10px] text-amber-300 italic truncate text-left",
                        "text-[10px] text-amber-700 italic truncate text-left",
                    ),
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.span(
                    person["nationality"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400",
                        "text-xs text-gray-500",
                    ),
                ),
                rx.el.span("•", class_name="text-xs text-gray-300"),
                rx.el.span(
                    person["birth_date_br"],
                    title=person["birth_date"],
                    class_name="text-xs text-gray-400 font-mono",
                ),
                class_name="flex items-center gap-1.5 mt-0.5",
            ),
            class_name="flex-1 min-w-0 text-left",
        ),
        rx.cond(
            person["completeness"] == 100,
            rx.el.span(
                f"{person['completeness']}%",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold text-emerald-300 bg-emerald-950/40 border border-emerald-900 px-2 py-0.5 rounded-full shrink-0",
                    "text-[10px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-full shrink-0",
                ),
            ),
            rx.el.span(
                f"{person['completeness']}%",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold text-amber-300 bg-amber-950/40 border border-amber-900 px-2 py-0.5 rounded-full shrink-0",
                    "text-[10px] font-semibold text-amber-700 bg-amber-50 border border-amber-100 px-2 py-0.5 rounded-full shrink-0",
                ),
            ),
        ),
        on_click=[
            ResearchState.select_person(person["id"]),
            ResearchState.set_active_view("timeline"),
        ],
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex items-center gap-3 p-3 rounded-lg border border-gray-800 hover:border-blue-800 hover:bg-blue-950/30 transition-colors w-full",
            "flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50/40 transition-colors w-full",
        ),
    )


def latest_people_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Últimas pessoas",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                rx.el.p(
                    "Registros recentes da composição.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 mt-0.5",
                        "text-xs text-gray-500 mt-0.5",
                    ),
                ),
            ),
            rx.el.button(
                "Ver todas",
                rx.icon("arrow-right", class_name="h-3 w-3"),
                on_click=lambda: ResearchState.set_active_view("table"),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "inline-flex items-center gap-1 text-xs font-semibold text-blue-400 hover:text-blue-300",
                    "inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-700",
                ),
            ),
            class_name="flex items-start justify-between mb-4",
        ),
        rx.cond(
            ResearchState.total_people > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.dashboard_latest_people, latest_person_row
                ),
                class_name="flex flex-col gap-2",
            ),
            rx.el.div(
                rx.icon("users", class_name="h-7 w-7 text-gray-500 mx-auto"),
                rx.el.p(
                    "Nenhuma pessoa pesquisada ainda.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-2",
                        "text-sm text-gray-500 text-center mt-2",
                    ),
                ),
                rx.el.button(
                    "Iniciar pesquisa",
                    on_click=lambda: ResearchState.set_active_view("research"),
                    class_name="inline-flex items-center gap-1 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 px-3 py-1.5 rounded-lg mx-auto mt-3",
                ),
                class_name="py-8 flex flex-col items-center",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def recent_search_row(entry) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search", class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0"
            ),
            rx.el.div(
                rx.el.p(
                    entry["term"],
                    title=entry["term"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-medium text-gray-100 truncate",
                        "text-sm font-medium text-gray-900 truncate",
                    ),
                ),
                rx.el.p(
                    f"→ {entry['title']}",
                    title=entry["title"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 truncate",
                        "text-xs text-gray-500 truncate",
                    ),
                ),
                rx.cond(
                    entry["context_label"] != "",
                    rx.el.p(
                        entry["context_label"],
                        title=entry["context_label"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] text-amber-300 italic truncate",
                            "text-[10px] text-amber-700 italic truncate",
                        ),
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    entry["short_id"] != "",
                    rx.el.span(
                        entry["short_id"],
                        title=f"Wikidata: {entry['short_id']}",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "inline-block text-[9px] font-mono text-blue-300 bg-blue-950/40 border border-blue-900 px-1.5 py-0.5 rounded mt-0.5",
                            "inline-block text-[9px] font-mono text-blue-700 bg-blue-50 border border-blue-100 px-1.5 py-0.5 rounded mt-0.5",
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-start gap-2 min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.span(
                entry["status"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold text-blue-300 bg-blue-950/40 border border-blue-900 px-2 py-0.5 rounded-full",
                    "text-[10px] font-semibold text-blue-700 bg-blue-50 border border-blue-100 px-2 py-0.5 rounded-full",
                ),
            ),
            rx.el.span(
                entry["timestamp_br"],
                title=entry["timestamp"],
                class_name="text-[10px] text-gray-400 font-mono mt-0.5",
            ),
            class_name="text-right shrink-0 flex flex-col items-end",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex items-start justify-between gap-3 py-2.5 border-b border-gray-800 last:border-0",
            "flex items-start justify-between gap-3 py-2.5 border-b border-gray-100 last:border-0",
        ),
    )


def recent_searches_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
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
                    "Histórico de buscas nesta sessão.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 mt-0.5",
                        "text-xs text-gray-500 mt-0.5",
                    ),
                ),
            ),
            rx.el.span(
                ResearchState.total_history.to_string(),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-bold text-gray-100 px-2 py-0.5 rounded-full bg-gray-800 border border-gray-700",
                    "text-xs font-bold text-gray-900 px-2 py-0.5 rounded-full bg-gray-100 border border-gray-200",
                ),
            ),
            class_name="flex items-start justify-between mb-3",
        ),
        rx.cond(
            ResearchState.total_history > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.dashboard_recent_history, recent_search_row
                ),
            ),
            rx.el.div(
                rx.icon("history", class_name="h-7 w-7 text-gray-500 mx-auto"),
                rx.el.p(
                    "Sem buscas recentes.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-2",
                        "text-sm text-gray-500 text-center mt-2",
                    ),
                ),
                class_name="py-8",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def data_quality_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Qualidade dos dados",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-base font-bold text-gray-100",
                    "text-base font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                "Indicadores de completude da composição.",
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
                rx.el.div(
                    rx.el.span(
                        "Completude",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-medium text-gray-300",
                            "text-xs font-medium text-gray-700",
                        ),
                    ),
                    rx.el.span(
                        f"{ResearchState.avg_completeness}%",
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
                        class_name="h-2 rounded-full bg-blue-600 transition-all duration-500",
                        style={"width": f"{ResearchState.avg_completeness}%"},
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-2 w-full rounded-full bg-gray-800 overflow-hidden",
                        "h-2 w-full rounded-full bg-gray-100 overflow-hidden",
                    ),
                ),
                class_name="mb-4",
            ),
            rx.foreach(
                ResearchState.completeness_buckets,
                lambda item: rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            item["label"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-medium text-gray-300",
                                "text-xs font-medium text-gray-700",
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
                            class_name="h-1.5 rounded-full bg-emerald-500",
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
                            "h-1.5 rounded-full bg-gray-800 w-full overflow-hidden",
                            "h-1.5 rounded-full bg-gray-100 w-full overflow-hidden",
                        ),
                    ),
                    class_name="mb-2.5",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def top_nationalities_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Top nacionalidades",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-base font-bold text-gray-100",
                    "text-base font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                "Distribuição compacta por país.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 mt-0.5",
                    "text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="mb-4",
        ),
        rx.cond(
            ResearchState.nationality_distribution.length() > 0,
            rx.el.div(
                rx.foreach(
                    ResearchState.dashboard_top_nationalities,
                    lambda item: rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                item["label"],
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-xs font-semibold text-gray-200 truncate",
                                    "text-xs font-semibold text-gray-700 truncate",
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
                                    )
                                },
                            ),
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "h-2 w-full rounded-full bg-gray-800 overflow-hidden",
                                "h-2 w-full rounded-full bg-gray-100 overflow-hidden",
                            ),
                        ),
                        class_name="mb-3",
                    ),
                ),
            ),
            rx.el.div(
                rx.icon("globe", class_name="h-7 w-7 text-gray-500 mx-auto"),
                rx.el.p(
                    "Sem dados ainda.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-2",
                        "text-sm text-gray-500 text-center mt-2",
                    ),
                ),
                class_name="py-8",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def storage_status_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    ResearchState.storage_ready,
                    rx.icon(
                        "database",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-5 w-5 text-emerald-400",
                            "h-5 w-5 text-emerald-600",
                        ),
                    ),
                    rx.icon(
                        "database-zap",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-5 w-5 text-amber-400",
                            "h-5 w-5 text-amber-600",
                        ),
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.storage_ready,
                    rx.cond(
                        ResearchState.dark_mode,
                        "h-10 w-10 rounded-lg bg-emerald-950/40 flex items-center justify-center shrink-0",
                        "h-10 w-10 rounded-lg bg-emerald-50 flex items-center justify-center shrink-0",
                    ),
                    rx.cond(
                        ResearchState.dark_mode,
                        "h-10 w-10 rounded-lg bg-amber-950/40 flex items-center justify-center shrink-0",
                        "h-10 w-10 rounded-lg bg-amber-50 flex items-center justify-center shrink-0",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.p(
                    rx.cond(
                        ResearchState.storage_ready,
                        "Armazenamento ativo",
                        "Conectando ao armazenamento...",
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-bold text-gray-100",
                        "text-sm font-bold text-gray-900",
                    ),
                ),
                rx.el.p(
                    rx.cond(
                        ResearchState.storage_ready,
                        f"SQLite local • {ResearchState.total_people} pessoa(s) • {ResearchState.total_history} busca(s)",
                        "Aguarde enquanto inicializamos o banco SQLite local.",
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 mt-0.5",
                        "text-xs text-gray-600 mt-0.5",
                    ),
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
                rx.el.span("Sincronizar"),
                on_click=ResearchState.refresh_from_storage,
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-300 hover:text-blue-400 px-3 py-2 rounded-lg border border-gray-800 hover:border-blue-800 transition-colors shrink-0",
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-700 hover:text-blue-700 px-3 py-2 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors shrink-0",
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-4",
            "bg-white border border-gray-200 rounded-xl p-4",
        ),
    )


def welcome_banner() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Centro de comando",
                    class_name="text-[10px] font-bold tracking-widest text-blue-100 uppercase",
                ),
                rx.el.h2(
                    f"Bem-vindo(a), {AuthState.current_user['name']}",
                    class_name="text-2xl font-bold text-white mt-1 tracking-tight",
                ),
                rx.el.p(
                    f"{ResearchState.total_people} pessoa(s) compostas • {ResearchState.total_locations} locais • Período {ResearchState.timeline_span}",
                    class_name="text-sm text-blue-100 mt-1",
                ),
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("search", class_name="h-4 w-4"),
                    rx.el.span("Nova pesquisa"),
                    on_click=lambda: ResearchState.set_active_view("research"),
                    class_name="inline-flex items-center gap-2 text-sm font-bold text-blue-700 bg-white hover:bg-blue-50 px-4 py-2.5 rounded-lg shadow-sm transition-all hover:scale-105 shrink-0",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4"),
                    rx.el.span("Exportar"),
                    on_click=ResearchState.export_csv_with_feedback,
                    class_name="inline-flex items-center gap-2 text-sm font-semibold text-white bg-blue-500/40 hover:bg-blue-500/60 border border-white/20 px-4 py-2.5 rounded-lg transition-all shrink-0",
                ),
                class_name="flex items-center gap-2 flex-wrap",
            ),
            class_name="flex items-start justify-between gap-4 flex-wrap",
        ),
        class_name="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl p-6 mb-6 shadow-sm",
    )


def next_action_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("compass", class_name="h-4 w-4 text-blue-600"),
                rx.el.h3(
                    "Próxima ação sugerida",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="mb-3",
        ),
        rx.cond(
            ResearchState.total_people == 0,
            rx.el.button(
                rx.el.div(
                    rx.icon("search", class_name="h-5 w-5 text-blue-600"),
                    class_name="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        "Faça sua primeira pesquisa",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-bold text-gray-100 text-left",
                            "text-sm font-bold text-gray-900 text-left",
                        ),
                    ),
                    rx.el.p(
                        "Procure uma personalidade na Wikipédia para iniciar sua composição.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-400 text-left",
                            "text-xs text-gray-600 text-left",
                        ),
                    ),
                    class_name="flex-1 min-w-0",
                ),
                rx.icon(
                    "arrow-right", class_name="h-4 w-4 text-blue-600 shrink-0"
                ),
                on_click=lambda: ResearchState.set_active_view("research"),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "flex items-center gap-3 p-4 rounded-xl border border-blue-900 bg-blue-950/30 hover:bg-blue-950/50 transition-colors w-full",
                    "flex items-center gap-3 p-4 rounded-xl border border-blue-200 bg-blue-50/60 hover:bg-blue-100/60 transition-colors w-full",
                ),
            ),
            rx.cond(
                ResearchState.avg_completeness < 80,
                rx.el.button(
                    rx.el.div(
                        rx.icon(
                            "circle-check", class_name="h-5 w-5 text-amber-600"
                        ),
                        class_name="h-10 w-10 rounded-lg bg-amber-50 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Revise dados incompletos",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-sm font-bold text-gray-100 text-left",
                                "text-sm font-bold text-gray-900 text-left",
                            ),
                        ),
                        rx.el.p(
                            f"Completude média {ResearchState.avg_completeness}% — analise campos ausentes nas Análises.",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs text-gray-400 text-left",
                                "text-xs text-gray-600 text-left",
                            ),
                        ),
                        class_name="flex-1 min-w-0",
                    ),
                    rx.icon(
                        "arrow-right",
                        class_name="h-4 w-4 text-amber-600 shrink-0",
                    ),
                    on_click=lambda: ResearchState.set_active_view("analytics"),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "flex items-center gap-3 p-4 rounded-xl border border-amber-900 bg-amber-950/30 hover:bg-amber-950/50 transition-colors w-full",
                        "flex items-center gap-3 p-4 rounded-xl border border-amber-200 bg-amber-50/60 hover:bg-amber-100/60 transition-colors w-full",
                    ),
                ),
                rx.el.button(
                    rx.el.div(
                        rx.icon("map", class_name="h-5 w-5 text-emerald-600"),
                        class_name="h-10 w-10 rounded-lg bg-emerald-50 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Explore o mapa geográfico",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-sm font-bold text-gray-100 text-left",
                                "text-sm font-bold text-gray-900 text-left",
                            ),
                        ),
                        rx.el.p(
                            f"{ResearchState.total_with_coordinates} registro(s) geocodificado(s) prontos para visualização.",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs text-gray-400 text-left",
                                "text-xs text-gray-600 text-left",
                            ),
                        ),
                        class_name="flex-1 min-w-0",
                    ),
                    rx.icon(
                        "arrow-right",
                        class_name="h-4 w-4 text-emerald-600 shrink-0",
                    ),
                    on_click=lambda: ResearchState.set_active_view("map"),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "flex items-center gap-3 p-4 rounded-xl border border-emerald-900 bg-emerald-950/30 hover:bg-emerald-950/50 transition-colors w-full",
                        "flex items-center gap-3 p-4 rounded-xl border border-emerald-200 bg-emerald-50/60 hover:bg-emerald-100/60 transition-colors w-full",
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


def progress_status_block() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("gauge", class_name="h-4 w-4 text-blue-600"),
                rx.el.h3(
                    "Status da composição",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-base font-bold text-gray-100",
                        "text-base font-bold text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Completude",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-medium text-gray-300",
                            "text-xs font-medium text-gray-700",
                        ),
                    ),
                    rx.el.span(
                        f"{ResearchState.avg_completeness}%",
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
                        class_name="h-2 rounded-full bg-blue-600 transition-all duration-500",
                        style={"width": f"{ResearchState.avg_completeness}%"},
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-2 w-full rounded-full bg-gray-800 overflow-hidden",
                        "h-2 w-full rounded-full bg-gray-100 overflow-hidden",
                    ),
                ),
                class_name="mb-3",
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
                            "text-xs font-bold text-emerald-400 font-mono",
                            "text-xs font-bold text-emerald-600 font-mono",
                        ),
                    ),
                    class_name="flex items-center justify-between mb-1.5",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-2 rounded-full bg-emerald-600 transition-all duration-500",
                        style={"width": f"{ResearchState.geocoding_coverage}%"},
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-2 w-full rounded-full bg-gray-800 overflow-hidden",
                        "h-2 w-full rounded-full bg-gray-100 overflow-hidden",
                    ),
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Mais longevo(a)",
                        class_name="text-[10px] font-semibold uppercase text-gray-400",
                    ),
                    rx.el.p(
                        ResearchState.oldest_person_name,
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-bold text-gray-100 truncate",
                            "text-xs font-bold text-gray-900 truncate",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "p-2.5 rounded-lg border border-gray-800",
                        "p-2.5 rounded-lg border border-gray-100 bg-gray-50",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Pico histórico",
                        class_name="text-[10px] font-semibold uppercase text-gray-400",
                    ),
                    rx.el.p(
                        ResearchState.peak_century,
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-bold text-gray-100 truncate",
                            "text-xs font-bold text-gray-900 truncate",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "p-2.5 rounded-lg border border-gray-800",
                        "p-2.5 rounded-lg border border-gray-100 bg-gray-50",
                    ),
                ),
                class_name="grid grid-cols-2 gap-2",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        welcome_banner(),
        rx.el.div(
            metric_card(
                "users",
                "Pessoas pesquisadas",
                ResearchState.total_people,
                "Total",
                "bg-blue-50 text-blue-600",
                "bg-blue-950/40 text-blue-400",
            ),
            metric_card(
                "map-pin",
                "Locais únicos",
                ResearchState.total_locations,
                "Geo",
                "bg-emerald-50 text-emerald-600",
                "bg-emerald-950/40 text-emerald-400",
            ),
            metric_card(
                "calendar-clock",
                "Período histórico",
                ResearchState.timeline_span,
                "Anos",
                "bg-amber-50 text-amber-600",
                "bg-amber-950/40 text-amber-400",
            ),
            metric_card(
                "circle-check",
                "Completude média",
                f"{ResearchState.avg_completeness}%",
                "Qualidade",
                "bg-violet-50 text-violet-600",
                "bg-violet-950/40 text-violet-400",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        rx.el.div(storage_status_card(), class_name="mb-6"),
        rx.el.div(
            next_action_panel(),
            progress_status_block(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                quick_actions_panel(),
                latest_people_panel(),
                class_name="flex flex-col gap-6 lg:col-span-2",
            ),
            rx.el.div(
                recent_searches_panel(),
                data_quality_panel(),
                top_nationalities_panel(),
                class_name="flex flex-col gap-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
    )