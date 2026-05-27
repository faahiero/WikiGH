import reflex as rx
import logging
import re
import hashlib
import secrets
import sqlite3
import asyncio
from pathlib import Path
from datetime import datetime
from typing import TypedDict


AUTH_DB_PATH = Path("geohist_auth.db")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def init_auth_db():
    try:
        conn = sqlite3.connect(AUTH_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        logging.exception(f"Erro ao inicializar banco de autenticação: {e}")


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}::{password}".encode("utf-8")).hexdigest()


def create_user_db(name: str, email: str, password: str) -> tuple[bool, str]:
    try:
        conn = sqlite3.connect(AUTH_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (email,)
        )
        if cursor.fetchone() is not None:
            conn.close()
            return False, "Já existe uma conta cadastrada com este e-mail."
        user_id = secrets.token_hex(8)
        salt = secrets.token_hex(16)
        password_hash = _hash_password(password, salt)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute(
            "INSERT INTO users (id, name, email, password_hash, salt, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, name, email, password_hash, salt, created_at),
        )
        conn.commit()
        conn.close()
        return True, user_id
    except Exception as e:
        logging.exception(f"Erro ao criar usuário: {e}")
        return False, "Erro inesperado ao criar a conta. Tente novamente."


def verify_user_db(email: str, password: str) -> tuple[bool, dict | str]:
    try:
        conn = sqlite3.connect(AUTH_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,)
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return False, "E-mail não cadastrado. Crie uma conta primeiro."
        expected = _hash_password(password, row["salt"])
        if expected != row["password_hash"]:
            return False, "Senha incorreta. Verifique e tente novamente."
        return True, {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "created_at": row["created_at"],
        }
    except Exception as e:
        logging.exception(f"Erro ao verificar usuário: {e}")
        return False, "Erro inesperado ao acessar a conta. Tente novamente."


def count_users_db() -> int:
    try:
        conn = sqlite3.connect(AUTH_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        conn.close()
        return int(result[0]) if result else 0
    except Exception as e:
        logging.exception(f"Erro ao contar usuários: {e}")
        return 0


class AuthUser(TypedDict):
    id: str
    name: str
    email: str
    created_at: str


class AuthState(rx.State):
    auth_mode: str = "login"  # "login" or "register"
    is_authenticated: bool = False
    current_user: AuthUser = {
        "id": "",
        "name": "",
        "email": "",
        "created_at": "",
    }
    is_submitting: bool = False
    auth_error: str = ""
    auth_success: str = ""
    total_users: int = 0
    auth_initialized: bool = False

    @rx.event
    async def init_auth(self):
        if self.auth_initialized:
            return
        await asyncio.to_thread(init_auth_db)
        self.total_users = await asyncio.to_thread(count_users_db)
        self.auth_initialized = True

    @rx.event
    def set_auth_mode(self, mode: str):
        self.auth_mode = mode
        self.auth_error = ""
        self.auth_success = ""

    @rx.event
    def clear_messages(self):
        self.auth_error = ""
        self.auth_success = ""

    @rx.event
    async def handle_register(self, form_data: dict):
        self.auth_error = ""
        self.auth_success = ""
        name = (form_data.get("name") or "").strip()
        email = (form_data.get("email") or "").strip()
        password = form_data.get("password") or ""
        confirm = form_data.get("confirm") or ""

        if not name or len(name) < 2:
            self.auth_error = "Informe seu nome completo (mínimo 2 caracteres)."
            return
        if not email or not EMAIL_RE.match(email):
            self.auth_error = "Informe um e-mail válido."
            return
        if len(password) < 6:
            self.auth_error = "A senha deve ter pelo menos 6 caracteres."
            return
        if password != confirm:
            self.auth_error = (
                "As senhas não coincidem. Verifique a confirmação."
            )
            return

        self.is_submitting = True
        yield
        ok, result = await asyncio.to_thread(
            create_user_db, name, email, password
        )
        self.is_submitting = False

        if not ok:
            self.auth_error = result
            yield rx.toast(
                title="Falha no cadastro",
                description=result,
                position="bottom-right",
                duration=4500,
                close_button=True,
            )
            return

        self.total_users = await asyncio.to_thread(count_users_db)
        self.auth_success = (
            f"Conta criada com sucesso! Faça login para continuar."
        )
        self.auth_mode = "login"
        yield rx.toast(
            title="Conta criada",
            description=f"Bem-vindo(a), {name}! Agora é só fazer login.",
            position="bottom-right",
            duration=4000,
            close_button=True,
        )

    @rx.event
    async def handle_login(self, form_data: dict):
        self.auth_error = ""
        self.auth_success = ""
        email = (form_data.get("email") or "").strip()
        password = form_data.get("password") or ""

        if not email or not EMAIL_RE.match(email):
            self.auth_error = "Informe um e-mail válido."
            return
        if not password:
            self.auth_error = "Informe sua senha."
            return

        self.is_submitting = True
        yield
        ok, result = await asyncio.to_thread(verify_user_db, email, password)
        self.is_submitting = False

        if not ok:
            self.auth_error = result
            yield rx.toast(
                title="Falha no login",
                description=result,
                position="bottom-right",
                duration=4500,
                close_button=True,
            )
            return

        self.current_user = result
        self.is_authenticated = True
        self.auth_success = ""
        yield rx.toast(
            title=f"Bem-vindo(a), {result['name']}!",
            description="Login realizado com sucesso.",
            position="bottom-right",
            duration=3500,
            close_button=True,
        )

    @rx.event
    async def logout(self):
        from app.states.research_state import ResearchState

        name = self.current_user.get("name", "")
        self.is_authenticated = False
        self.current_user = {
            "id": "",
            "name": "",
            "email": "",
            "created_at": "",
        }
        self.auth_mode = "login"
        self.auth_error = ""
        self.auth_success = ""
        # Return user to the public landing page after logout for cleaner UX
        research = await self.get_state(ResearchState)
        research.landing_mode = True
        research.active_view = "research"
        yield rx.toast(
            title="Sessão encerrada",
            description=f"Até logo, {name}!"
            if name
            else "Você saiu da sua conta.",
            position="bottom-right",
            duration=3000,
            close_button=True,
        )

    @rx.var
    def user_initials(self) -> str:
        name = self.current_user.get("name", "")
        if not name:
            return "?"
        parts = name.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return name[0].upper() if name else "?"