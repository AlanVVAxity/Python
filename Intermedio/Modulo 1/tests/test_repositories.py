"""Pruebas del CRUD de los repositorios."""

from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from modulo_01.models import OrderStatus
from modulo_01.repositories import LineaNueva, OrderRepository, UserRepository


@pytest.fixture()
def datos(session: Session) -> tuple[UserRepository, OrderRepository, int]:
    usuarios = UserRepository(session)
    ordenes = OrderRepository(session)
    user = usuarios.crear(email="alan@example.com", nombre="Alan")
    session.commit()
    return usuarios, ordenes, user.id


def test_crear_y_obtener_orden(
    session: Session, datos: tuple[UserRepository, OrderRepository, int]
) -> None:
    _, ordenes, user_id = datos
    creada = ordenes.crear(
        user_id=user_id,
        referencia="ORD-1001",
        lineas=[LineaNueva("TEC-01", "Teclado", 2, Decimal("250.00"))],
    )
    session.commit()

    recuperada = ordenes.obtener(creada.id)

    assert recuperada is not None
    assert recuperada.referencia == "ORD-1001"
    assert len(recuperada.items) == 1
    assert recuperada.total == Decimal("500.00")


def test_crear_sin_lineas_falla(
    datos: tuple[UserRepository, OrderRepository, int],
) -> None:
    _, ordenes, user_id = datos

    with pytest.raises(ValueError, match="al menos una línea"):
        ordenes.crear(user_id=user_id, referencia="ORD-VACIA", lineas=[])


def test_cambiar_estado(
    session: Session, datos: tuple[UserRepository, OrderRepository, int]
) -> None:
    _, ordenes, user_id = datos
    orden = ordenes.crear(
        user_id=user_id,
        referencia="ORD-1002",
        lineas=[LineaNueva("MON-01", "Monitor", 1, Decimal("4200.00"))],
    )
    session.commit()

    actualizada = ordenes.cambiar_estado(orden.id, OrderStatus.PAGADA)
    session.commit()

    assert actualizada is not None
    assert actualizada.estado is OrderStatus.PAGADA


def test_eliminar_orden(
    session: Session, datos: tuple[UserRepository, OrderRepository, int]
) -> None:
    _, ordenes, user_id = datos
    orden = ordenes.crear(
        user_id=user_id,
        referencia="ORD-1003",
        lineas=[LineaNueva("MOU-01", "Mouse", 1, Decimal("150.50"))],
    )
    session.commit()

    assert ordenes.eliminar(orden.id) is True
    session.commit()
    assert ordenes.obtener(orden.id) is None
    assert ordenes.eliminar(9999) is False


def test_listar_usuarios_activos(
    session: Session, datos: tuple[UserRepository, OrderRepository, int]
) -> None:
    usuarios, _, user_id = datos
    usuarios.crear(email="sofia@example.com", nombre="Sofia")
    usuarios.desactivar(user_id)
    session.commit()

    activos = usuarios.listar(solo_activos=True)

    assert [u.email for u in activos] == ["sofia@example.com"]
