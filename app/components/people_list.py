import reflex as rx
from app.states.research_state import ResearchState


def person_card(person) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    person["image_url"] != "",
                    rx.el.img(
                        src=person["image_url"],
                        alt=person["name"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-11 w-11 rounded-full bg-gray-800 object-cover border border-gray-700",
                            "h-11 w-11 rounded-full bg-gray-100 object-cover border border-gray-200",
                        ),
                    ),
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/notionists/svg?seed={person['name']}",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-11 w-11 rounded-full bg-gray-800",
                            "h-11 w-11 rounded-full bg-gray-100",
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
                class_name="flex items-center gap-3",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                on_click=lambda: ResearchState.remove_person(person["id"]),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-gray-500 hover:text-red-400 p-1.5 rounded-md hover:bg-red-950/30 transition-colors",
                    "text-gray-400 hover:text-red-600 p-1.5 rounded-md hover:bg-red-50 transition-colors",
                ),
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.p(
            person["summary"],
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-xs text-gray-400 mt-3 line-clamp-2 leading-relaxed",
                "text-xs text-gray-600 mt-3 line-clamp-2 leading-relaxed",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", class_name="h-3 w-3 text-gray-400"),
                rx.el.span(
                    f"{person['birth_date']}  →  {person['death_date']}",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[11px] text-gray-300 font-mono",
                        "text-[11px] text-gray-600 font-mono",
                    ),
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.div(
                rx.icon("map-pin", class_name="h-3 w-3 text-gray-400"),
                rx.el.span(
                    person["birth_place"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-[11px] text-gray-300",
                        "text-[11px] text-gray-600",
                    ),
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "flex flex-col gap-1.5 mt-3 pt-3 border-t border-gray-800",
                "flex flex-col gap-1.5 mt-3 pt-3 border-t border-gray-100",
            ),
        ),
        rx.el.div(
            rx.cond(
                person["completeness"] == 100,
                rx.el.span(
                    rx.el.span(
                        class_name="h-1.5 w-1.5 rounded-full bg-emerald-500"
                    ),
                    rx.el.span(
                        "Dados completos",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-medium text-emerald-300",
                            "text-[10px] font-medium text-emerald-700",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-950/40 border border-emerald-900",
                        "inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-50 border border-emerald-100",
                    ),
                ),
                rx.el.span(
                    rx.el.span(
                        class_name="h-1.5 w-1.5 rounded-full bg-amber-500"
                    ),
                    rx.el.span(
                        f"Dados parciais ({person['completeness']}%%)",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] font-medium text-amber-300",
                            "text-[10px] font-medium text-amber-700",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-950/40 border border-amber-900",
                        "inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-50 border border-amber-100",
                    ),
                ),
            ),
            rx.el.a(
                rx.icon("external-link", class_name="h-3 w-3"),
                href=person["article_url"],
                target="_blank",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-gray-500 hover:text-blue-400",
                    "text-gray-400 hover:text-blue-600",
                ),
            ),
            class_name="flex items-center justify-between mt-3",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-blue-900 transition-all",
            "bg-white border border-gray-200 rounded-xl p-4 hover:border-blue-200 hover:shadow-sm transition-all",
        ),
    )


def people_list() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Pessoas pesquisadas",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100",
                        "text-lg font-bold text-gray-900",
                    ),
                ),
                rx.el.p(
                    "Composição em comum dos artigos confirmados nesta sessão.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 mt-0.5",
                        "text-sm text-gray-500 mt-0.5",
                    ),
                ),
            ),
            rx.el.span(
                ResearchState.total_people.to_string(),
                rx.el.span(
                    " registros",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs font-medium text-gray-400 ml-1",
                        "text-xs font-medium text-gray-500 ml-1",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm font-bold text-gray-100 px-3 py-1 rounded-full bg-gray-800 border border-gray-700",
                    "text-sm font-bold text-gray-900 px-3 py-1 rounded-full bg-gray-100 border border-gray-200",
                ),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.cond(
            ResearchState.total_people > 0,
            rx.el.div(
                rx.foreach(ResearchState.people, person_card),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4",
            ),
            rx.el.div(
                rx.icon("users", class_name="h-8 w-8 text-gray-500 mx-auto"),
                rx.el.p(
                    "Nenhuma pessoa pesquisada ainda.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-3",
                        "text-sm text-gray-500 text-center mt-3",
                    ),
                ),
                rx.el.p(
                    "Confirme um artigo na busca para começar sua composição.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-500 text-center mt-1",
                        "text-xs text-gray-400 text-center mt-1",
                    ),
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "bg-gray-900 border border-dashed border-gray-700 rounded-xl py-12",
                    "bg-white border border-dashed border-gray-300 rounded-xl py-12",
                ),
            ),
        ),
    )