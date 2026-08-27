"""Consultas de lectura con el ORM y con SQLAlchemy Core."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Engine, func, select, text
from sqlalchemy.orm import Session

from modulo_01.models import Order, OrderItem, OrderStatus, User


def total_de_orden(session: Session, order_id: int) -> Decimal:
    """Calcula el total de una orden directamente en la base de datos."""
    stmt = select(
        func.coalesce(func.sum(OrderItem.cantidad * OrderItem.precio_unitario), 0)
    ).where(OrderItem.order_id == order_id)
    return Decimal(str(session.scalar(stmt)))


def ventas_por_usuario(session: Session) -> list[tuple[str, Decimal]]:
    """Devuelve el importe vendido por usuario, sin contar órdenes canceladas."""
    subtotal = OrderItem.cantidad * OrderItem.precio_unitario
    stmt = (
        select(User.email, func.coalesce(func.sum(subtotal), 0).label("total"))
        .join(Order, Order.user_id == User.id)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .where(Order.estado != OrderStatus.CANCELADA)
        .group_by(User.email)
        .order_by(func.sum(subtotal).desc())
    )
    return [(email, Decimal(str(total))) for email, total in session.execute(stmt)]


def ordenes_con_mas_de(session: Session, minimo: int) -> list[Order]:
    """Órdenes que tienen más de `minimo` líneas."""
    stmt = (
        select(Order)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .group_by(Order.id)
        .having(func.count(OrderItem.id) > minimo)
        .order_by(Order.id)
    )
    return list(session.scalars(stmt))


def resumen_core(engine: Engine) -> list[dict[str, object]]:
    """Mismo resumen, pero con SQLAlchemy Core (sin instanciar objetos)."""
    ordenes = Order.__table__
    items = OrderItem.__table__
    stmt = (
        select(
            ordenes.c.referencia,
            func.count(items.c.id).label("lineas"),
            func.coalesce(
                func.sum(items.c.cantidad * items.c.precio_unitario), 0
            ).label("total"),
        )
        .select_from(ordenes.join(items, items.c.order_id == ordenes.c.id))
        .group_by(ordenes.c.referencia)
        .order_by(ordenes.c.referencia)
    )
    with engine.connect() as conexion:
        return [dict(fila._mapping) for fila in conexion.execute(stmt)]


def conteo_crudo(engine: Engine) -> int:
    """Ejemplo de SQL textual parametrizable con `text()`."""
    with engine.connect() as conexion:
        return conexion.execute(text("SELECT COUNT(*) FROM orders")).scalar_one()
