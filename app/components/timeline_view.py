import reflex as rx
from app.states.research_state import ResearchState


def filter_button(label: str, value: str) -> rx.Component:
    is_active = ResearchState.timeline_filter == value
    return rx.el.button(
        label,
        on_click=lambda: ResearchState.set_timeline_filter(value),
        class_name=rx.cond(
            is_active,
            "px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 text-white border border-blue-600",
            rx.cond(
                ResearchState.dark_mode,
                "px-3 py-1.5 text-xs font-semibold rounded-lg bg-gray-900 text-gray-300 border border-gray-800 hover:border-blue-800 hover:text-blue-400",
                "px-3 py-1.5 text-xs font-semibold rounded-lg bg-white text-gray-700 border border-gray-200 hover:border-blue-300 hover:text-blue-700",
            ),
        ),
    )


def timeline_event_row(event) -> rx.Component:
    is_birth = event["kind"] == "Nascimento"
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    is_birth,
                    rx.icon("baby", class_name="h-4 w-4 text-emerald-500"),
                    rx.icon("flower-2", class_name="h-4 w-4 text-red-500"),
                ),
                class_name=rx.cond(
                    is_birth,
                    rx.cond(
                        ResearchState.dark_mode,
                        "h-9 w-9 rounded-lg bg-emerald-950/40 border border-emerald-900 flex items-center justify-center shrink-0",
                        "h-9 w-9 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center shrink-0",
                    ),
                    rx.cond(
                        ResearchState.dark_mode,
                        "h-9 w-9 rounded-lg bg-red-950/40 border border-red-900 flex items-center justify-center shrink-0",
                        "h-9 w-9 rounded-lg bg-red-50 border border-red-100 flex items-center justify-center shrink-0",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        event["name"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-semibold text-gray-100",
                            "text-sm font-semibold text-gray-900",
                        ),
                    ),
                    rx.cond(
                        is_birth,
                        rx.el.span(
                            "Nascimento",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-[10px] font-semibold text-emerald-300 bg-emerald-950/40 border border-emerald-900 px-2 py-0.5 rounded-full",
                                "text-[10px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-full",
                            ),
                        ),
                        rx.el.span(
                            "Falecimento",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-[10px] font-semibold text-red-300 bg-red-950/40 border border-red-900 px-2 py-0.5 rounded-full",
                                "text-[10px] font-semibold text-red-700 bg-red-50 border border-red-100 px-2 py-0.5 rounded-full",
                            ),
                        ),
                    ),
                    class_name="flex items-center gap-2 flex-wrap",
                ),
                rx.el.p(
                    event["place"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 mt-0.5",
                        "text-xs text-gray-600 mt-0.5",
                    ),
                ),
                class_name="flex-1 text-left min-w-0",
            ),
            rx.el.div(
                rx.el.p(
                    event["year"].to_string(),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-lg font-bold text-gray-100 font-mono",
                        "text-lg font-bold text-gray-900 font-mono",
                    ),
                ),
                rx.el.p(
                    event["date"],
                    class_name="text-[10px] text-gray-400 font-mono",
                ),
                class_name="text-right shrink-0",
            ),
            class_name="flex items-center gap-3 w-full",
        ),
        on_click=lambda: ResearchState.select_person(event["person_id"]),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "w-full p-3 rounded-lg border border-gray-800 hover:border-blue-800 hover:bg-blue-950/30 transition-colors",
            "w-full p-3 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50/40 transition-colors",
        ),
    )


def selected_detail_panel() -> rx.Component:
    return rx.cond(
        ResearchState.has_selected_person,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        ResearchState.selected_person["image_url"] != "",
                        rx.el.img(
                            src=ResearchState.selected_person["image_url"],
                            alt=ResearchState.selected_person["name"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "h-14 w-14 rounded-full bg-gray-800 object-cover border border-gray-700 shrink-0",
                                "h-14 w-14 rounded-full bg-gray-100 object-cover border border-gray-200 shrink-0",
                            ),
                        ),
                        rx.el.img(
                            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={ResearchState.selected_person['name']}",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "h-14 w-14 rounded-full bg-gray-800 shrink-0",
                                "h-14 w-14 rounded-full bg-gray-100 shrink-0",
                            ),
                        ),
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Detalhes",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xs font-semibold uppercase tracking-wider text-blue-400",
                                "text-xs font-semibold uppercase tracking-wider text-blue-600",
                            ),
                        ),
                        rx.el.h3(
                            ResearchState.selected_person["name"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-xl font-bold text-gray-100 mt-1",
                                "text-xl font-bold text-gray-900 mt-1",
                            ),
                        ),
                        rx.el.p(
                            ResearchState.selected_person["nationality"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-sm text-gray-400",
                                "text-sm text-gray-500",
                            ),
                        ),
                    ),
                    class_name="flex items-start gap-3",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-4 w-4"),
                    on_click=lambda: ResearchState.select_person(""),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-gray-500 hover:text-gray-200 p-1",
                        "text-gray-400 hover:text-gray-700 p-1",
                    ),
                ),
                class_name="flex items-start justify-between",
            ),
            rx.el.p(
                ResearchState.selected_person["summary"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs text-gray-300 leading-relaxed mt-3 line-clamp-4",
                    "text-xs text-gray-600 leading-relaxed mt-3 line-clamp-4",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Nascimento",
                        class_name="text-[10px] font-semibold uppercase text-gray-400",
                    ),
                    rx.el.p(
                        ResearchState.selected_person["birth_date"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-mono text-gray-100",
                            "text-sm font-mono text-gray-900",
                        ),
                    ),
                    rx.el.p(
                        ResearchState.selected_person["birth_place"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-400",
                            "text-xs text-gray-600",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "p-3 rounded-lg bg-emerald-950/30 border border-emerald-900",
                        "p-3 rounded-lg bg-emerald-50/60 border border-emerald-100",
                    ),
                ),
                rx.el.div(
                    rx.el.span(
                        "Falecimento",
                        class_name="text-[10px] font-semibold uppercase text-gray-400",
                    ),
                    rx.el.p(
                        ResearchState.selected_person["death_date"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-mono text-gray-100",
                            "text-sm font-mono text-gray-900",
                        ),
                    ),
                    rx.el.p(
                        ResearchState.selected_person["death_place"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-400",
                            "text-xs text-gray-600",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "p-3 rounded-lg bg-red-950/30 border border-red-900",
                        "p-3 rounded-lg bg-red-50/60 border border-red-100",
                    ),
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-4",
            ),
            rx.el.a(
                rx.icon("external-link", class_name="h-3.5 w-3.5"),
                rx.el.span("Ver na Wikipédia"),
                href=ResearchState.selected_person["article_url"],
                target="_blank",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-300 hover:text-blue-400 px-3 py-2 rounded-lg border border-gray-800 hover:border-blue-800 transition-colors mt-4",
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-700 hover:text-blue-700 px-3 py-2 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors mt-4",
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "bg-gray-900 border border-gray-800 rounded-xl p-5",
                "bg-white border border-gray-200 rounded-xl p-5",
            ),
        ),
        rx.el.div(
            rx.icon(
                "mouse-pointer-click",
                class_name="h-7 w-7 text-gray-500 mx-auto",
            ),
            rx.el.p(
                "Selecione um evento na linha do tempo para ver detalhes.",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm text-gray-400 text-center mt-2",
                    "text-sm text-gray-500 text-center mt-2",
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "bg-gray-900 border border-dashed border-gray-700 rounded-xl py-10",
                "bg-white border border-dashed border-gray-300 rounded-xl py-10",
            ),
        ),
    )


def timeline_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Linha do tempo",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-lg font-bold text-gray-100",
                            "text-lg font-bold text-gray-900",
                        ),
                    ),
                    rx.el.p(
                        "Eventos cronológicos de nascimento e falecimento.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm text-gray-400 mt-0.5",
                            "text-sm text-gray-500 mt-0.5",
                        ),
                    ),
                ),
                rx.el.div(
                    filter_button("Todos", "all"),
                    filter_button("Nascimentos", "birth"),
                    filter_button("Falecimentos", "death"),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-start justify-between gap-4 mb-4 flex-wrap",
            ),
            rx.cond(
                ResearchState.total_timeline_events > 0,
                rx.el.div(
                    rx.foreach(
                        ResearchState.timeline_events, timeline_event_row
                    ),
                    class_name="flex flex-col gap-2 max-h-[600px] overflow-y-auto pr-1",
                ),
                rx.el.div(
                    rx.icon(
                        "calendar-clock",
                        class_name="h-8 w-8 text-gray-500 mx-auto",
                    ),
                    rx.el.p(
                        "Nenhum evento na linha do tempo.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm text-gray-400 text-center mt-3",
                            "text-sm text-gray-500 text-center mt-3",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "bg-gray-950 border border-dashed border-gray-800 rounded-xl py-12",
                        "bg-gray-50 border border-dashed border-gray-300 rounded-xl py-12",
                    ),
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "bg-gray-900 border border-gray-800 rounded-xl p-5 lg:col-span-2",
                "bg-white border border-gray-200 rounded-xl p-5 lg:col-span-2",
            ),
        ),
        rx.el.div(
            selected_detail_panel(),
            class_name="flex flex-col gap-4",
        ),
        class_name="grid grid-cols-1 lg:grid-cols-3 gap-4",
    )