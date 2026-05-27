import reflex as rx
from app.states.research_state import ResearchState


def summary_card(
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
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "text-xs font-medium text-gray-500",
                    "text-xs font-medium text-gray-400",
                ),
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.p(
            label,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-sm font-medium text-gray-400 mt-4",
                "text-sm font-medium text-gray-500 mt-4",
            ),
        ),
        rx.el.p(
            value,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-3xl font-bold text-gray-100 mt-1 tracking-tight",
                "text-3xl font-bold text-gray-900 mt-1 tracking-tight",
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-blue-900 transition-colors",
            "bg-white border border-gray-200 rounded-xl p-5 hover:border-blue-200 transition-colors",
        ),
    )


def summary_cards() -> rx.Component:
    return rx.el.div(
        summary_card(
            "users",
            "Pessoas pesquisadas",
            ResearchState.total_people,
            "Total",
            "bg-blue-50 text-blue-600",
            "bg-blue-950/40 text-blue-400",
        ),
        summary_card(
            "map-pin",
            "Locais mapeados",
            ResearchState.total_locations,
            "Únicos",
            "bg-emerald-50 text-emerald-600",
            "bg-emerald-950/40 text-emerald-400",
        ),
        summary_card(
            "calendar-clock",
            "Período histórico",
            ResearchState.timeline_span,
            "Anos",
            "bg-amber-50 text-amber-600",
            "bg-amber-950/40 text-amber-400",
        ),
        summary_card(
            "history",
            "Histórico salvo",
            ResearchState.total_history,
            "Buscas",
            "bg-violet-50 text-violet-600",
            "bg-violet-950/40 text-violet-400",
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
    )