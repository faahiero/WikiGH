import reflex as rx
from app.states.research_state import ResearchState


def table_row(person) -> rx.Component:
    cell_cls = rx.cond(
        ResearchState.dark_mode,
        "px-4 py-3 border-b border-gray-800",
        "px-4 py-3 border-b border-gray-100",
    )
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.cond(
                    person["image_url"] != "",
                    rx.el.img(
                        src=person["image_url"],
                        alt=person["name"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-8 w-8 rounded-full bg-gray-800 shrink-0 object-cover border border-gray-700",
                            "h-8 w-8 rounded-full bg-gray-100 shrink-0 object-cover border border-gray-200",
                        ),
                    ),
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/notionists/svg?seed={person['name']}",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-8 w-8 rounded-full bg-gray-800 shrink-0",
                            "h-8 w-8 rounded-full bg-gray-100 shrink-0",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        person["name"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-semibold text-gray-100",
                            "text-sm font-semibold text-gray-900",
                        ),
                    ),
                    rx.el.p(
                        person["nationality"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-400",
                            "text-xs text-gray-500",
                        ),
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name=cell_cls,
        ),
        rx.el.td(
            rx.el.p(
                person["birth_date"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-mono text-gray-100",
                    "text-xs font-mono text-gray-900",
                ),
            ),
            rx.el.p(
                person["birth_place"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 truncate max-w-[200px]",
                    "text-xs text-gray-500 truncate max-w-[200px]",
                ),
            ),
            class_name=cell_cls,
        ),
        rx.el.td(
            rx.el.p(
                person["death_date"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-mono text-gray-100",
                    "text-xs font-mono text-gray-900",
                ),
            ),
            rx.el.p(
                person["death_place"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-400 truncate max-w-[200px]",
                    "text-xs text-gray-500 truncate max-w-[200px]",
                ),
            ),
            class_name=cell_cls,
        ),
        rx.el.td(
            rx.cond(
                person["completeness"] == 100,
                rx.el.span(
                    f"{person['completeness']}%",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[10px] font-semibold text-emerald-300 bg-emerald-950/40 border border-emerald-900 px-2 py-0.5 rounded-full w-fit inline-block",
                        "text-[10px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-full w-fit inline-block",
                    ),
                ),
                rx.el.span(
                    f"{person['completeness']}%",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[10px] font-semibold text-amber-300 bg-amber-950/40 border border-amber-900 px-2 py-0.5 rounded-full w-fit inline-block",
                        "text-[10px] font-semibold text-amber-700 bg-amber-50 border border-amber-100 px-2 py-0.5 rounded-full w-fit inline-block",
                    ),
                ),
            ),
            class_name=cell_cls,
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    rx.icon("external-link", class_name="h-3.5 w-3.5"),
                    href=person["article_url"],
                    target="_blank",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-gray-500 hover:text-blue-400 p-1.5 rounded-md hover:bg-blue-950/30",
                        "text-gray-400 hover:text-blue-600 p-1.5 rounded-md hover:bg-blue-50",
                    ),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                    on_click=lambda: ResearchState.remove_person(person["id"]),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-gray-500 hover:text-red-400 p-1.5 rounded-md hover:bg-red-950/30",
                        "text-gray-400 hover:text-red-600 p-1.5 rounded-md hover:bg-red-50",
                    ),
                ),
                class_name="flex items-center gap-1",
            ),
            class_name=cell_cls,
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "hover:bg-blue-950/20 transition-colors",
            "hover:bg-blue-50/30 transition-colors",
        ),
    )


def table_view() -> rx.Component:
    th_cls = rx.cond(
        ResearchState.dark_mode,
        "px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-gray-400 bg-gray-950 border-b border-gray-800",
        "px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b border-gray-200",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Tabela completa",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100",
                        "text-lg font-bold text-gray-900",
                    ),
                ),
                rx.el.p(
                    "Composição completa de pessoas pesquisadas com opção de exportação.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 mt-0.5",
                        "text-sm text-gray-500 mt-0.5",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Filtrar nome, nacionalidade, local...",
                        default_value=ResearchState.table_search,
                        on_change=ResearchState.set_table_search.debounce(500),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "pl-9 pr-3 py-2 text-xs bg-gray-800 border border-gray-700 rounded-lg w-full sm:w-64 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100 placeholder-gray-500",
                            "pl-9 pr-3 py-2 text-xs bg-gray-50 border border-gray-200 rounded-lg w-full sm:w-64 focus:outline-none focus:ring-2 focus:ring-blue-500",
                        ),
                        aria_label="Filtrar resultados da tabela",
                    ),
                    class_name="relative w-full sm:w-auto",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-3.5 w-3.5"),
                    rx.el.span("Exportar CSV"),
                    on_click=ResearchState.export_csv_with_feedback,
                    class_name="inline-flex items-center gap-1.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 px-3 py-2 rounded-lg transition-colors",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between gap-4 mb-4 flex-wrap",
        ),
        rx.cond(
            ResearchState.total_people > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                rx.el.div(
                                    rx.icon("user", class_name="h-3.5 w-3.5"),
                                    rx.el.span("Pessoa"),
                                    class_name="flex items-center gap-1.5",
                                ),
                                class_name=th_cls,
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon("baby", class_name="h-3.5 w-3.5"),
                                    rx.el.span("Nascimento"),
                                    class_name="flex items-center gap-1.5",
                                ),
                                class_name=th_cls,
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon(
                                        "flower-2", class_name="h-3.5 w-3.5"
                                    ),
                                    rx.el.span("Falecimento"),
                                    class_name="flex items-center gap-1.5",
                                ),
                                class_name=th_cls,
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon(
                                        "circle-check", class_name="h-3.5 w-3.5"
                                    ),
                                    rx.el.span("Completude"),
                                    class_name="flex items-center gap-1.5",
                                ),
                                class_name=th_cls,
                            ),
                            rx.el.th(
                                "Ações",
                                class_name=th_cls,
                            ),
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(ResearchState.filtered_people, table_row),
                    ),
                    class_name="table-auto w-full",
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "bg-gray-900 border border-gray-800 rounded-xl overflow-hidden overflow-x-auto",
                    "bg-white border border-gray-200 rounded-xl overflow-hidden overflow-x-auto",
                ),
            ),
            rx.el.div(
                rx.icon("table", class_name="h-8 w-8 text-gray-500 mx-auto"),
                rx.el.p(
                    "Sem dados na composição.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-3",
                        "text-sm text-gray-500 text-center mt-3",
                    ),
                ),
                rx.el.p(
                    "Confirme um artigo na busca para começar.",
                    class_name="text-xs text-gray-500 text-center mt-1",
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "bg-gray-900 border border-dashed border-gray-700 rounded-xl py-12",
                    "bg-white border border-dashed border-gray-300 rounded-xl py-12",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )