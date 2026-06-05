import reflex as rx
from app.states.research_state import ResearchState


def workbench_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("book-open-text", class_name="h-4 w-4 text-white"),
                class_name="h-9 w-9 rounded-lg bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.span(
                    "Workbench Editorial",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[10px] font-bold tracking-widest text-blue-400 uppercase",
                        "text-[10px] font-bold tracking-widest text-blue-600 uppercase",
                    ),
                ),
                rx.el.h2(
                    "Curadoria de biografias",
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
            rx.el.span(
                rx.el.span(
                    class_name="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"
                ),
                rx.el.span(
                    "pt.wikipedia.org",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs font-medium text-gray-200",
                        "text-xs font-medium text-gray-700",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-gray-800 border border-gray-700",
                    "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white border border-gray-200",
                ),
            ),
            class_name="flex items-center gap-2",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex items-center justify-between gap-4 pb-4 mb-5 border-b border-dashed border-gray-800",
            "flex items-center justify-between gap-4 pb-4 mb-5 border-b border-dashed border-gray-200",
        ),
    )


def search_result_item(item) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "file-text",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-4 w-4 text-blue-400",
                        "h-4 w-4 text-blue-600",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "h-9 w-9 rounded-lg bg-blue-950/40 flex items-center justify-center shrink-0",
                    "h-9 w-9 rounded-lg bg-blue-50 flex items-center justify-center shrink-0",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    item["title"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-semibold text-gray-100 text-left",
                        "text-sm font-semibold text-gray-900 text-left",
                    ),
                ),
                rx.el.p(
                    item["snippet"],
                    title=item["snippet"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 mt-1 text-left line-clamp-3 break-words leading-relaxed",
                        "text-xs text-gray-500 mt-1 text-left line-clamp-3 break-words leading-relaxed",
                    ),
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.icon(
                "chevron-right",
                class_name="h-4 w-4 text-gray-400 shrink-0",
            ),
            class_name="flex items-start gap-3 w-full",
        ),
        on_click=lambda: ResearchState.select_article(item["title"]),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "w-full text-left p-3 rounded-lg border border-gray-800 hover:border-blue-800 hover:bg-blue-950/30 transition-colors",
            "w-full text-left p-3 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50/40 transition-colors",
        ),
    )


def suggestion_button(label: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: ResearchState.run_suggested_search(label),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "text-xs px-2.5 py-1 rounded-full bg-gray-800 text-gray-300 hover:bg-blue-950/60 hover:text-blue-300 transition-colors",
            "text-xs px-2.5 py-1 rounded-full bg-gray-100 text-gray-700 hover:bg-blue-100 hover:text-blue-700 transition-colors",
        ),
    )


def empty_state() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "h-6 w-6 text-blue-400",
                    "h-6 w-6 text-blue-600",
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "h-14 w-14 rounded-full bg-blue-950/40 flex items-center justify-center mx-auto",
                "h-14 w-14 rounded-full bg-blue-50 flex items-center justify-center mx-auto",
            ),
        ),
        rx.el.p(
            "Comece sua pesquisa",
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-base font-semibold text-gray-100 mt-4 text-center",
                "text-base font-semibold text-gray-900 mt-4 text-center",
            ),
        ),
        rx.el.p(
            "Digite o nome de uma pessoa, lugar ou tópico em português. Os resultados serão buscados na Wikipédia.",
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-sm text-gray-400 mt-1 text-center max-w-sm mx-auto",
                "text-sm text-gray-500 mt-1 text-center max-w-sm mx-auto",
            ),
        ),
        class_name="py-10",
    )


def loading_skeleton() -> rx.Component:
    skel_cls = rx.cond(
        ResearchState.dark_mode,
        "h-14 rounded-lg bg-gray-800 animate-pulse",
        "h-14 rounded-lg bg-gray-100 animate-pulse",
    )
    return rx.el.div(
        rx.el.div(class_name=skel_cls),
        rx.el.div(class_name=skel_cls),
        rx.el.div(class_name=skel_cls),
        class_name="space-y-2",
    )


def preview_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    ResearchState.selected_preview["image_url"] != "",
                    rx.el.img(
                        src=ResearchState.selected_preview["image_url"],
                        alt=ResearchState.selected_preview["title"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-16 w-16 rounded-lg bg-gray-800 object-cover border border-gray-700 shrink-0",
                            "h-16 w-16 rounded-lg bg-gray-100 object-cover border border-gray-200 shrink-0",
                        ),
                    ),
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/notionists/svg?seed={ResearchState.selected_preview['title']}",
                        alt=ResearchState.selected_preview["title"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-16 w-16 rounded-lg bg-gray-800 border border-gray-700 shrink-0",
                            "h-16 w-16 rounded-lg bg-gray-100 border border-gray-200 shrink-0",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.span(
                        "Pré-visualização",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs font-semibold uppercase tracking-wider text-blue-400",
                            "text-xs font-semibold uppercase tracking-wider text-blue-600",
                        ),
                    ),
                    rx.el.h3(
                        ResearchState.selected_preview["title"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xl font-bold text-gray-100 mt-1",
                            "text-xl font-bold text-gray-900 mt-1",
                        ),
                    ),
                ),
                class_name="flex items-start gap-3",
            ),
            rx.el.div(
                rx.cond(
                    ResearchState.selected_preview["wikidata_id"]
                    .to_string()
                    .startswith("Q"),
                    rx.el.a(
                        rx.el.span(
                            "Wikidata",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-[10px] font-semibold uppercase text-gray-400",
                                "text-[10px] font-semibold uppercase text-gray-500",
                            ),
                        ),
                        rx.el.span(
                            ResearchState.selected_preview["wikidata_id"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-mono text-blue-300 ml-1",
                                "text-xs font-mono text-blue-700 ml-1",
                            ),
                        ),
                        rx.icon(
                            "external-link",
                            class_name="h-3 w-3 ml-1 inline-block",
                        ),
                        href="https://www.wikidata.org/wiki/"
                        + ResearchState.selected_preview["wikidata_id"],
                        target="_blank",
                        title="Abrir entidade no Wikidata",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "px-2.5 py-1 rounded-md bg-blue-950/40 border border-blue-900 hover:border-blue-700 hover:bg-blue-950/60 transition-colors inline-flex items-center",
                            "px-2.5 py-1 rounded-md bg-blue-50 border border-blue-100 hover:border-blue-300 hover:bg-blue-100 transition-colors inline-flex items-center",
                        ),
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Wikidata",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-[10px] font-semibold uppercase text-gray-400",
                                "text-[10px] font-semibold uppercase text-gray-500",
                            ),
                        ),
                        rx.el.span(
                            ResearchState.selected_preview["wikidata_id"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-mono text-gray-300 ml-1",
                                "text-xs font-mono text-gray-700 ml-1",
                            ),
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "px-2.5 py-1 rounded-md bg-gray-800 border border-gray-700",
                            "px-2.5 py-1 rounded-md bg-gray-100 border border-gray-200",
                        ),
                    ),
                ),
                class_name="flex items-start justify-between gap-3",
            ),
            class_name="flex items-start justify-between gap-3 flex-wrap",
        ),
        rx.el.p(
            ResearchState.selected_preview["extract"],
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-sm text-gray-300 leading-relaxed mt-3",
                "text-sm text-gray-600 leading-relaxed mt-3",
            ),
        ),
        rx.cond(
            ResearchState.is_disambiguation,
            rx.el.div(
                rx.icon(
                    "triangle-alert",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-4 w-4 text-amber-400 shrink-0",
                        "h-4 w-4 text-amber-600 shrink-0",
                    ),
                ),
                rx.el.p(
                    "Página de desambiguação detectada. Por favor, selecione um artigo mais específico nos resultados.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-amber-200",
                        "text-xs text-amber-800",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "flex items-start gap-2 mt-4 p-3 rounded-lg bg-amber-950/40 border border-amber-900",
                    "flex items-start gap-2 mt-4 p-3 rounded-lg bg-amber-50 border border-amber-200",
                ),
            ),
            rx.cond(
                ResearchState.is_human,
                rx.el.div(
                    rx.icon(
                        "circle-check-big",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-4 w-4 text-emerald-400 shrink-0",
                            "h-4 w-4 text-emerald-600 shrink-0",
                        ),
                    ),
                    rx.el.p(
                        "Confirme para extrair informações biográficas (nome, nacionalidade, datas e locais).",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-emerald-200",
                            "text-xs text-emerald-800",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "flex items-start gap-2 mt-4 p-3 rounded-lg bg-emerald-950/40 border border-emerald-900",
                        "flex items-start gap-2 mt-4 p-3 rounded-lg bg-emerald-50 border border-emerald-100",
                    ),
                ),
                rx.el.div(
                    rx.icon(
                        "triangle-alert",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-4 w-4 text-red-400 shrink-0",
                            "h-4 w-4 text-red-600 shrink-0",
                        ),
                    ),
                    rx.el.p(
                        "O artigo selecionado não parece ser biográfico (não corresponde a uma pessoa). Por favor, selecione um artigo referente a uma pessoa biográfica para continuar.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-red-200",
                            "text-xs text-red-800",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "flex items-start gap-2 mt-4 p-3 rounded-lg bg-red-950/40 border border-red-900",
                        "flex items-start gap-2 mt-4 p-3 rounded-lg bg-red-50 border border-red-200",
                    ),
                ),
            ),
        ),
        rx.el.div(
            rx.el.a(
                rx.icon(
                    "external-link",
                    class_name="h-3.5 w-3.5",
                ),
                rx.el.span("Ver na Wikipédia"),
                href=ResearchState.selected_preview["url"],
                target="_blank",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-300 hover:text-blue-400 px-3 py-2 rounded-lg border border-gray-800 hover:border-blue-800 transition-colors",
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-700 hover:text-blue-700 px-3 py-2 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors",
                ),
            ),
            rx.el.button(
                rx.cond(
                    ResearchState.is_extracting,
                    rx.icon(
                        "loader-circle",
                        class_name="h-3.5 w-3.5 animate-spin",
                    ),
                    rx.icon("check", class_name="h-3.5 w-3.5"),
                ),
                rx.el.span(
                    rx.cond(
                        ResearchState.is_extracting,
                        "Extraindo...",
                        rx.cond(
                            ResearchState.is_human,
                            "Confirmar e extrair",
                            "Não biográfico",
                        ),
                    )
                ),
                on_click=ResearchState.confirm_article,
                disabled=ResearchState.is_disambiguation
                | ResearchState.is_extracting
                | ~ResearchState.is_human,
                class_name="inline-flex items-center gap-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 px-3 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
            ),
            class_name="flex items-center gap-2 mt-4",
        ),
        id="preview-anchor",
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5 scroll-mt-20",
            "bg-white border border-gray-200 rounded-xl p-5 scroll-mt-20",
        ),
    )


def guided_chips_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("sparkles", class_name="h-3.5 w-3.5 text-blue-500"),
            rx.el.span(
                "Sugestões guiadas",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-bold uppercase tracking-wider text-blue-400",
                    "text-[10px] font-bold uppercase tracking-wider text-blue-600",
                ),
            ),
            class_name="flex items-center gap-1.5 mb-2",
        ),
        rx.el.div(
            rx.foreach(
                ResearchState.dynamic_suggestions,
                suggestion_button,
            ),
            class_name="flex items-center gap-1.5 flex-wrap",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "px-4 py-3 rounded-lg bg-gradient-to-r from-blue-950/30 to-gray-900 border border-blue-900/40 mt-3",
            "px-4 py-3 rounded-lg bg-gradient-to-r from-blue-50/70 to-white border border-blue-100 mt-3",
        ),
    )


def search_panel() -> rx.Component:
    return rx.el.div(
        workbench_header(),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Ex: Fernando Pessoa, Machado de Assis, Marie Curie...",
                    default_value=ResearchState.search_query,
                    on_change=ResearchState.set_search_query.debounce(500),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "w-full pl-10 pr-10 py-3 text-sm bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500 text-gray-100",
                        "w-full pl-10 pr-10 py-3 text-sm bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400",
                    ),
                    aria_label="Termo de pesquisa na Wikipédia",
                ),
                rx.cond(
                    ResearchState.search_query != "",
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=ResearchState.clear_search,
                        class_name="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-700",
                        aria_label="Limpar termo de pesquisa",
                    ),
                    rx.fragment(),
                ),
                class_name="relative flex-1 min-w-[200px]",
            ),
            rx.el.button(
                rx.cond(
                    ResearchState.is_searching,
                    rx.icon("loader-circle", class_name="h-4 w-4 animate-spin"),
                    rx.icon("search", class_name="h-4 w-4"),
                ),
                rx.el.span("Pesquisar"),
                on_click=ResearchState.perform_search,
                class_name="inline-flex items-center gap-2 px-5 py-3 text-sm font-semibold text-white bg-gradient-to-br from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 rounded-lg transition-all shadow-sm shrink-0 disabled:opacity-50 disabled:cursor-not-allowed",
                disabled=ResearchState.is_searching,
                aria_label="Executar busca biográfica",
            ),
            class_name="flex flex-col sm:flex-row gap-2",
        ),
        guided_chips_bar(),
        rx.cond(
            ResearchState.error_message != "",
            rx.el.div(
                rx.icon(
                    "circle-alert",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-4 w-4 text-red-400 shrink-0",
                        "h-4 w-4 text-red-600 shrink-0",
                    ),
                ),
                rx.el.p(
                    ResearchState.error_message,
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-red-200",
                        "text-xs text-red-800",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "flex items-start gap-2 mt-3 p-3 rounded-lg bg-red-950/40 border border-red-900",
                    "flex items-start gap-2 mt-3 p-3 rounded-lg bg-red-50 border border-red-200",
                ),
            ),
            rx.fragment(),
        ),
        rx.cond(
            (ResearchState.info_message != "")
            & (ResearchState.error_message == ""),
            rx.el.div(
                rx.icon(
                    "info",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-4 w-4 text-blue-400 shrink-0",
                        "h-4 w-4 text-blue-600 shrink-0",
                    ),
                ),
                rx.el.p(
                    ResearchState.info_message,
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-blue-200",
                        "text-xs text-blue-800",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "flex items-start gap-2 mt-3 p-3 rounded-lg bg-blue-950/40 border border-blue-900",
                    "flex items-start gap-2 mt-3 p-3 rounded-lg bg-blue-50 border border-blue-200",
                ),
            ),
            rx.fragment(),
        ),
        rx.cond(
            ResearchState.is_loading_article,
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "h-32 rounded-xl bg-gray-800 animate-pulse mt-5",
                        "h-32 rounded-xl bg-gray-100 animate-pulse mt-5",
                    ),
                ),
            ),
            rx.cond(
                ResearchState.has_preview,
                rx.el.div(preview_panel(), class_name="mt-5"),
                rx.fragment(),
            ),
        ),
        rx.el.div(
            rx.cond(
                ResearchState.is_searching,
                loading_skeleton(),
                rx.cond(
                    ResearchState.has_results,
                    rx.el.div(
                        rx.el.p(
                            rx.cond(
                                ResearchState.has_preview,
                                "Outros resultados",
                                "Resultados encontrados",
                            ),
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2",
                                "text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2",
                            ),
                        ),
                        rx.el.div(
                            rx.foreach(
                                ResearchState.search_results, search_result_item
                            ),
                            class_name="space-y-2",
                        ),
                    ),
                    rx.cond(
                        ResearchState.has_preview,
                        rx.fragment(),
                        empty_state(),
                    ),
                ),
            ),
            class_name="mt-5",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-2xl p-6 relative overflow-hidden",
            "bg-white border border-gray-200 rounded-2xl p-6 relative overflow-hidden shadow-sm",
        ),
    )