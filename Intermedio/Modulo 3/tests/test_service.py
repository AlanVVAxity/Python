from decimal import Decimal
from unittest.mock import Mock

import pytest

from modulo_03.order import OrderItem
from modulo_03.repository import OrderRepository
from modulo_03.service import OrderService


@pytest.mark.unit
def test_create_order_saves_order_in_repository() -> None:
    repository = Mock(spec=OrderRepository)
    service = OrderService(repository=repository)

    items = [
        OrderItem(
            product_name="Teclado",
            unit_price=Decimal("25.50"),
            quantity=2,
        )
    ]

    order = service.create_order(
        order_id="ORD-100",
        customer_email="cliente@example.com",
        items=items,
    )

    repository.save.assert_called_once_with(order)
    assert order.order_id == "ORD-100"
    assert order.customer_email == "cliente@example.com"
    assert order.total == Decimal("51.00")


@pytest.mark.unit
def test_create_order_returns_the_created_order() -> None:
    repository = Mock(spec=OrderRepository)
    service = OrderService(repository=repository)

    expected_items = [
        OrderItem(
            product_name="Mouse",
            unit_price=Decimal("15.00"),
            quantity=2,
        )
    ]

    result = service.create_order(
        order_id="ORD-101",
        customer_email="persona@example.com",
        items=expected_items,
    )

    assert result.order_id == "ORD-101"
    assert result.customer_email == "persona@example.com"
    assert result.items == expected_items
    assert result.total == Decimal("30.00")


@pytest.mark.unit
def test_create_order_does_not_save_when_order_is_invalid() -> None:
    repository = Mock(spec=OrderRepository)
    service = OrderService(repository=repository)

    with pytest.raises(ValueError):
        service.create_order(
            order_id="ORD-102",
            customer_email="correo-invalido",
            items=[],
        )

    repository.save.assert_not_called()
