from decimal import Decimal

import pytest

from modulo_03.order import Order, OrderItem


@pytest.mark.unit
def test_order_item_calculates_subtotal() -> None:
    item = OrderItem(
        product_name="Teclado",
        unit_price=Decimal("25.50"),
        quantity=2,
    )

    assert item.subtotal == Decimal("51.00")


@pytest.mark.unit
def test_order_calculates_total_from_its_items() -> None:
    order = Order(
        order_id="ORD-001",
        customer_email="cliente@example.com",
        items=[
            OrderItem(
                product_name="Teclado",
                unit_price=Decimal("25.50"),
                quantity=2,
            ),
            OrderItem(
                product_name="Mouse",
                unit_price=Decimal("10.00"),
                quantity=1,
            ),
        ],
    )

    assert order.total == Decimal("61.00")


@pytest.mark.unit
@pytest.mark.parametrize(
    ("unit_price", "quantity"),
    [
        (Decimal("0.00"), 1),
        (Decimal("-1.00"), 1),
        (Decimal("10.00"), 0),
        (Decimal("10.00"), -1),
    ],
)
def test_order_item_rejects_invalid_price_or_quantity(
    unit_price: Decimal,
    quantity: int,
) -> None:
    with pytest.raises(ValueError):
        OrderItem(
            product_name="Producto",
            unit_price=unit_price,
            quantity=quantity,
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    "customer_email",
    [
        "",
        "correo-sin-arroba",
        "@example.com",
        "cliente@",
    ],
)
def test_order_rejects_invalid_customer_email(customer_email: str) -> None:
    with pytest.raises(ValueError):
        Order(
            order_id="ORD-001",
            customer_email=customer_email,
            items=[],
        )


@pytest.mark.unit
def test_order_rejects_empty_order_id() -> None:
    with pytest.raises(ValueError):
        Order(
            order_id="",
            customer_email="cliente@example.com",
            items=[],
        )


@pytest.mark.unit
def test_order_item_rejects_empty_product_name() -> None:
    with pytest.raises(ValueError):
        OrderItem(
            product_name="   ",
            unit_price=Decimal("10.00"),
            quantity=1,
        )


@pytest.mark.unit
def test_order_with_no_items_has_zero_total() -> None:
    order = Order(
        order_id="ORD-EMPTY",
        customer_email="cliente@example.com",
        items=[],
    )

    assert order.total == Decimal("0.00")
