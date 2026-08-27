"""Pruebas de los modelos y sus relaciones."""

from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from modulo_01.models import Order, OrderItem, OrderStatus, User


def crear_usuario(session: Session, email: str = "alan@example.com") -> User:
    user = User(email=email, nombre="Alan")
    session.add(user)
    session.commit()
    return user


def test_orden_calcula_su_total(session: Session) -> None:
    user = crear_usuario(session)
    orden = Order(
        referencia="ORD-1",
        user=user,
        items=[
            OrderItem(
                sku="TEC-01",
                descripcion="Teclado",
                cantidad=2,
                precio_unitario=Decimal("250.00"),
            ),
            OrderItem(
                sku="MOU-01",
                descripcion="Mouse",
                cantidad=1,
                precio_unitario=Decimal("150.50"),
            ),
        ],
    )
    session.add(orden)
    session.commit()

    assert orden.total == Decimal("650.50")
    assert orden.estado is OrderStatus.PENDIENTE
    assert orden.user.email == "alan@example.com"


def test_email_duplicado_es_rechazado(session: Session) -> None:
    crear_usuario(session)
    session.add(User(email="alan@example.com", nombre="Otro"))

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_borrar_usuario_borra_sus_ordenes_e_items(session: Session) -> None:
    user = crear_usuario(session)
    session.add(
        Order(
            referencia="ORD-2",
            user=user,
            items=[
                OrderItem(
                    sku="MON-01",
                    descripcion="Monitor",
                    cantidad=1,
                    precio_unitario=Decimal("4200.00"),
                )
            ],
        )
    )
    session.commit()

    session.delete(user)
    session.commit()

    assert session.scalar(select(func.count()).select_from(Order)) == 0
    assert session.scalar(select(func.count()).select_from(OrderItem)) == 0


def test_sku_repetido_en_la_misma_orden_es_rechazado(session: Session) -> None:
    user = crear_usuario(session)
    session.add(
        Order(
            referencia="ORD-3",
            user=user,
            items=[
                OrderItem(
                    sku="TEC-01",
                    descripcion="Teclado",
                    cantidad=1,
                    precio_unitario=Decimal("250.00"),
                ),
                OrderItem(
                    sku="TEC-01",
                    descripcion="Teclado repetido",
                    cantidad=1,
                    precio_unitario=Decimal("250.00"),
                ),
            ],
        )
    )

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()
