"""Demostración de uso del módulo: CRUD, transacciones y consultas."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from modulo_01.db import crear_engine, sesion_de
from modulo_01.models import OrderStatus
from modulo_01.queries import resumen_core, ventas_por_usuario
from modulo_01.repositories import LineaNueva, OrderRepository, UserRepository


def sembrar() -> None:
    """Crea usuarios y órdenes de ejemplo, si aún no existen."""
    engine = crear_engine()
    with sesion_de(engine) as session:
        usuarios = UserRepository(session)
        ordenes = OrderRepository(session)

        alan = usuarios.buscar_por_email("alan@example.com") or usuarios.crear(
            email="alan@example.com", nombre="Alan"
        )
        sofia = usuarios.buscar_por_email("sofia@example.com") or usuarios.crear(
            email="sofia@example.com", nombre="Sofia"
        )

        if ordenes.buscar_por_referencia("ORD-1001") is None:
            ordenes.crear(
                user_id=alan.id,
                referencia="ORD-1001",
                lineas=[
                    LineaNueva("TEC-01", "Teclado mecánico", 2, Decimal("250.00")),
                    LineaNueva("MOU-01", "Mouse inalámbrico", 1, Decimal("150.50")),
                ],
            )

        if ordenes.buscar_por_referencia("ORD-1002") is None:
            orden = ordenes.crear(
                user_id=sofia.id,
                referencia="ORD-1002",
                lineas=[LineaNueva("MON-01", 'Monitor 27"', 1, Decimal("4200.00"))],
            )
            ordenes.cambiar_estado(orden.id, OrderStatus.PAGADA)


def demostrar_transaccion() -> None:
    """Muestra que una transacción fallida no deja datos a medias."""
    engine = crear_engine()
    try:
        with sesion_de(engine) as session:
            usuarios = UserRepository(session)
            usuarios.crear(email="temporal@example.com", nombre="Temporal")
            usuarios.crear(email="alan@example.com", nombre="Duplicado")
    except IntegrityError:
        print("Transacción revertida: el email duplicado canceló todo el bloque.")

    with sesion_de(engine) as session:
        repetido = UserRepository(session).buscar_por_email("temporal@example.com")
        print("¿Quedó el usuario temporal?", repetido is not None)


def main() -> None:
    engine = crear_engine()
    sembrar()

    with sesion_de(engine) as session:
        for orden in OrderRepository(session).listar_por_usuario(1):
            print(orden.referencia, orden.estado.value, orden.total)

        print("\nVentas por usuario:")
        for email, total in ventas_por_usuario(session):
            print(f"  {email}: {total}")

    print("\nResumen con Core:")
    for fila in resumen_core(engine):
        print(" ", fila)

    print()
    demostrar_transaccion()


if __name__ == "__main__":
    main()
