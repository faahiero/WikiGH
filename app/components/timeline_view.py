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
                        rx.cond(
                            (
                                ResearchState.selected_person["is_homonym"]
                                == "true"
                            )
                            & (
                                ResearchState.selected_person["context_label"]
                                != ""
                            ),
                            rx.el.div(
                                rx.icon(
                                    "split",
                                    class_name="h-3 w-3 text-amber-600",
                                ),
                                rx.el.span(
                                    "Homônimo:",
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-[10px] font-bold uppercase tracking-wider text-amber-300",
                                        "text-[10px] font-bold uppercase tracking-wider text-amber-700",
                                    ),
                                ),
                                rx.el.span(
                                    ResearchState.selected_person[
                                        "context_label"
                                    ],
                                    class_name=rx.cond(
                                        ResearchState.dark_mode,
                                        "text-[11px] text-amber-200 truncate",
                                        "text-[11px] text-amber-800 truncate",
                                    ),
                                ),
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "inline-flex items-center gap-1 px-2 py-0.5 mt-1 rounded-md bg-amber-950/40 border border-amber-900 max-w-full",
                                    "inline-flex items-center gap-1 px-2 py-0.5 mt-1 rounded-md bg-amber-50 border border-amber-100 max-w-full",
                                ),
                            ),
                            rx.fragment(),
                        ),
                        rx.el.p(
                            ResearchState.selected_person["nationality"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-sm text-gray-400 mt-0.5",
                                "text-sm text-gray-500 mt-0.5",
                            ),
                        ),
                        rx.cond(
                            ResearchState.selected_person["short_id"] != "",
                            rx.el.span(
                                ResearchState.selected_person["short_id"],
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-[10px] font-mono text-blue-300 mt-0.5 inline-block",
                                    "text-[10px] font-mono text-blue-600 mt-0.5 inline-block",
                                ),
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex flex-col",
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


def narrative_timeline_event(event) -> rx.Component:
    is_birth = event["kind"] == "Nascimento"
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        is_birth,
                        "h-3 w-3 rounded-full bg-emerald-500 ring-4 ring-emerald-100 z-10",
                        "h-3 w-3 rounded-full bg-red-500 ring-4 ring-red-100 z-10",
                    ),
                ),
                class_name="absolute left-[18px] top-6 -translate-x-1/2",
            ),
            rx.el.div(
                rx.el.p(
                    event["year"].to_string(),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-2xl font-extrabold text-gray-100 font-mono leading-none",
                        "text-2xl font-extrabold text-gray-900 font-mono leading-none",
                    ),
                ),
                rx.el.p(
                    event["date_br"],
                    title=event["date"],
                    class_name="text-[10px] text-gray-400 font-mono mt-0.5",
                ),
                class_name="w-20 shrink-0 pt-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        is_birth,
                        rx.icon(
                            "baby", class_name="h-3.5 w-3.5 text-emerald-600"
                        ),
                        rx.icon(
                            "flower-2", class_name="h-3.5 w-3.5 text-red-600"
                        ),
                    ),
                    rx.el.span(
                        rx.cond(is_birth, "Nascimento", "Falecimento"),
                        class_name=rx.cond(
                            is_birth,
                            "text-[10px] font-bold uppercase tracking-wider text-emerald-700",
                            "text-[10px] font-bold uppercase tracking-wider text-red-700",
                        ),
                    ),
                    class_name="flex items-center gap-1 mb-1",
                ),
                rx.el.p(
                    event["name"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-bold text-gray-100 leading-tight",
                        "text-sm font-bold text-gray-900 leading-tight",
                    ),
                ),
                rx.cond(
                    event["is_homonym"] & (event["context_label"] != ""),
                    rx.el.div(
                        rx.icon(
                            "split", class_name="h-2.5 w-2.5 text-amber-600"
                        ),
                        rx.el.span(
                            event["context_label"],
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-[10px] text-amber-200 truncate",
                                "text-[10px] text-amber-800 truncate",
                            ),
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "inline-flex items-center gap-1 px-1.5 py-0.5 mt-1 rounded bg-amber-950/40 border border-amber-900 max-w-full",
                            "inline-flex items-center gap-1 px-1.5 py-0.5 mt-1 rounded bg-amber-50 border border-amber-100 max-w-full",
                        ),
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.icon(
                        "map-pin", class_name="h-3 w-3 text-gray-400 shrink-0"
                    ),
                    rx.el.span(
                        event["place"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-400 truncate",
                            "text-xs text-gray-600 truncate",
                        ),
                    ),
                    class_name="flex items-center gap-1 mt-1",
                ),
                class_name="flex-1 min-w-0 text-left",
            ),
            class_name="flex items-start gap-4 w-full pl-10",
        ),
        on_click=lambda: ResearchState.select_person(event["person_id"]),
        class_name=rx.cond(
            ResearchState.selected_person_id == event["person_id"],
            rx.cond(
                ResearchState.dark_mode,
                "w-full p-3 rounded-xl border-2 border-blue-700 bg-blue-950/30 transition-all relative",
                "w-full p-3 rounded-xl border-2 border-blue-400 bg-blue-50/60 transition-all relative",
            ),
            rx.cond(
                ResearchState.dark_mode,
                "w-full p-3 rounded-xl border border-gray-800 bg-gray-900 hover:border-blue-800 hover:bg-blue-950/30 transition-all relative",
                "w-full p-3 rounded-xl border border-gray-200 bg-white hover:border-blue-300 hover:bg-blue-50/40 transition-all relative",
            ),
        ),
    )


def narrative_filter_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("calendar-range", class_name="h-3.5 w-3.5 text-amber-600"),
            rx.el.span(
                "Filtros narrativos",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-bold uppercase tracking-wider text-amber-400",
                    "text-[10px] font-bold uppercase tracking-wider text-amber-700",
                ),
            ),
            class_name="flex items-center gap-1.5",
        ),
        rx.el.div(
            filter_button("Todos os eventos", "all"),
            filter_button("Nascimentos", "birth"),
            filter_button("Falecimentos", "death"),
            class_name="flex items-center gap-2 flex-wrap",
        ),
        class_name="flex items-center justify-between gap-4 flex-wrap",
    )


def timeline_summary_strip() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "Período",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold uppercase text-gray-400",
                    "text-[10px] font-semibold uppercase text-gray-500",
                ),
            ),
            rx.el.p(
                ResearchState.timeline_span,
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm font-bold text-gray-100 font-mono",
                    "text-sm font-bold text-gray-900 font-mono",
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "px-3 py-2 border-r border-gray-800",
                "px-3 py-2 border-r border-gray-100",
            ),
        ),
        rx.el.div(
            rx.el.span(
                "Eventos",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold uppercase text-gray-400",
                    "text-[10px] font-semibold uppercase text-gray-500",
                ),
            ),
            rx.el.p(
                ResearchState.total_timeline_events.to_string(),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm font-bold text-gray-100",
                    "text-sm font-bold text-gray-900",
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "px-3 py-2 border-r border-gray-800",
                "px-3 py-2 border-r border-gray-100",
            ),
        ),
        rx.el.div(
            rx.el.span(
                "Vida média",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold uppercase text-gray-400",
                    "text-[10px] font-semibold uppercase text-gray-500",
                ),
            ),
            rx.el.p(
                f"{ResearchState.average_lifespan} anos",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm font-bold text-gray-100",
                    "text-sm font-bold text-gray-900",
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "px-3 py-2 border-r border-gray-800",
                "px-3 py-2 border-r border-gray-100",
            ),
        ),
        rx.el.div(
            rx.el.span(
                "Século pico",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold uppercase text-gray-400",
                    "text-[10px] font-semibold uppercase text-gray-500",
                ),
            ),
            rx.el.p(
                ResearchState.peak_century,
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-sm font-bold text-gray-100",
                    "text-sm font-bold text-gray-900",
                ),
            ),
            class_name="px-3 py-2",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex items-center bg-gray-950 rounded-xl border border-gray-800 overflow-hidden mb-4",
            "flex items-center bg-gradient-to-r from-amber-50/30 to-white rounded-xl border border-amber-100 overflow-hidden mb-4",
        ),
    )


def timeline_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("scroll-text", class_name="h-4 w-4 text-white"),
                        class_name="h-9 w-9 rounded-lg bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Cronologia narrativa",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-[10px] font-bold tracking-widest text-amber-400 uppercase",
                                "text-[10px] font-bold tracking-widest text-amber-700 uppercase",
                            ),
                        ),
                        rx.el.h2(
                            "Linha do tempo histórica",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-lg font-bold text-gray-100 leading-tight",
                                "text-lg font-bold text-gray-900 leading-tight",
                            ),
                        ),
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="mb-4",
            ),
            timeline_summary_strip(),
            narrative_filter_bar(),
            rx.el.div(class_name="h-3"),
            rx.cond(
                ResearchState.total_timeline_events > 0,
                rx.el.div(
                    rx.el.div(
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "absolute left-[18px] top-2 bottom-2 w-px bg-gradient-to-b from-transparent via-amber-900/40 to-transparent",
                            "absolute left-[18px] top-2 bottom-2 w-px bg-gradient-to-b from-transparent via-amber-200 to-transparent",
                        ),
                    ),
                    rx.foreach(
                        ResearchState.timeline_events, narrative_timeline_event
                    ),
                    class_name="flex flex-col gap-2 max-h-[480px] overflow-y-auto pr-1 relative",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "calendar-clock",
                            class_name="h-10 w-10 text-amber-600",
                        ),
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "h-20 w-20 rounded-full bg-amber-950/40 border border-amber-900 flex items-center justify-center mx-auto",
                            "h-20 w-20 rounded-full bg-amber-50 border border-amber-100 flex items-center justify-center mx-auto",
                        ),
                    ),
                    rx.el.p(
                        "Nenhum evento na linha do tempo.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-base font-semibold text-gray-100 text-center mt-4",
                            "text-base font-semibold text-gray-900 text-center mt-4",
                        ),
                    ),
                    rx.el.p(
                        "Pesquise pessoas com datas conhecidas para construir sua narrativa histórica.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm text-gray-400 text-center mt-1 max-w-md mx-auto",
                            "text-sm text-gray-500 text-center mt-1 max-w-md mx-auto",
                        ),
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "bg-gray-950 border border-dashed border-gray-800 rounded-xl py-12",
                        "bg-gradient-to-b from-amber-50/30 to-white border border-dashed border-amber-200 rounded-xl py-12",
                    ),
                ),
            ),
            class_name=rx.cond(
                ResearchState.dark_mode,
                "bg-gray-900 border border-gray-800 rounded-2xl p-5 lg:col-span-2",
                "bg-white border border-gray-200 rounded-2xl p-5 lg:col-span-2 shadow-sm",
            ),
        ),
        rx.el.div(
            selected_detail_panel(),
            class_name="flex flex-col gap-4",
        ),
        class_name="grid grid-cols-1 lg:grid-cols-3 gap-4",
    )