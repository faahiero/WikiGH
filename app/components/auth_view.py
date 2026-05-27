import reflex as rx
from app.states.auth_state import AuthState
from app.states.research_state import ResearchState


def _input(
    name: str,
    placeholder: str,
    type_: str = "text",
    icon: str = "",
    autocomplete: str = "",
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            icon != "",
            rx.icon(
                icon,
                class_name="h-4 w-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none",
            ),
            rx.fragment(),
        ),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=type_,
            auto_complete=autocomplete,
            required=True,
            class_name=rx.cond(
                icon != "",
                "w-full pl-10 pr-3 py-2.5 text-sm bg-white text-gray-900 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400",
                "w-full px-3.5 py-2.5 text-sm bg-white text-gray-900 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400",
            ),
        ),
        class_name="relative",
    )


def _form_label(label: str, hint: str = "") -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-semibold text-gray-700 mb-1.5",
        ),
        rx.cond(
            hint != "",
            rx.el.p(hint, class_name="text-[11px] text-gray-400 mb-1.5 -mt-1"),
            rx.fragment(),
        ),
    )


def login_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            _form_label("E-mail"),
            _input("email", "voce@exemplo.com", "email", "mail", "email"),
            class_name="mb-4",
        ),
        rx.el.div(
            _form_label("Senha"),
            _input(
                "password", "Sua senha", "password", "lock", "current-password"
            ),
            class_name="mb-5",
        ),
        rx.el.button(
            rx.cond(
                AuthState.is_submitting,
                rx.icon("loader-circle", class_name="h-4 w-4 animate-spin"),
                rx.icon("log-in", class_name="h-4 w-4"),
            ),
            rx.el.span(
                rx.cond(AuthState.is_submitting, "Entrando...", "Entrar"),
            ),
            type="submit",
            disabled=AuthState.is_submitting,
            class_name="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        on_submit=AuthState.handle_login,
        reset_on_submit=False,
    )


def register_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            _form_label("Nome completo"),
            _input("name", "Como devemos chamá-lo(a)", "text", "user", "name"),
            class_name="mb-4",
        ),
        rx.el.div(
            _form_label("E-mail"),
            _input("email", "voce@exemplo.com", "email", "mail", "email"),
            class_name="mb-4",
        ),
        rx.el.div(
            _form_label("Senha", "Mínimo de 6 caracteres."),
            _input(
                "password", "Crie uma senha", "password", "lock", "new-password"
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            _form_label("Confirmar senha"),
            _input(
                "confirm",
                "Repita a senha",
                "password",
                "shield",
                "new-password",
            ),
            class_name="mb-5",
        ),
        rx.el.button(
            rx.cond(
                AuthState.is_submitting,
                rx.icon("loader-circle", class_name="h-4 w-4 animate-spin"),
                rx.icon("user-plus", class_name="h-4 w-4"),
            ),
            rx.el.span(
                rx.cond(
                    AuthState.is_submitting, "Criando conta...", "Criar conta"
                ),
            ),
            type="submit",
            disabled=AuthState.is_submitting,
            class_name="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        on_submit=AuthState.handle_register,
        reset_on_submit=False,
    )


def auth_messages() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.auth_error != "",
            rx.el.div(
                rx.icon(
                    "circle-alert",
                    class_name="h-4 w-4 text-red-600 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    AuthState.auth_error,
                    class_name="text-xs text-red-800 leading-relaxed",
                ),
                class_name="flex items-start gap-2 p-3 rounded-lg bg-red-50 border border-red-200 mb-4",
            ),
            rx.fragment(),
        ),
        rx.cond(
            AuthState.auth_success != "",
            rx.el.div(
                rx.icon(
                    "circle-check-big",
                    class_name="h-4 w-4 text-emerald-600 shrink-0 mt-0.5",
                ),
                rx.el.p(
                    AuthState.auth_success,
                    class_name="text-xs text-emerald-800 leading-relaxed",
                ),
                class_name="flex items-start gap-2 p-3 rounded-lg bg-emerald-50 border border-emerald-200 mb-4",
            ),
            rx.fragment(),
        ),
    )


def auth_tabs() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Entrar",
            on_click=lambda: AuthState.set_auth_mode("login"),
            class_name=rx.cond(
                AuthState.auth_mode == "login",
                "flex-1 px-4 py-2 text-sm font-semibold text-blue-700 bg-white border border-gray-200 rounded-lg shadow-sm",
                "flex-1 px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 rounded-lg",
            ),
        ),
        rx.el.button(
            "Cadastrar",
            on_click=lambda: AuthState.set_auth_mode("register"),
            class_name=rx.cond(
                AuthState.auth_mode == "register",
                "flex-1 px-4 py-2 text-sm font-semibold text-blue-700 bg-white border border-gray-200 rounded-lg shadow-sm",
                "flex-1 px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 rounded-lg",
            ),
        ),
        class_name="flex gap-2 p-1 bg-gray-100 rounded-xl mb-6",
    )


def auth_view() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.button(
                    rx.icon("arrow-left", class_name="h-4 w-4"),
                    rx.el.span("Voltar"),
                    on_click=ResearchState.enter_landing,
                    class_name="inline-flex items-center gap-1.5 text-sm font-medium text-gray-600 hover:text-gray-900",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("globe", class_name="h-5 w-5 text-white"),
                        class_name="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center",
                    ),
                    rx.el.span(
                        "Wikipedia GeoHist",
                        class_name="text-lg font-extrabold tracking-tight text-gray-900",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="max-w-7xl mx-auto flex items-center justify-between px-6 h-16",
            ),
            class_name="border-b border-gray-200 bg-white",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Acesso à plataforma",
                        class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-100 text-xs font-semibold mb-4",
                    ),
                    rx.el.h1(
                        rx.cond(
                            AuthState.auth_mode == "login",
                            "Acesse sua conta",
                            "Crie sua conta",
                        ),
                        class_name="text-3xl font-extrabold text-gray-900 tracking-tight mb-2",
                    ),
                    rx.el.p(
                        rx.cond(
                            AuthState.auth_mode == "login",
                            "Entre com suas credenciais para retomar suas pesquisas biográficas.",
                            "Cadastre-se para começar a compor e mapear biografias da Wikipédia em português.",
                        ),
                        class_name="text-sm text-gray-600 mb-6",
                    ),
                    auth_tabs(),
                    auth_messages(),
                    rx.cond(
                        AuthState.auth_mode == "login",
                        login_form(),
                        register_form(),
                    ),
                    rx.el.div(
                        rx.cond(
                            AuthState.auth_mode == "login",
                            rx.el.p(
                                rx.el.span(
                                    "Ainda não tem conta? ",
                                    class_name="text-xs text-gray-500",
                                ),
                                rx.el.button(
                                    "Cadastre-se gratuitamente",
                                    on_click=lambda: AuthState.set_auth_mode(
                                        "register"
                                    ),
                                    class_name="text-xs font-semibold text-blue-600 hover:text-blue-700",
                                ),
                                class_name="text-center",
                            ),
                            rx.el.p(
                                rx.el.span(
                                    "Já tem uma conta? ",
                                    class_name="text-xs text-gray-500",
                                ),
                                rx.el.button(
                                    "Faça login",
                                    on_click=lambda: AuthState.set_auth_mode(
                                        "login"
                                    ),
                                    class_name="text-xs font-semibold text-blue-600 hover:text-blue-700",
                                ),
                                class_name="text-center",
                            ),
                        ),
                        class_name="mt-6 pt-5 border-t border-gray-100",
                    ),
                    class_name="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm",
                ),
                rx.el.p(
                    rx.icon(
                        "shield-check",
                        class_name="h-3.5 w-3.5 inline-block mr-1 text-gray-400",
                    ),
                    rx.el.span(
                        "Seus dados são armazenados localmente e protegidos com hash criptográfico.",
                        class_name="text-[11px] text-gray-500",
                    ),
                    class_name="text-center mt-5",
                ),
                class_name="max-w-md w-full mx-auto px-6 py-12",
            ),
            class_name="flex items-center justify-center min-h-[calc(100vh-4rem)] bg-gradient-to-b from-blue-50/40 via-white to-white",
        ),
        class_name="bg-gray-50 text-gray-900 w-full font-['Inter'] min-h-screen",
    )