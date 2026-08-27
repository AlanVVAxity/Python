"""Pruebas de las consultas agregadas."""

from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from modulo_01.models import OrderStatus
from modulo_01.queries import (
    conteo_crudo,
    ordenes_con_mas_de,
    resumen_core,
    total_de_orden,
    ventas_por_usuario,
)
from modulo_01.repositories import LineaNueva, OrderRepository, UserRepository


@pytest.fixture()
def poblado(session: Session) -> int:
    usuarios = UserRepository(session)
    ordenes = OrderRepository(session)

    alan = usuarios.crear(email="alan@example.com", nombre="Alan")
    sofia = usuarios.crear(email="sofia@example.com", nombre="Sofia")
    session.flush()

    orden_alan = ordenes.crear(
        user_id=alan.id,
        referencia="ORD-1001",
        lineas=[
            LineaNueva("TEC-01", "Teclado", 2, Decimal("250.00")),
            LineaNueva("MOU-01", "Mouse", 1, Decimal("150.50")),
        ],
    )
    orden_sofia = ordenes.crear(
        user_id=sofia.id,
        referencia="ORD-1002",
        lineas=[LineaNueva("MON-01", "Monitor", 1, Decimal("4200.00"))],
    )
    ordenes.cambiar_estado(orden_sofia.id, OrderStatus.CANCELADA)
    session.commit()
    return orden_alan.id


def test_total_de_orden(session: Session, poblado: int) -> None:
    assert total_de_orden(session, poblado) == Decimal("650.50")


def test_ventas_por_usuario_ignora_canceladas(session: Session, poblado: int) -> None:
    assert ventas_por_usuario(session) == [("alan@example.com", Decimal("650.50"))]


def test_ordenes_con_mas_de_una_linea(session: Session, poblado: int) -> None:
    resultado = ordenes_con_mas_de(session, 1)

    assert [orden.referencia for orden in resultado] == ["ORD-1001"]


def test_consultas_core(session: Session, engine: Engine, poblado: int) -> None:
    resumen = resumen_core(engine)

    assert len(resumen) == 2
    assert resumen[0]["referencia"] == "ORD-1001"
    assert conteo_crudo(engine) == 2
