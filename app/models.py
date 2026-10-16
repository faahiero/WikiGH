import reflex as rx
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class ThematicCollection(Base):
    __tablename__ = "thematic_collection"
    __table_args__ = (
        UniqueConstraint(
            "owner_user_id", "name", name="uq_thematic_collection_owner_name"
        ),
        CheckConstraint(
            "length(trim(owner_user_id)) > 0",
            name="ck_thematic_collection_owner_required",
        ),
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_thematic_collection_name_required",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    owner_user_id: Mapped[str] = mapped_column(
        String, nullable=False, index=True, server_default=""
    )
    name: Mapped[str] = mapped_column(String, nullable=False, server_default="")
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )


class CollectionMembership(Base):
    __tablename__ = "collection_membership"
    __table_args__ = (
        UniqueConstraint(
            "collection_id",
            "person_id",
            name="uq_collection_membership_collection_person",
        ),
        CheckConstraint(
            "length(trim(person_id)) > 0",
            name="ck_collection_membership_person_required",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    collection_id: Mapped[int] = mapped_column(
        ForeignKey("thematic_collection.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        server_default="0",
    )
    person_id: Mapped[str] = mapped_column(
        String, nullable=False, index=True, server_default=""
    )
