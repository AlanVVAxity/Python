"""Modelo de orden."""

from __future__ import annotations

import enum
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modulo_01.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from modulo_01.models.order_item import OrderItem
    from modulo_01.models.user import User


class OrderStatus(enum.StrEnum):
    """Estados posibles de una orden."""

    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    CANCELADA = "CANCELADA"


class Order(Base, TimestampMixin):
    """Orden de compra asociada a un usuario."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    referencia: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    estado: Mapped[OrderStatus] = mapped_column(
        SAEnum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDIENTE,
    )

    user: Mapped[User] = relationship(back_populates="orders")
    items: Mapped[list[OrderItem]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def total(self) -> Decimal:
        """Suma de los subtotales de las líneas de la orden."""
        return sum((item.subtotal for item in self.items), Decimal("0.00"))

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, referencia={self.referencia!r})"
