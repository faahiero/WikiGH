import reflex as rx
from app.states.research_state import ResearchState


def history_row(entry) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "history",
                class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    entry["term"],
                    title=entry["term"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm font-medium text-gray-100",
                        "text-sm font-medium text-gray-900",
                    ),
                ),
                rx.el.p(
                    f"→ {entry['title']}",
                    title=entry["title"],
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-xs text-gray-400 break-words",
                        "text-xs text-gray-500 break-words",
                    ),
                ),
                rx.cond(
                    entry["context_label"] != "",
                    rx.el.p(
                        entry["context_label"],
                        title=entry["context_label"],
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-[10px] text-amber-300 italic break-words mt-0.5",
                            "text-[10px] text-amber-700 italic break-words mt-0.5",
                        ),
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    entry["short_id"] != "",
                    rx.el.a(
                        entry["short_id"],
                        rx.icon(
                            "external-link",
                            class_name="h-2 w-2 inline-block ml-0.5",
                        ),
                        href="https://www.wikidata.org/wiki/" + entry["qid"],
                        target="_blank",
                        title=f"Abrir {entry['qid']} no Wikidata",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "inline-flex items-center text-[9px] font-mono text-blue-300 bg-blue-950/40 border border-blue-900 hover:border-blue-700 px-1.5 py-0.5 rounded mt-1",
                            "inline-flex items-center text-[9px] font-mono text-blue-700 bg-blue-50 border border-blue-100 hover:border-blue-300 px-1.5 py-0.5 rounded mt-1",
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name="min-w-0 flex-1",
            ),
            class_name="flex items-start gap-2 min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.span(
                entry["status"],
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-[10px] font-semibold text-emerald-300 bg-emerald-950/40 border border-emerald-900 px-2 py-0.5 rounded-full",
                    "text-[10px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-full",
                ),
            ),
            rx.el.span(
                entry["timestamp_br"],
                title=entry["timestamp"],
                class_name="text-[11px] text-gray-400 font-mono mt-1 block text-right",
            ),
            class_name="flex flex-col items-end gap-0.5 shrink-0",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "flex items-start justify-between gap-3 py-3 border-b border-gray-800 last:border-0",
            "flex items-start justify-between gap-3 py-3 border-b border-gray-100 last:border-0",
        ),
    )


def history_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Histórico recente",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-lg font-bold text-gray-100",
                            "text-lg font-bold text-gray-900",
                        ),
                    ),
                    rx.cond(
                        ResearchState.storage_ready,
                        rx.el.span(
                            rx.icon(
                                "database",
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "h-3 w-3 text-emerald-400",
                                    "h-3 w-3 text-emerald-700",
                                ),
                            ),
                            rx.el.span(
                                "Persistido",
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-[10px] font-semibold text-emerald-300",
                                    "text-[10px] font-semibold text-emerald-800",
                                ),
                            ),
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-950/40 border border-emerald-900",
                                "inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-50 border border-emerald-100",
                            ),
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "Buscas realizadas e seus artigos correspondentes (salvas localmente).",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 mt-0.5",
                        "text-sm text-gray-500 mt-0.5",
                    ),
                ),
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                rx.el.span("Limpar"),
                on_click=ResearchState.clear_history,
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-300 hover:text-red-400 px-3 py-1.5 rounded-lg border border-gray-800 hover:border-red-900 hover:bg-red-950/30 transition-colors",
                    "inline-flex items-center gap-1.5 text-xs font-medium text-gray-700 hover:text-red-700 px-3 py-1.5 rounded-lg border border-gray-200 hover:border-red-200 hover:bg-red-50 transition-colors",
                ),
            ),
            class_name="flex items-center justify-between mb-2",
        ),
        rx.cond(
            ResearchState.total_history > 0,
            rx.el.div(
                rx.foreach(ResearchState.enriched_history, history_row),
                class_name="px-1",
            ),
            rx.el.div(
                rx.icon("history", class_name="h-7 w-7 text-gray-500 mx-auto"),
                rx.el.p(
                    "Sem histórico no momento.",
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "text-sm text-gray-400 text-center mt-2",
                        "text-sm text-gray-500 text-center mt-2",
                    ),
                ),
                class_name="py-10",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5",
            "bg-white border border-gray-200 rounded-xl p-5",
        ),
    )