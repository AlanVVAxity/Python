"""Operaciones de persistencia sobre órdenes."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from modulo_01.models import Order, OrderItem, OrderStatus


@dataclass(frozen=True)
class LineaNueva:
    """Datos de entrada para crear una línea de orden."""

    sku: str
    descripcion: str
    cantidad: int
    precio_unitario: Decimal


class OrderRepository:
    """CRUD de órdenes sobre una sesión de SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def crear(
        self,
        *,
        user_id: int,
        referencia: str,
        lineas: Sequence[LineaNueva],
    ) -> Order:
        if not lineas:
            raise ValueError("Una orden necesita al menos una línea.")

        orden = Order(
            referencia=referencia,
            user_id=user_id,
            items=[
                OrderItem(
                    sku=linea.sku,
                    descripcion=linea.descripcion,
                    cantidad=linea.cantidad,
                    precio_unitario=linea.precio_unitario,
                )
                for linea in lineas
            ],
        )
        self._session.add(orden)
        self._session.flush()
        return orden

    def obtener(self, order_id: int) -> Order | None:
        stmt = (
            select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
        )
        return self._session.scalar(stmt)

    def buscar_por_referencia(self, referencia: str) -> Order | None:
        stmt = select(Order).where(Order.referencia == referencia)
        return self._session.scalar(stmt)

    def listar_por_usuario(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.id)
            .options(selectinload(Order.items))
        )
        return list(self._session.scalars(stmt))

    def cambiar_estado(self, order_id: int, estado: OrderStatus) -> Order | None:
        orden = self.obtener(order_id)
        if orden is None:
            return None
        orden.estado = estado
        self._session.flush()
        return orden

    def eliminar(self, order_id: int) -> bool:
        orden = self.obtener(order_id)
        if orden is None:
            return False
        self._session.delete(orden)
        self._session.flush()
        return True
