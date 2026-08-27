"""Modelo de usuario."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modulo_01.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from modulo_01.models.order import Order


class User(Base, TimestampMixin):
    """Persona que realiza órdenes."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120))
    activo: Mapped[bool] = mapped_column(default=True)
    telefono: Mapped[str | None] = mapped_column(String(20), default=None)

    orders: Mapped[list[Order]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
