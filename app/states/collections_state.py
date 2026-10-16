import reflex as rx
import asyncio
import logging
import sqlite3
from contextlib import closing
from typing import Any, TypedDict

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError

from app.models import CollectionMembership, ThematicCollection
from app.states.research_state import DB_PATH


class CollectionItem(TypedDict):
    id: int
    name: str
    description: str
    created_at: str
    count: int


class CollectionPerson(TypedDict):
    id: str
    name: str
    context: str
    article_title: str
    article_url: str
    dates: str
    label: str
    missing: bool


class CollectionsState(rx.State):
    collections: list[CollectionItem] = []
    people: list[CollectionPerson] = []
    member_ids: list[str] = []
    selected_collection_id: int = 0
    busy: bool = False
    loaded: bool = False
    message: str = ""
    error: str = ""
    confirm_delete: bool = False
    form_version: int = 0
    _owner: str = ""
    _revision: int = 0

    def _clear(self):
        self.collections = []
        self.people = []
        self.member_ids = []
        self.selected_collection_id = 0
        self.busy = False
        self.loaded = False
        self.message = ""
        self.error = ""
        self.confirm_delete = False
        self.form_version += 1
        self._owner = ""
        self._revision += 1

    @rx.event
    def clear_account(self):
        self._clear()

    @rx.var
    def selected_collection(self) -> CollectionItem:
        return next(
            (
                c
                for c in self.collections
                if c["id"] == self.selected_collection_id
            ),
            {
                "id": 0,
                "name": "",
                "description": "",
                "created_at": "",
                "count": 0,
            },
        )

    @rx.var
    def members(self) -> list[CollectionPerson]:
        lookup = {p["id"]: p for p in self.people}
        return [
            lookup.get(
                pid,
                {
                    "id": pid,
                    "name": "Biografia indisponível",
                    "context": "O registro foi removido da composição original.",
                    "article_title": "",
                    "article_url": "",
                    "dates": "",
                    "label": pid,
                    "missing": True,
                },
            )
            for pid in self.member_ids
        ]

    @rx.var
    def available_people(self) -> list[CollectionPerson]:
        existing = set(self.member_ids)
        return [p for p in self.people if p["id"] not in existing]

    def _read_people(self) -> list[CollectionPerson]:
        from app.states.research_state import _format_br_date

        if not DB_PATH.is_file():
            return []
        with closing(
            sqlite3.connect(f"{DB_PATH.resolve().as_uri()}?mode=ro", uri=True)
        ) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                "SELECT id, name, occupation, description, nationality, article_title, article_url, birth_date, death_date FROM people ORDER BY name COLLATE NOCASE, id"
            ).fetchall()
        people: list[CollectionPerson] = []
        for row in rows:
            pid = str(row["id"] or "")
            if not pid:
                continue
            name = str(row["name"] or "Sem nome")
            title = str(row["article_title"] or name)
            context = str(
                row["occupation"]
                or row["description"]
                or row["nationality"]
                or "Contexto não informado"
            )
            birth = _format_br_date(str(row["birth_date"] or "—"))
            death = _format_br_date(str(row["death_date"] or "—"))
            dates = f"{birth} · {death}"
            people.append(
                {
                    "id": pid,
                    "name": name,
                    "context": context,
                    "article_title": title,
                    "article_url": str(row["article_url"] or "")
                    if str(row["article_url"] or "").startswith(
                        (
                            "https://pt.wikipedia.org/",
                            "http://pt.wikipedia.org/",
                        )
                    )
                    else "",
                    "dates": dates,
                    "label": f"{name} — {context} · {title} · {dates} [{pid}]",
                    "missing": False,
                }
            )
        return people

    def _database_operation(
        self,
        owner: str,
        action: str,
        collection_id: int,
        person_id: str,
        name: str,
        description: str,
    ) -> tuple[
        list[CollectionItem], list[str], list[CollectionPerson], int, str
    ]:
        if not owner:
            raise ValueError("Entre na sua conta para acessar as coleções.")
        if action not in {
            "load",
            "select",
            "create",
            "add",
            "remove",
            "delete",
        }:
            raise ValueError("Operação inválida.")
        if action in {"select", "add", "remove", "delete"} and (
            type(collection_id) is not int or collection_id <= 0
        ):
            raise ValueError("Selecione uma coleção válida.")
        if action in {"add", "remove"} and (
            not person_id
            or len(person_id) > 256
            or person_id.strip() != person_id
        ):
            raise ValueError("Selecione uma biografia válida.")
        if action == "create":
            name = name.strip()
            description = description.strip()
            if not name:
                raise ValueError("Informe um nome para a coleção.")
            if len(name) > 160:
                raise ValueError("O nome deve ter no máximo 160 caracteres.")
            if len(description) > 2000:
                raise ValueError(
                    "A descrição deve ter no máximo 2.000 caracteres."
                )
        people = self._read_people()
        if action == "add" and not any(p["id"] == person_id for p in people):
            raise ValueError(
                "Esta biografia não está mais salva. Pesquise e confirme o artigo antes de adicioná-la."
            )
        feedback = ""
        with rx.session() as session:
            try:
                owned_ids = select(ThematicCollection.id).where(
                    ThematicCollection.owner_user_id == owner
                )
                if action in {"select", "add", "remove", "delete"}:
                    collection = session.scalar(
                        select(ThematicCollection)
                        .where(
                            ThematicCollection.id == collection_id,
                            ThematicCollection.owner_user_id == owner,
                        )
                        .with_for_update()
                    )
                    if collection is None:
                        raise ValueError(
                            "Coleção não encontrada ou indisponível para esta conta. Atualize a lista."
                        )
                if action == "create":
                    duplicate = session.scalar(
                        select(ThematicCollection.id).where(
                            ThematicCollection.owner_user_id == owner,
                            func.lower(ThematicCollection.name) == name.lower(),
                        )
                    )
                    if duplicate is not None:
                        raise ValueError(
                            "Você já possui uma coleção com esse nome. Escolha outro nome."
                        )
                    collection = ThematicCollection(
                        owner_user_id=owner,
                        name=name,
                        description=description or None,
                    )
                    session.add(collection)
                    session.flush()
                    collection_id = collection.id
                    feedback = "Coleção criada. Agora você pode adicionar biografias salvas."
                elif action in {"add", "remove"}:
                    membership = session.scalar(
                        select(CollectionMembership).where(
                            CollectionMembership.collection_id.in_(owned_ids),
                            CollectionMembership.collection_id == collection_id,
                            CollectionMembership.person_id == person_id,
                        )
                    )
                    if action == "add":
                        if membership is not None:
                            raise ValueError(
                                "Esta biografia já faz parte da coleção."
                            )
                        session.add(
                            CollectionMembership(
                                collection_id=collection_id, person_id=person_id
                            )
                        )
                        feedback = "Biografia adicionada à coleção."
                    else:
                        if membership is None:
                            raise ValueError(
                                "Esta biografia não faz parte da coleção selecionada."
                            )
                        session.delete(membership)
                        feedback = "Biografia removida da coleção. O registro original foi preservado."
                elif action == "delete":
                    session.execute(
                        delete(CollectionMembership).where(
                            CollectionMembership.collection_id.in_(owned_ids),
                            CollectionMembership.collection_id == collection_id,
                        )
                    )
                    session.execute(
                        delete(ThematicCollection).where(
                            ThematicCollection.id == collection_id,
                            ThematicCollection.owner_user_id == owner,
                        )
                    )
                    collection_id = 0
                    feedback = (
                        "Coleção excluída. Nenhuma biografia foi apagada."
                    )
                if action in {"create", "add", "remove", "delete"}:
                    session.commit()
                rows = session.execute(
                    select(
                        ThematicCollection.id,
                        ThematicCollection.name,
                        ThematicCollection.description,
                        ThematicCollection.created_at,
                        func.count(CollectionMembership.id),
                    )
                    .outerjoin(
                        CollectionMembership,
                        CollectionMembership.collection_id
                        == ThematicCollection.id,
                    )
                    .where(ThematicCollection.owner_user_id == owner)
                    .group_by(ThematicCollection.id)
                    .order_by(
                        func.lower(ThematicCollection.name),
                        ThematicCollection.id,
                    )
                ).all()
                collections: list[CollectionItem] = [
                    {
                        "id": row[0],
                        "name": row[1],
                        "description": row[2] or "",
                        "created_at": row[3].strftime("%d/%m/%Y"),
                        "count": int(row[4]),
                    }
                    for row in rows
                ]
                if not any(c["id"] == collection_id for c in collections):
                    collection_id = collections[0]["id"] if collections else 0
                member_ids = (
                    list(
                        session.scalars(
                            select(CollectionMembership.person_id)
                            .where(
                                CollectionMembership.collection_id.in_(
                                    owned_ids
                                ),
                                CollectionMembership.collection_id
                                == collection_id,
                            )
                            .order_by(CollectionMembership.id)
                        ).all()
                    )
                    if collection_id
                    else []
                )
                return collections, member_ids, people, collection_id, feedback
            except Exception as e:
                session.rollback()
                logging.exception(f"Error: {e}")
                raise

    @rx.event
    async def create_collection(self, form_data: dict[str, Any]):
        name = str(form_data.get("name", ""))
        description = str(form_data.get("description", ""))
        yield CollectionsState.run_operation("create", 0, "", name, description)

    @rx.event
    async def add_person(self, form_data: dict[str, Any]):
        yield CollectionsState.run_operation(
            "add",
            self.selected_collection_id,
            str(form_data.get("person_id", "")),
            "",
            "",
        )

    @rx.event
    def request_delete(self):
        if not self.busy and self.selected_collection_id:
            self.confirm_delete = True

    @rx.event
    def cancel_delete(self):
        self.confirm_delete = False

    @rx.event
    def delete_collection(self):
        if self.confirm_delete:
            yield CollectionsState.run_operation(
                "delete", self.selected_collection_id, "", "", ""
            )

    @rx.event
    def reload_collections(self):
        yield CollectionsState.run_operation(
            "load", self.selected_collection_id, "", "", ""
        )

    @rx.event(background=True)
    async def run_operation(
        self,
        action: str,
        collection_id: int,
        person_id: str,
        name: str,
        description: str,
    ):
        from app.states.auth_state import AuthState

        async with self:
            auth = await self.get_state(AuthState)
            owner = auth.current_user["id"] if auth.is_authenticated else ""
            if not owner:
                self._clear()
                self.error = "Entre na sua conta para acessar as coleções."
                return
            if self._owner != owner:
                self._clear()
                self._owner = owner
            if self.busy:
                return
            self.busy = True
            self.error = ""
            self.message = ""
            self.confirm_delete = False
            self._revision += 1
            revision = self._revision
        try:
            result = await asyncio.to_thread(
                self._database_operation,
                owner,
                action,
                collection_id,
                person_id,
                name,
                description,
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            error = (
                str(e)
                if isinstance(e, ValueError)
                else (
                    "Esse nome ou vínculo já existe. Atualize a lista e tente novamente."
                    if isinstance(e, IntegrityError)
                    else "Não foi possível concluir a operação. Atualize as coleções para conferir os dados e tente novamente."
                )
            )
            async with self:
                auth = await self.get_state(AuthState)
                if (
                    self._revision == revision
                    and auth.is_authenticated
                    and auth.current_user["id"] == owner
                ):
                    self.error = error
                    self.busy = False
            return
        async with self:
            auth = await self.get_state(AuthState)
            if (
                self._revision != revision
                or not auth.is_authenticated
                or auth.current_user["id"] != owner
            ):
                return
            (
                self.collections,
                self.member_ids,
                self.people,
                self.selected_collection_id,
                self.message,
            ) = result
            self.loaded = True
            self.busy = False
            if action == "create":
                self.form_version += 1
