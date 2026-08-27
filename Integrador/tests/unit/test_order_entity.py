from decimal import Decimal

import pytest

from orders_service.domain.entities import Order, OrderItem, OrderStatus
from orders_service.domain.exceptions import (
    InvalidOrderItemError,
    InvalidOrderStatusError,
)


def test_order_calculates_total() -> None:
    order = Order(
        customer_email="cliente@example.com",
        items=[
            OrderItem(
                product_name="Producto A",
                quantity=2,
                unit_price=Decimal("10.50"),
            ),
            OrderItem(
                product_name="Producto B",
                quantity=1,
                unit_price=Decimal("5.00"),
            ),
        ],
    )

    assert order.total == Decimal("26.00")


def test_order_can_be_marked_as_paid() -> None:
    order = Order(
        customer_email="cliente@example.com",
        items=[
            OrderItem(
                product_name="Producto A",
                quantity=1,
                unit_price=Decimal("10.00"),
            )
        ],
    )

    order.mark_as_paid()

    assert order.status == OrderStatus.PAID


def test_paid_order_cannot_be_cancelled() -> None:
    order = Order(
        customer_email="cliente@example.com",
        items=[
            OrderItem(
                product_name="Producto A",
                quantity=1,
                unit_price=Decimal("10.00"),
            )
        ],
    )

    order.mark_as_paid()

    with pytest.raises(InvalidOrderStatusError):
        order.cancel()


def test_order_item_requires_positive_quantity() -> None:
    with pytest.raises(InvalidOrderItemError):
        OrderItem(
            product_name="Producto A",
            quantity=0,
            unit_price=Decimal("10.00"),
        )
