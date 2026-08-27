"""Modelo de línea de orden."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modulo_01.models.base import Base

if TYPE_CHECKING:
    from modulo_01.models.order import Order


class OrderItem(Base):
    """Línea individual dentro de una orden."""

    __tablename__ = "order_items"
    __table_args__ = (
        UniqueConstraint("order_id", "sku", name="uq_order_item_sku"),
        CheckConstraint("cantidad > 0", name="ck_order_item_cantidad"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), index=True
    )
    sku: Mapped[str] = mapped_column(String(40))
    descripcion: Mapped[str] = mapped_column(String(200))
    cantidad: Mapped[int] = mapped_column()
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order: Mapped[Order] = relationship(back_populates="items")

    @property
    def subtotal(self) -> Decimal:
        """Precio unitario multiplicado por la cantidad."""
        return Decimal(self.precio_unitario) * self.cantidad

    def __repr__(self) -> str:
        return f"OrderItem(sku={self.sku!r}, cantidad={self.cantidad!r})"
