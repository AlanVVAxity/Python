from decimal import Decimal

import pytest

from modulo_08.domain.entities import Order
from modulo_08.domain.exceptions import InvalidOrderError
from modulo_08.domain.value_objects import OrderStatus


def test_create_order_creates_pending_order() -> None:
    order = Order.create(
        customer_email="cliente@example.com",
        product_name="Teclado mecánico",
        quantity=2,
        unit_price=Decimal("49.90"),
    )

    assert order.customer_email == "cliente@example.com"
    assert order.product_name == "Teclado mecánico"
    assert order.quantity == 2
    assert order.unit_price == Decimal("49.90")
    assert order.total_price == Decimal("99.80")
    assert order.status == OrderStatus.PENDING
    assert order.id is not None
    assert order.created_at is not None


@pytest.mark.parametrize(
    ("customer_email", "expected_message"),
    [
        ("", "El correo del cliente es obligatorio."),
        ("correo-invalido", "El correo del cliente no tiene un formato válido."),
    ],
)
def test_create_order_rejects_invalid_customer_email(
    customer_email: str,
    expected_message: str,
) -> None:
    with pytest.raises(InvalidOrderError, match=expected_message):
        Order.create(
            customer_email=customer_email,
            product_name="Teclado mecánico",
            quantity=1,
            unit_price=Decimal("49.90"),
        )


def test_create_order_rejects_empty_product_name() -> None:
    with pytest.raises(
        InvalidOrderError,
        match="El nombre del producto es obligatorio.",
    ):
        Order.create(
            customer_email="cliente@example.com",
            product_name="   ",
            quantity=1,
            unit_price=Decimal("49.90"),
        )


def test_create_order_rejects_non_positive_quantity() -> None:
    with pytest.raises(
        InvalidOrderError,
        match="La cantidad debe ser mayor que cero.",
    ):
        Order.create(
            customer_email="cliente@example.com",
            product_name="Teclado mecánico",
            quantity=0,
            unit_price=Decimal("49.90"),
        )


def test_create_order_rejects_non_positive_unit_price() -> None:
    with pytest.raises(
        InvalidOrderError,
        match="El precio unitario debe ser mayor que cero.",
    ):
        Order.create(
            customer_email="cliente@example.com",
            product_name="Teclado mecánico",
            quantity=1,
            unit_price=Decimal("0"),
        )
