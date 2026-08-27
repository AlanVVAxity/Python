from decimal import Decimal

import pytest

from modulo_05.application.order_service import OrderService
from modulo_05.application.ports import OrderRepository
from modulo_05.domain.order import Order


class FakeOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        return self.orders.get(order_id)

    def list_all(self) -> list[Order]:
        return list(self.orders.values())


def test_create_order_saves_and_returns_order() -> None:
    repository: OrderRepository = FakeOrderRepository()
    service = OrderService(repository)

    created_order = service.create_order(
        order_id="order-1",
        customer_name="Ana Pérez",
        total=Decimal("150.50"),
    )

    assert created_order == Order(
        id="order-1",
        customer_name="Ana Pérez",
        total=Decimal("150.50"),
    )
    assert repository.get_by_id("order-1") == created_order


def test_create_order_raises_error_when_id_already_exists() -> None:
    repository: OrderRepository = FakeOrderRepository()
    service = OrderService(repository)

    service.create_order(
        order_id="order-1",
        customer_name="Ana Pérez",
        total=Decimal("150.50"),
    )

    with pytest.raises(ValueError, match="Ya existe un pedido"):
        service.create_order(
            order_id="order-1",
            customer_name="Carlos Ruiz",
            total=Decimal("200.00"),
        )


def test_get_order_returns_none_when_order_does_not_exist() -> None:
    repository: OrderRepository = FakeOrderRepository()
    service = OrderService(repository)

    order = service.get_order("missing-order")

    assert order is None


def test_list_orders_returns_all_saved_orders() -> None:
    repository: OrderRepository = FakeOrderRepository()
    service = OrderService(repository)

    first_order = service.create_order(
        order_id="order-1",
        customer_name="Ana Pérez",
        total=Decimal("150.50"),
    )
    second_order = service.create_order(
        order_id="order-2",
        customer_name="Carlos Ruiz",
        total=Decimal("200.00"),
    )

    assert service.list_orders() == [first_order, second_order]
