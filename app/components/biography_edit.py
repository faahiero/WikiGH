import reflex as rx
from app.states.research_state import ResearchState


def biography_edit_button(person) -> rx.Component:
    return rx.el.button(
        rx.icon("pencil", class_name="h-3.5 w-3.5"),
        "Editar",
        type="button",
        on_click=lambda: ResearchState.open_biography_edit(person["id"]),
        disabled=ResearchState.edit_busy,
        aria_label=f"Editar biografia de {person['name']} ({person['id']})",
        class_name=rx.cond(
            ResearchState.dark_mode,
            "inline-flex items-center gap-1 p-1.5 rounded-md text-xs font-medium text-blue-300 hover:bg-blue-950/40 focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50",
            "inline-flex items-center gap-1 p-1.5 rounded-md text-xs font-medium text-blue-700 hover:bg-blue-50 focus-visible:ring-2 focus-visible:ring-blue-600 disabled:opacity-50",
        ),
    )


def edit_field(field: str, label: str, hint: str, limit: int) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for=field,
            class_name=rx.cond(
                ResearchState.dark_mode,
                "block text-sm font-medium text-gray-100 mb-1",
                "block text-sm font-medium text-gray-900 mb-1",
            ),
        ),
        rx.el.input(
            id=field,
            name=field,
            type="text",
            default_value=ResearchState.edit_values[field],
            key=ResearchState.edit_values[field],
            max_length=limit,
            aria_describedby=f"{field}-help",
            class_name=rx.cond(
                ResearchState.dark_mode,
                "w-full rounded-lg border border-gray-700 bg-gray-950 text-gray-100 px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                "w-full rounded-lg border border-gray-300 bg-white text-gray-900 px-3 py-2 text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-600",
            ),
        ),
        rx.el.p(
            f"Antes desta edição: {ResearchState.edit_original[field]}",
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-xs text-gray-400 mt-1 break-words",
                "text-xs text-gray-600 mt-1 break-words",
            ),
        ),
        rx.el.p(
            hint,
            id=f"{field}-help",
            class_name=rx.cond(
                ResearchState.dark_mode,
                "text-xs text-gray-400 mt-1",
                "text-xs text-gray-600 mt-1",
            ),
        ),
        class_name="min-w-0",
    )


def biography_edit() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-[70] bg-black/60",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "Editar biografia",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "text-lg font-semibold text-gray-100",
                                "text-lg font-semibold text-gray-900",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-5 w-5"),
                            type="button",
                            aria_label="Cancelar edição e fechar",
                            on_click=ResearchState.cancel_biography_edit,
                            disabled=ResearchState.edit_busy,
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "rounded-lg p-2 text-gray-300 hover:bg-gray-800 focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50",
                                "rounded-lg p-2 text-gray-600 hover:bg-gray-100 focus-visible:ring-2 focus-visible:ring-blue-600 disabled:opacity-50",
                            ),
                        ),
                        class_name="flex items-center justify-between gap-3",
                    ),
                    rx.el.p(
                        ResearchState.edit_name,
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-sm font-semibold text-gray-100 mt-2 break-words",
                            "text-sm font-semibold text-gray-900 mt-2 break-words",
                        ),
                    ),
                    rx.el.p(
                        f"{ResearchState.edit_person_id} · {ResearchState.edit_context}",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-300 mt-1 break-words",
                            "text-xs text-gray-600 mt-1 break-words",
                        ),
                    ),
                    rx.el.p(
                        f"Artigo de origem: {ResearchState.edit_article_title}",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-400 mt-1 break-words",
                            "text-xs text-gray-600 mt-1 break-words",
                        ),
                    ),
                    rx.radix.primitives.dialog.description(
                        "Correção manual local: os valores abaixo são os dados atualmente salvos, não uma nova consulta à fonte. Salvar não altera a Wikipédia, o Wikidata nem a identidade e o resumo do artigo.",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "text-xs text-gray-300 mt-3 leading-relaxed",
                            "text-xs text-gray-600 mt-3 leading-relaxed",
                        ),
                    ),
                    class_name="shrink-0 px-5 pt-4 pb-3",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.fieldset(
                            edit_field(
                                "nationality",
                                "Nacionalidade",
                                "Até 240 caracteres. Vazio ou — indica não informado.",
                                240,
                            ),
                            rx.el.div(
                                edit_field(
                                    "birth_date",
                                    "Data de nascimento",
                                    "dd/mm/aaaa, mm/aaaa, aaaa ou YYYY-MM-DD. a.C.: 44 a.C. ou -0044.",
                                    40,
                                ),
                                edit_field(
                                    "death_date",
                                    "Data de falecimento",
                                    "Mesmos formatos. Vivo(a) mantém o status vivo; uma data remove esse status. Vazio: desconhecida.",
                                    40,
                                ),
                                class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                            ),
                            edit_field(
                                "birth_place",
                                "Local de nascimento",
                                "Até 240 caracteres. Alterar o local remove suas coordenadas antigas.",
                                240,
                            ),
                            edit_field(
                                "death_place",
                                "Local de falecimento",
                                "Até 240 caracteres. Para Vivo(a), deixe vazio ou —.",
                                240,
                            ),
                            disabled=ResearchState.edit_busy,
                            class_name="flex min-w-0 flex-col gap-4 disabled:opacity-70",
                        ),
                        rx.el.p(
                            rx.icon(
                                "map-pin-off",
                                class_name="h-4 w-4 shrink-0 mt-0.5",
                            ),
                            "Um local corrigido precisa de coordenadas correspondentes obtidas por nova extração antes de voltar ao mapa e às rotas. Uma reextração pode substituir as correções locais pelos dados da fonte.",
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "flex gap-2 text-xs leading-relaxed rounded-lg border border-blue-900 bg-blue-950/30 text-blue-200 p-3 mt-4",
                                "flex gap-2 text-xs leading-relaxed rounded-lg border border-blue-100 bg-blue-50 text-blue-800 p-3 mt-4",
                            ),
                        ),
                        rx.cond(
                            ResearchState.edit_error != "",
                            rx.el.p(
                                ResearchState.edit_error,
                                role="alert",
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "text-sm text-red-200 bg-red-950/40 border border-red-900 rounded-lg p-3 mt-3",
                                    "text-sm text-red-800 bg-red-50 border border-red-200 rounded-lg p-3 mt-3",
                                ),
                            ),
                            rx.fragment(),
                        ),
                        class_name="min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 py-3",
                    ),
                    rx.el.input(
                        type="hidden",
                        name="edit_version",
                        default_value=ResearchState.edit_version.to_string(),
                        key=ResearchState.edit_version.to_string(),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=ResearchState.cancel_biography_edit,
                            disabled=ResearchState.edit_busy,
                            class_name=rx.cond(
                                ResearchState.dark_mode,
                                "rounded-lg border border-gray-700 bg-gray-900 text-gray-200 px-4 py-2 text-sm hover:bg-gray-800 focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50",
                                "rounded-lg border border-gray-300 bg-white text-gray-700 px-4 py-2 text-sm hover:bg-gray-50 focus-visible:ring-2 focus-visible:ring-blue-600 disabled:opacity-50",
                            ),
                        ),
                        rx.el.button(
                            rx.cond(
                                ResearchState.edit_busy,
                                rx.icon(
                                    "loader-circle",
                                    class_name="h-4 w-4 animate-spin",
                                ),
                                rx.icon("save", class_name="h-4 w-4"),
                            ),
                            rx.cond(
                                ResearchState.edit_busy,
                                "Salvando…",
                                "Salvar correção",
                            ),
                            type="submit",
                            disabled=ResearchState.edit_busy,
                            class_name="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 text-white px-4 py-2 text-sm font-semibold hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:opacity-60",
                        ),
                        aria_live="polite",
                        class_name=rx.cond(
                            ResearchState.dark_mode,
                            "flex shrink-0 flex-wrap justify-end gap-2 border-t border-gray-800 bg-gray-900 px-5 py-4",
                            "flex shrink-0 flex-wrap justify-end gap-2 border-t border-gray-200 bg-white px-5 py-4",
                        ),
                    ),
                    on_submit=ResearchState.save_biography_edit,
                    reset_on_submit=False,
                    key=ResearchState.edit_version,
                    class_name="flex flex-1 min-h-0 flex-col",
                ),
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "fixed left-1/2 top-1/2 z-[71] flex max-h-[92dvh] w-[calc(100%_-_2rem)] max-w-xl -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-xl border border-gray-700 bg-gray-900 text-gray-100 font-['Inter'] focus:outline-hidden",
                    "fixed left-1/2 top-1/2 z-[71] flex max-h-[92dvh] w-[calc(100%_-_2rem)] max-w-xl -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-xl border border-gray-200 bg-white text-gray-900 font-['Inter'] focus:outline-hidden",
                ),
            ),
        ),
        open=ResearchState.edit_open,
        on_open_change=ResearchState.set_biography_edit_open,
    )
