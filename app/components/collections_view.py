import reflex as rx

from app.states.collections_state import (
    CollectionItem,
    CollectionPerson,
    CollectionsState,
)
from app.states.research_state import ResearchState


PANEL = rx.cond(
    ResearchState.dark_mode,
    "rounded-xl border border-gray-800 bg-gray-900 p-5 text-gray-100 min-w-0",
    "rounded-xl border border-gray-200 bg-white p-5 text-gray-900 min-w-0",
)
FIELD = rx.cond(
    ResearchState.dark_mode,
    "w-full rounded-lg border border-gray-700 bg-gray-950 px-3 py-2 text-sm text-gray-100 placeholder:text-gray-500 focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-blue-500",
    "w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 placeholder:text-gray-500 focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-blue-600",
)
MUTED = rx.cond(
    ResearchState.dark_mode,
    "text-xs text-gray-400 leading-relaxed",
    "text-xs text-gray-600 leading-relaxed",
)
ACTION = "inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
SECONDARY = rx.cond(
    ResearchState.dark_mode,
    "inline-flex items-center justify-center gap-2 rounded-lg border border-gray-700 bg-gray-900 px-3 py-2 text-xs font-medium text-gray-200 hover:bg-gray-800 focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50",
    "inline-flex items-center justify-center gap-2 rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs font-medium text-gray-700 hover:bg-gray-50 focus-visible:ring-2 focus-visible:ring-blue-600 disabled:opacity-50",
)


def collection_button(item: CollectionItem) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon("folder", class_name="h-4 w-4 shrink-0 text-blue-500"),
            rx.el.span(
                item["name"],
                class_name="font-semibold text-sm break-words flex-1 min-w-0",
            ),
            rx.el.span(item["count"], class_name="text-xs shrink-0"),
            class_name="flex items-center gap-2 w-full",
        ),
        rx.el.p(
            rx.cond(
                item["description"] != "", item["description"], "Sem descrição"
            ),
            class_name="text-xs mt-1 leading-relaxed break-words",
        ),
        rx.el.p(
            f"Criada em {item['created_at']}", class_name="text-[11px] mt-2"
        ),
        on_click=lambda: CollectionsState.run_operation(
            "select", item["id"], "", "", ""
        ),
        disabled=CollectionsState.busy,
        aria_pressed=CollectionsState.selected_collection_id == item["id"],
        key=item["id"],
        class_name=rx.cond(
            CollectionsState.selected_collection_id == item["id"],
            rx.cond(
                ResearchState.dark_mode,
                "w-full text-left rounded-lg border border-blue-900 bg-blue-950/40 text-blue-300 p-3 focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-60",
                "w-full text-left rounded-lg border border-blue-200 bg-blue-50 text-blue-800 p-3 focus-visible:ring-2 focus-visible:ring-blue-600 disabled:opacity-60",
            ),
            rx.cond(
                ResearchState.dark_mode,
                "w-full text-left rounded-lg border border-gray-800 bg-gray-950 text-gray-300 p-3 hover:border-blue-800 focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-60",
                "w-full text-left rounded-lg border border-gray-200 bg-gray-50 text-gray-700 p-3 hover:border-blue-300 focus-visible:ring-2 focus-visible:ring-blue-600 disabled:opacity-60",
            ),
        ),
    )


def create_collection_form() -> rx.Component:
    return rx.el.section(
        rx.el.h2("Nova coleção", class_name="text-sm font-bold mb-1"),
        rx.el.p(
            "Defina um tema e reúna biografias da sua composição.",
            class_name=MUTED,
        ),
        rx.el.form(
            rx.el.label(
                "Nome da coleção",
                html_for="collection-name",
                class_name="block text-xs font-semibold mb-1",
            ),
            rx.el.input(
                id="collection-name",
                name="name",
                placeholder="Ex.: Cientistas do século XX",
                required=True,
                max_length=160,
                class_name=FIELD,
            ),
            rx.el.label(
                "Descrição (opcional)",
                html_for="collection-description",
                class_name="block text-xs font-semibold mt-3 mb-1",
            ),
            rx.el.textarea(
                id="collection-description",
                name="description",
                placeholder="Qual é o recorte desta pesquisa?",
                max_length=2000,
                rows=3,
                class_name=FIELD,
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Criar coleção",
                type="submit",
                disabled=CollectionsState.busy,
                class_name=ACTION,
            ),
            on_submit=CollectionsState.create_collection,
            key=CollectionsState.form_version,
            class_name="flex flex-col gap-1 mt-4",
        ),
        class_name=PANEL,
    )


def member_card(person: CollectionPerson) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    person["name"],
                    class_name="text-sm font-semibold break-words",
                ),
                rx.el.p(person["context"], class_name=MUTED),
                rx.cond(
                    ~person["missing"],
                    rx.el.div(
                        rx.el.p(
                            f"Artigo: {person['article_title']}",
                            class_name="text-xs break-words",
                        ),
                        rx.el.p(person["dates"], class_name=MUTED),
                        rx.el.p(
                            f"Identificador: {person['id']}", class_name=MUTED
                        ),
                        rx.cond(
                            person["article_url"] != "",
                            rx.el.a(
                                rx.icon(
                                    "external-link", class_name="h-3.5 w-3.5"
                                ),
                                "Ler na Wikipédia",
                                href=person["article_url"],
                                target="_blank",
                                rel="noopener noreferrer",
                                class_name="inline-flex gap-1.5 items-center text-xs text-blue-600 dark:text-blue-400 font-medium mt-1 focus-visible:ring-2 focus-visible:ring-blue-500",
                            ),
                            rx.el.p(
                                "Link do artigo indisponível.", class_name=MUTED
                            ),
                        ),
                        class_name="mt-2 space-y-1",
                    ),
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.el.button(
                rx.icon("minus", class_name="h-3.5 w-3.5"),
                "Remover",
                on_click=lambda: CollectionsState.run_operation(
                    "remove",
                    CollectionsState.selected_collection_id,
                    person["id"],
                    "",
                    "",
                ),
                disabled=CollectionsState.busy,
                aria_label=f"Remover {person['name']} desta coleção",
                title="Remove apenas o vínculo; preserva a biografia",
                class_name=SECONDARY,
            ),
            class_name="flex flex-col sm:flex-row items-start gap-3",
        ),
        key=person["id"],
        class_name=rx.cond(
            ResearchState.dark_mode,
            "rounded-lg border border-gray-800 bg-gray-950 p-4 text-gray-200",
            "rounded-lg border border-gray-200 bg-gray-50 p-4 text-gray-800",
        ),
    )


def add_member_form() -> rx.Component:
    return rx.el.div(
        rx.cond(
            CollectionsState.people.length() == 0,
            rx.el.div(
                rx.el.p(
                    "Nenhuma biografia salva para adicionar.",
                    class_name="text-sm font-medium",
                ),
                rx.el.p(
                    "Busque um artigo e confirme a extração para salvar a primeira biografia.",
                    class_name=MUTED,
                ),
                rx.el.button(
                    rx.icon("search", class_name="h-4 w-4"),
                    "Buscar artigo",
                    on_click=ResearchState.set_active_view("research"),
                    class_name=SECONDARY,
                ),
                class_name="space-y-2",
            ),
            rx.cond(
                CollectionsState.available_people.length() == 0,
                rx.el.p(
                    "Todas as biografias salvas já fazem parte desta coleção.",
                    class_name=MUTED,
                ),
                rx.el.form(
                    rx.el.label(
                        "Adicionar biografia salva",
                        html_for="collection-person",
                        class_name="block text-xs font-semibold mb-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.select(
                                rx.el.option(
                                    "Selecione uma biografia…",
                                    value="",
                                    disabled=True,
                                ),
                                rx.foreach(
                                    CollectionsState.available_people,
                                    lambda p: rx.el.option(
                                        p["label"], value=p["id"], key=p["id"]
                                    ),
                                ),
                                name="person_id",
                                id="collection-person",
                                default_value="",
                                required=True,
                                disabled=CollectionsState.busy,
                                class_name=rx.cond(
                                    ResearchState.dark_mode,
                                    "w-full appearance-none rounded-lg border border-gray-700 bg-gray-950 py-2 pl-3 pr-9 text-sm text-gray-100 focus-visible:ring-2 focus-visible:ring-blue-500",
                                    "w-full appearance-none rounded-lg border border-gray-300 bg-white py-2 pl-3 pr-9 text-sm text-gray-900 focus-visible:ring-2 focus-visible:ring-blue-600",
                                ),
                            ),
                            rx.icon(
                                "chevron-down",
                                class_name="absolute right-3 top-3 h-4 w-4 pointer-events-none text-gray-500",
                            ),
                            class_name="relative flex-1 min-w-0",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="h-4 w-4"),
                            "Adicionar",
                            type="submit",
                            disabled=CollectionsState.busy,
                            class_name=ACTION,
                        ),
                        class_name="flex flex-col sm:flex-row gap-2",
                    ),
                    rx.el.p(
                        "Nome, contexto, artigo e identificador ajudam a distinguir homônimos.",
                        class_name=MUTED,
                    ),
                    on_submit=CollectionsState.add_person,
                    reset_on_submit=True,
                    key=CollectionsState.selected_collection_id,
                    class_name="space-y-2",
                ),
            ),
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "border-t border-b border-gray-800 py-4 my-4",
            "border-t border-b border-gray-200 py-4 my-4",
        ),
    )


def selected_collection_panel() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    CollectionsState.selected_collection["name"],
                    class_name="text-lg font-bold break-words",
                ),
                rx.cond(
                    CollectionsState.selected_collection["description"] != "",
                    rx.el.p(
                        CollectionsState.selected_collection["description"],
                        class_name="text-sm leading-relaxed text-justify mt-2 whitespace-pre-wrap break-words",
                    ),
                ),
                rx.el.p(
                    f"{CollectionsState.member_ids.length()} biografia(s) · Criada em {CollectionsState.selected_collection['created_at']}",
                    class_name=MUTED,
                ),
                class_name="flex-1 min-w-0 space-y-1",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                "Excluir coleção",
                on_click=CollectionsState.request_delete,
                disabled=CollectionsState.busy,
                class_name=SECONDARY,
            ),
            class_name="flex flex-col sm:flex-row gap-3 items-start justify-between",
        ),
        rx.cond(
            CollectionsState.confirm_delete,
            rx.el.div(
                rx.el.p(
                    "Excluir esta coleção e todos os seus vínculos? As biografias originais serão preservadas.",
                    class_name="text-sm",
                ),
                rx.el.div(
                    rx.el.button(
                        "Confirmar exclusão",
                        on_click=CollectionsState.delete_collection,
                        disabled=CollectionsState.busy,
                        class_name="rounded-lg bg-red-600 text-white px-3 py-2 text-xs font-semibold hover:bg-red-700 focus-visible:ring-2 focus-visible:ring-red-500",
                    ),
                    rx.el.button(
                        "Cancelar",
                        on_click=CollectionsState.cancel_delete,
                        class_name=SECONDARY,
                    ),
                    class_name="flex flex-wrap gap-2 mt-3",
                ),
                role="alert",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "rounded-lg border border-red-900 bg-red-950/40 text-red-200 p-4 mt-4",
                    "rounded-lg border border-red-200 bg-red-50 text-red-800 p-4 mt-4",
                ),
            ),
        ),
        add_member_form(),
        rx.el.h3(
            "Biografias desta coleção", class_name="text-sm font-semibold mb-3"
        ),
        rx.cond(
            CollectionsState.member_ids.length() > 0,
            rx.el.div(
                rx.foreach(CollectionsState.members, member_card),
                class_name="flex flex-col gap-3",
            ),
            rx.el.div(
                rx.icon("users", class_name="h-8 w-8 text-blue-500"),
                rx.el.p(
                    "Esta coleção ainda não tem biografias.",
                    class_name="text-sm font-medium",
                ),
                rx.el.p(
                    "Escolha um registro acima para começar a organizar seu tema.",
                    class_name=MUTED,
                ),
                class_name="flex flex-col items-center text-center gap-2 py-10",
            ),
        ),
        rx.el.p(
            "Remover um membro ou excluir a coleção não altera a composição original, o mapa ou as demais visualizações.",
            class_name=MUTED,
        ),
        class_name=PANEL,
    )


def collections_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("folders", class_name="h-5 w-5 text-blue-500"),
                rx.el.p(
                    "Organize suas pesquisas por tema",
                    class_name="text-sm font-semibold",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-4 w-4"),
                "Atualizar coleções",
                on_click=CollectionsState.reload_collections,
                disabled=CollectionsState.busy,
                class_name=SECONDARY,
            ),
            class_name="flex flex-wrap items-center justify-between gap-3",
        ),
        rx.el.p(
            "Suas coleções são privadas e vinculadas à sua conta. Uma biografia pode participar de várias coleções.",
            class_name=MUTED,
        ),
        rx.cond(
            CollectionsState.error != "",
            rx.el.p(
                CollectionsState.error,
                role="alert",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "rounded-lg border border-red-900 bg-red-950/40 text-red-200 p-3 text-sm",
                    "rounded-lg border border-red-200 bg-red-50 text-red-800 p-3 text-sm",
                ),
            ),
        ),
        rx.cond(
            CollectionsState.message != "",
            rx.el.p(
                CollectionsState.message,
                role="status",
                class_name=rx.cond(
                    ResearchState.dark_mode,
                    "rounded-lg border border-green-900 bg-green-950/40 text-green-200 p-3 text-sm",
                    "rounded-lg border border-green-200 bg-green-50 text-green-800 p-3 text-sm",
                ),
            ),
        ),
        rx.cond(
            CollectionsState.busy,
            rx.el.div(
                rx.icon(
                    "loader-circle",
                    class_name="h-4 w-4 animate-spin text-blue-500",
                ),
                "Atualizando coleções…",
                role="status",
                class_name="flex items-center gap-2 text-sm",
            ),
        ),
        rx.el.div(
            rx.el.div(
                create_collection_form(),
                rx.el.section(
                    rx.el.h2(
                        f"Minhas coleções ({CollectionsState.collections.length()})",
                        class_name="text-sm font-bold mb-3",
                    ),
                    rx.cond(
                        CollectionsState.collections.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                CollectionsState.collections, collection_button
                            ),
                            class_name="flex flex-col gap-2",
                        ),
                        rx.el.p(
                            rx.cond(
                                CollectionsState.loaded,
                                "Você ainda não criou nenhuma coleção. Use o formulário acima para definir seu primeiro tema.",
                                "Atualize a lista para carregar suas coleções.",
                            ),
                            class_name=MUTED,
                        ),
                    ),
                    class_name=PANEL,
                ),
                class_name="flex flex-col gap-4 min-w-0",
            ),
            rx.cond(
                CollectionsState.selected_collection_id > 0,
                selected_collection_panel(),
                rx.el.section(
                    rx.icon(
                        "folder-plus", class_name="h-10 w-10 text-blue-500"
                    ),
                    rx.el.h2(
                        "Seu próximo recorte histórico começa aqui",
                        class_name="text-lg font-bold",
                    ),
                    rx.el.p(
                        "Crie uma coleção com o tema da sua pesquisa. Depois, reúna biografias já salvas sem alterar os registros originais.",
                        class_name=MUTED,
                    ),
                    class_name=rx.cond(
                        ResearchState.dark_mode,
                        "flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-gray-700 bg-gray-900 p-8 text-center text-gray-100 min-h-64",
                        "flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-gray-300 bg-white p-8 text-center text-gray-900 min-h-64",
                    ),
                ),
            ),
            class_name="grid grid-cols-1 xl:grid-cols-[minmax(280px,1fr)_minmax(0,2fr)] gap-4 items-start w-full",
        ),
        class_name=rx.cond(
            ResearchState.dark_mode,
            "w-full space-y-4 text-gray-100",
            "w-full space-y-4 text-gray-900",
        ),
    )
