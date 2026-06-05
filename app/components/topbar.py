import reflex as rx
from app.states.research_state import ResearchState
from app.states.auth_state import AuthState


def topbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    rx.match(
                        ResearchState.active_view,
                        ("dashboard", "Painel"),
                        ("research", "Pesquisa"),
                        ("map", "Visualização"),
                        ("timeline", "Visualização"),
                        ("analytics", "Análises"),
                        ("table", "Composição"),
                        "Painel",
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[10px] font-bold tracking-widest text-blue-400 uppercase",
                        "text-[10px] font-bold tracking-widest text-blue-600 uppercase",
                    ),
                ),
                rx.el.h1(
                    rx.match(
                        ResearchState.active_view,
                        ("dashboard", "Dashboard"),
                        ("research", "Pesquisa GeoHist"),
                        ("map", "Mapa geográfico"),
                        ("timeline", "Linha do tempo"),
                        ("analytics", "Análises"),
                        ("table", "Tabela completa"),
                        "Dashboard",
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100 leading-tight",
                        "text-lg font-bold text-gray-900 leading-tight",
                    ),
                ),
                rx.el.p(
                    rx.match(
                        ResearchState.active_view,
                        (
                            "dashboard",
                            "Visão geral da composição biográfica e indicadores.",
                        ),
                        (
                            "research",
                            "Pesquisa baseada na Wikipédia.",
                        ),
                        (
                            "map",
                            "Distribuição espacial de nascimento e falecimento.",
                        ),
                        (
                            "timeline",
                            "Eventos cronológicos das pessoas pesquisadas.",
                        ),
                        (
                            "analytics",
                            "Estatísticas e completude.",
                        ),
                        (
                            "table",
                            "Composição completa com filtro e exportação.",
                        ),
                        "",
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 mt-0.5 hidden md:block",
                        "text-xs text-gray-500 mt-0.5 hidden md:block",
                    ),
                ),
            ),
            rx.el.div(
                rx.cond(
                    ResearchState.storage_ready,
                    rx.el.div(
                        rx.el.span(
                            class_name="h-1.5 w-1.5 rounded-full bg-emerald-500"
                        ),
                        rx.icon(
                            "database",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "h-3.5 w-3.5 text-emerald-400",
                                "h-3.5 w-3.5 text-emerald-700",
                            ),
                        ),
                        rx.el.span(
                            "Salvo localmente",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-semibold text-emerald-300",
                                "text-xs font-semibold text-emerald-800",
                            ),
                        ),
                        rx.el.span(
                            ResearchState.total_people.to_string(),
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-[10px] font-mono text-emerald-300 bg-gray-950 border border-emerald-900 px-1.5 py-0.5 rounded-full ml-1",
                                "text-[10px] font-mono text-emerald-700 bg-white border border-emerald-200 px-1.5 py-0.5 rounded-full ml-1",
                            ),
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "hidden md:inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-900/60",
                            "hidden md:inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-emerald-50 border border-emerald-100",
                        ),
                    ),
                    rx.el.div(
                        rx.el.span(
                            class_name="h-1.5 w-1.5 rounded-full bg-amber-500 animate-pulse"
                        ),
                        rx.icon(
                            "database-zap",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "h-3.5 w-3.5 text-amber-400",
                                "h-3.5 w-3.5 text-amber-700",
                            ),
                        ),
                        rx.el.span(
                            "Conectando…",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-semibold text-amber-300",
                                "text-xs font-semibold text-amber-800",
                            ),
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "hidden md:inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-950/40 border border-amber-900/60",
                            "hidden md:inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 border border-amber-100",
                        ),
                    ),
                ),
                rx.el.button(
                    rx.icon("refresh-cw", class_name="h-4 w-4"),
                    rx.el.span("Sincronizar"),
                    on_click=ResearchState.refresh_from_storage,
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "inline-flex items-center gap-1.5 text-xs font-medium text-gray-300 hover:text-blue-400 px-3 py-2 rounded-lg border border-gray-800 hover:border-blue-800 transition-colors",
                        "inline-flex items-center gap-1.5 text-xs font-medium text-gray-700 hover:text-blue-700 px-3 py-2 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors",
                    ),
                    aria_label="Recarregar dados do armazenamento local",
                ),
                rx.el.button(
                    rx.icon("circle-help", class_name="h-4 w-4"),
                    rx.el.span("Ajuda"),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "inline-flex items-center gap-1.5 text-xs font-medium text-gray-300 hover:text-blue-400 px-3 py-2 rounded-lg border border-gray-800 hover:border-blue-800 transition-colors",
                        "inline-flex items-center gap-1.5 text-xs font-medium text-gray-700 hover:text-blue-700 px-3 py-2 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AuthState.current_user["name"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-semibold text-gray-100 leading-none text-right",
                                "text-xs font-semibold text-gray-900 leading-none text-right",
                            ),
                        ),
                        rx.el.p(
                            AuthState.current_user["email"],
                            class_name="text-[10px] text-gray-400 leading-none mt-1 text-right",
                        ),
                        class_name="hidden sm:block",
                    ),
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.current_user['name']}",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-9 w-9 rounded-full bg-gray-800 border border-gray-700",
                            "h-9 w-9 rounded-full bg-gray-100 border border-gray-200",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        on_click=AuthState.logout,
                        title="Sair da conta",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "inline-flex items-center justify-center h-9 w-9 rounded-lg text-gray-300 hover:text-red-400 border border-gray-800 hover:border-red-900 hover:bg-red-950/30 transition-colors",
                            "inline-flex items-center justify-center h-9 w-9 rounded-lg text-gray-700 hover:text-red-700 border border-gray-200 hover:border-red-200 hover:bg-red-50 transition-colors",
                        ),
                        aria_label="Sair da conta",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between gap-3 px-6 py-3",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border-b border-gray-800 sticky top-0 z-10",
            "bg-white border-b border-gray-200 sticky top-0 z-10",
        ),
    )