import reflex as rx
import reflex_enterprise as rxe
from app.states.research_state import ResearchState
from app.states.auth_state import AuthState
from app.components.auth_view import auth_view
from app.components.sidebar import sidebar
from app.components.topbar import topbar
from app.components.summary_cards import summary_cards
from app.components.search_panel import search_panel
from app.components.people_list import people_list
from app.components.history_panel import history_panel
from app.components.map_view import map_view
from app.components.timeline_view import timeline_view
from app.components.analytics_view import analytics_view
from app.components.table_view import table_view
from app.components.dashboard_view import dashboard_view


def research_section() -> rx.Component:
    return rx.el.div(
        summary_cards(),
        rx.el.div(
            rx.el.div(
                search_panel(),
                people_list(),
                class_name="flex flex-col gap-6 lg:col-span-2",
            ),
            rx.el.div(
                history_panel(),
                class_name="flex flex-col gap-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6",
        ),
    )


def main_content() -> rx.Component:
    return rx.match(
        ResearchState.active_view,
        ("dashboard", dashboard_view()),
        ("research", research_section()),
        ("map", map_view()),
        ("timeline", timeline_view()),
        ("analytics", analytics_view()),
        ("table", table_view()),
        dashboard_view(),
    )


def landing_nav() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("globe", class_name="h-5 w-5 text-white"),
                    class_name="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center",
                ),
                rx.el.span(
                    "Wikipedia GeoHist",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xl font-extrabold tracking-tight text-gray-100",
                        "text-xl font-extrabold tracking-tight text-gray-900",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.a(
                    "Início",
                    href="#home",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-semibold text-gray-300 hover:text-blue-400 transition-colors hidden md:inline",
                        "text-sm font-semibold text-gray-600 hover:text-blue-600 transition-colors hidden md:inline",
                    ),
                ),
                rx.el.a(
                    "Funcionalidades",
                    href="#features",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-semibold text-gray-300 hover:text-blue-400 transition-colors hidden md:inline",
                        "text-sm font-semibold text-gray-600 hover:text-blue-600 transition-colors hidden md:inline",
                    ),
                ),
                rx.el.a(
                    "Como Funciona",
                    href="#workflow",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-semibold text-gray-300 hover:text-blue-400 transition-colors hidden md:inline",
                        "text-sm font-semibold text-gray-600 hover:text-blue-600 transition-colors hidden md:inline",
                    ),
                ),
                rx.el.button(
                    "Entrar",
                    on_click=[
                        AuthState.set_auth_mode("login"),
                        ResearchState.enter_app,
                    ],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-semibold text-gray-200 hover:text-blue-400 px-4 py-2 rounded-lg transition-all",
                        "text-sm font-semibold text-gray-700 hover:text-blue-700 px-4 py-2 rounded-lg transition-all",
                    ),
                ),
                rx.el.button(
                    "Acessar Plataforma",
                    on_click=ResearchState.enter_app,
                    class_name="text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg shadow-sm hover:shadow transition-all",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="max-w-7xl mx-auto flex items-center justify-between px-6 h-16",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "border-b border-gray-800 bg-gray-950/80 backdrop-blur-md sticky top-0 z-50 w-full",
            "border-b border-gray-200 bg-white/80 backdrop-blur-md sticky top-0 z-50 w-full",
        ),
    )


def landing_hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Exploração Histórica e Geográfica",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-950/40 text-blue-300 border border-blue-900 text-xs font-semibold mb-6",
                        "inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-100 text-xs font-semibold mb-6",
                    ),
                ),
                rx.el.h1(
                    "Descubra as conexões geográficas de biografias históricas",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-100 tracking-tight leading-none mb-6",
                        "text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 tracking-tight leading-none mb-6",
                    ),
                ),
                rx.el.p(
                    "Componha, analise e mapeie trajetórias de vida diretamente da Wikipédia em português. Transforme biografias complexas em mapas interativos e linhas do tempo estruturadas.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg text-gray-300 max-w-2xl mx-auto mb-10 leading-relaxed",
                        "text-lg text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed",
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        "Iniciar Pesquisa Gratuita",
                        on_click=ResearchState.enter_app,
                        class_name="inline-flex items-center gap-2 text-base font-semibold text-white bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all",
                    ),
                    rx.el.a(
                        "Saber mais",
                        href="#features",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "inline-flex items-center gap-1 text-base font-semibold text-gray-200 hover:text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition-all",
                            "inline-flex items-center gap-1 text-base font-semibold text-gray-700 hover:text-gray-900 px-6 py-3 rounded-lg hover:bg-gray-100 transition-all",
                        ),
                    ),
                    class_name="flex flex-col sm:flex-row gap-4 justify-center",
                ),
                class_name="text-center max-w-4xl mx-auto",
            ),
            class_name="py-20 md:py-28 px-6",
        ),
        id="home",
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gradient-to-b from-blue-950/30 via-gray-950 to-gray-950 border-b border-gray-800",
            "bg-gradient-to-b from-blue-50/50 via-white to-white border-b border-gray-100",
        ),
    )


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-blue-600"),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "h-12 w-12 rounded-xl bg-blue-950/40 flex items-center justify-center mb-5",
                "h-12 w-12 rounded-xl bg-blue-50 flex items-center justify-center mb-5",
            ),
        ),
        rx.el.h3(
            title,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-lg font-bold text-gray-100 mb-2",
                "text-lg font-bold text-gray-900 mb-2",
            ),
        ),
        rx.el.p(
            description,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-sm text-gray-400 leading-relaxed",
                "text-sm text-gray-600 leading-relaxed",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "p-6 bg-gray-900 border border-gray-800 rounded-xl hover:border-blue-800 transition-all",
            "p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:border-blue-300 hover:shadow-md transition-all",
        ),
    )


def landing_features() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Recursos Poderosos",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs font-bold uppercase tracking-wider text-blue-400",
                        "text-xs font-bold uppercase tracking-wider text-blue-600",
                    ),
                ),
                rx.el.h2(
                    "Tudo o que você precisa para analisar biografias",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-3xl font-bold text-gray-100 mt-2 mb-4",
                        "text-3xl font-bold text-gray-900 mt-2 mb-4",
                    ),
                ),
                rx.el.p(
                    "Nossas ferramentas de extração transformam texto não-estruturado em dados limpos e interativos.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 max-w-xl mx-auto",
                        "text-sm text-gray-500 max-w-xl mx-auto",
                    ),
                ),
                class_name="text-center mb-16",
            ),
            rx.el.div(
                feature_card(
                    "map-pin",
                    "Mapeamento Espacial",
                    "Geração automática de pontos geográficos para eventos de nascimento e morte das personalidades selecionadas.",
                ),
                feature_card(
                    "calendar-clock",
                    "Linha do Tempo",
                    "Organize cronologicamente a composição de múltiplos biografados para traçar paralelos históricos.",
                ),
                feature_card(
                    "chart-pie",
                    "Análises e Estatísticas",
                    "Distribuição por séculos de nascimento, nacionalidades predominantes e completude das fichas biográficas extraídas.",
                ),
                feature_card(
                    "database",
                    "Persistência Local",
                    "Seus dados e históricos de buscas ficam salvos com segurança diretamente no navegador via SQLite integrado.",
                ),
                feature_card(
                    "download",
                    "Exportação Facilitada",
                    "Exporte sua composição biográfica personalizada em formato CSV estruturado a qualquer momento para análises externas.",
                ),
                feature_card(
                    "search",
                    "Pesquisa em Tempo Real",
                    "Conexão direta com as APIs oficiais da Wikipédia em português e Wikidata para obtenção instantânea de dados.",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            class_name="max-w-7xl mx-auto px-6 py-20",
        ),
        id="features",
    )


def workflow_step(step: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            step,
            class_name="h-10 w-10 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-sm shadow-md mb-4",
        ),
        rx.el.h3(
            title,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-lg font-bold text-gray-100 mb-2",
                "text-lg font-bold text-gray-900 mb-2",
            ),
        ),
        rx.el.p(
            description,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-sm text-gray-400 leading-relaxed",
                "text-sm text-gray-600 leading-relaxed",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex flex-col items-start p-6 bg-gray-900 rounded-xl border border-gray-800 relative",
            "flex flex-col items-start p-6 bg-gray-50 rounded-xl border border-gray-100 relative",
        ),
    )


def landing_workflow() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Como Funciona",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs font-bold uppercase tracking-wider text-blue-400",
                        "text-xs font-bold uppercase tracking-wider text-blue-600",
                    ),
                ),
                rx.el.h2(
                    "Como usar o Wikipédia GeoHist",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-3xl font-bold text-gray-100 mt-2 mb-4",
                        "text-3xl font-bold text-gray-900 mt-2 mb-4",
                    ),
                ),
                rx.el.p(
                    "Siga estes três passos simples para iniciar sua primeira análise estruturada.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 max-w-xl mx-auto",
                        "text-sm text-gray-500 max-w-xl mx-auto",
                    ),
                ),
                class_name="text-center mb-16",
            ),
            rx.el.div(
                workflow_step(
                    "01",
                    "Busque Personalidades",
                    "Digite um termo ou nome em português. Nossa ferramenta consulta instantaneamente as APIs da Wikipédia e Wikidata para encontrar biografias compatíveis.",
                ),
                workflow_step(
                    "02",
                    "Confirme e Extraia",
                    "Revise a pré-visualização e com um clique confirme a extração estruturada de datas, locais, nacionalidades e dados espaciais.",
                ),
                workflow_step(
                    "03",
                    "Visualize e Analise",
                    "Acompanhe os resultados gerados automaticamente nos painéis de mapa dinâmico, cronogramas temporais e gráficos estatísticos unificados.",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
            ),
            class_name="max-w-7xl mx-auto px-6 py-20",
        ),
        id="workflow",
        class_name=rx.cond(
            ResearchState.dark_mode,
            "border-t border-b border-gray-800 bg-gray-950",
            "border-t border-b border-gray-100 bg-white",
        ),
    )


def landing_cta() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Pronto para iniciar sua composição histórica?",
                    class_name="text-3xl sm:text-4xl font-extrabold text-white mb-4 tracking-tight",
                ),
                rx.el.p(
                    "Nenhuma instalação é necessária. Experimente agora mesmo a nossa ferramenta inteligente de pesquisa e mapeamento biográfico.",
                    class_name="text-blue-100 max-w-2xl mx-auto mb-8 text-base sm:text-lg leading-relaxed",
                ),
                rx.el.button(
                    "Acessar Plataforma Agora",
                    on_click=ResearchState.enter_app,
                    class_name="inline-flex items-center gap-2 text-base font-bold text-blue-700 bg-white hover:bg-blue-50 px-8 py-4 rounded-xl shadow-lg transition-all hover:scale-105",
                ),
                class_name="text-center max-w-4xl mx-auto",
            ),
            class_name="max-w-7xl mx-auto px-6 py-16 sm:py-20",
        ),
        class_name="bg-blue-600 my-12 rounded-2xl mx-6 max-w-7xl lg:mx-auto shadow-xl overflow-hidden",
    )


def landing_footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("globe", class_name="h-4 w-4 text-white"),
                        class_name="h-7 w-7 rounded-lg bg-blue-600 flex items-center justify-center",
                    ),
                    rx.el.span(
                        "Wikipedia GeoHist",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-bold text-gray-100",
                            "text-sm font-bold text-gray-900",
                        ),
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "© 2025 Wikipedia GeoHist. Desenvolvido para fins de pesquisa educacional e histórica com dados abertos.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-500",
                        "text-xs text-gray-400",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-gray-800 pt-8",
                    "flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-gray-200 pt-8",
                ),
            ),
            class_name="max-w-7xl mx-auto px-6 py-12",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-950 border-t border-gray-800 w-full",
            "bg-gray-50 border-t border-gray-100 w-full",
        ),
    )


def public_landing_view() -> rx.Component:
    return rx.el.div(
        landing_nav(),
        landing_hero(),
        landing_features(),
        landing_workflow(),
        landing_cta(),
        landing_footer(),
        dark_mode_toggle_floating(),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-950 text-gray-100 w-full font-['Inter'] relative",
            "bg-gray-50 text-gray-900 w-full font-['Inter'] relative",
        ),
    )


def dark_mode_toggle_floating() -> rx.Component:
    return rx.el.button(
        rx.cond(
            ResearchState.dark_mode,
            rx.icon("sun", class_name="h-5 w-5 text-amber-400 animate-pulse"),
            rx.icon("moon", class_name="h-5 w-5 text-blue-600"),
        ),
        on_click=ResearchState.toggle_dark_mode,
        class_name=rx.cond(
            ResearchState.dark_mode,
            "fixed bottom-6 right-6 z-50 p-3 rounded-full bg-gray-900 border border-gray-800 shadow-lg hover:shadow-blue-900/50 hover:bg-gray-800 hover:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-110 flex items-center justify-center",
            "fixed bottom-6 right-6 z-50 p-3 rounded-full bg-white border border-gray-200 shadow-lg hover:shadow-blue-100/50 hover:bg-gray-50 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-110 flex items-center justify-center",
        ),
        aria_label="Alternar tema escuro/claro",
        title="Alternar tema escuro/claro",
    )


def authenticated_app() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            topbar(),
            rx.el.div(
                main_content(),
                class_name="px-6 lg:px-8 py-6",
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "flex-1 min-w-0 flex flex-col bg-gray-950",
                "flex-1 min-w-0 flex flex-col bg-gray-50",
            ),
        ),
        dark_mode_toggle_floating(),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex min-h-screen bg-gray-950 text-gray-100 relative",
            "flex min-h-screen bg-gray-50 text-gray-900 relative",
        ),
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.cond(
            ResearchState.landing_mode,
            public_landing_view(),
            rx.cond(
                AuthState.is_authenticated,
                authenticated_app(),
                auth_view(),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "font-['Inter'] bg-gray-950 min-h-screen text-gray-100",
            "font-['Inter'] bg-gray-50 min-h-screen text-gray-900",
        ),
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            cross_origin="",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    on_load=[ResearchState.load_data, AuthState.init_auth],
)