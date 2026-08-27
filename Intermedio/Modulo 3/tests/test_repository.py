from decimal import Decimal

import pytest

from modulo_03.order import Order, OrderItem
from modulo_03.repository import InMemoryOrderRepository


@pytest.mark.unit
def test_repository_saves_and_gets_order_by_id() -> None:
    repository = InMemoryOrderRepository()
    order = Order(
        order_id="ORD-200",
        customer_email="cliente@example.com",
        items=[
            OrderItem(
                product_name="Monitor",
                unit_price=Decimal("250.00"),
                quantity=1,
            )
        ],
    )

    repository.save(order)

    result = repository.get_by_id("ORD-200")

    assert result == order


@pytest.mark.unit
def test_repository_returns_none_when_order_does_not_exist() -> None:
    repository = InMemoryOrderRepository()

    result = repository.get_by_id("ORD-NOT-FOUND")

    assert result is None


@pytest.mark.unit
def test_repository_lists_all_saved_orders() -> None:
    repository = InMemoryOrderRepository()

    first_order = Order(
        order_id="ORD-201",
        customer_email="primero@example.com",
        items=[
            OrderItem(
                product_name="Teclado",
                unit_price=Decimal("20.00"),
                quantity=1,
            )
        ],
    )
    second_order = Order(
        order_id="ORD-202",
        customer_email="segundo@example.com",
        items=[
            OrderItem(
                product_name="Mouse",
                unit_price=Decimal("15.00"),
                quantity=2,
            )
        ],
    )

    repository.save(first_order)
    repository.save(second_order)

    assert repository.list_all() == [first_order, second_order]


@pytest.mark.unit
def test_repository_replaces_order_when_id_already_exists() -> None:
    repository = InMemoryOrderRepository()

    original_order = Order(
        order_id="ORD-203",
        customer_email="original@example.com",
        items=[
            OrderItem(
                product_name="Producto original",
                unit_price=Decimal("10.00"),
                quantity=1,
            )
        ],
    )
    replacement_order = Order(
        order_id="ORD-203",
        customer_email="nuevo@example.com",
        items=[
            OrderItem(
                product_name="Producto nuevo",
                unit_price=Decimal("30.00"),
                quantity=1,
            )
        ],
    )

    repository.save(original_order)
    repository.save(replacement_order)

    assert repository.get_by_id("ORD-203") == replacement_order
    assert repository.list_all() == [replacement_order]


@pytest.mark.unit
def test_repository_is_iterable() -> None:
    repository = InMemoryOrderRepository()
    order = Order(
        order_id="ORD-204",
        customer_email="iterable@example.com",
        items=[
            OrderItem(
                product_name="Laptop",
                unit_price=Decimal("1000.00"),
                quantity=1,
            )
        ],
    )

    repository.save(order)

    assert list(repository) == [order]
