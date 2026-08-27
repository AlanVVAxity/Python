from collections.abc import Callable

from modulo_05.application.ports import OrderRepository
from modulo_05.domain.order import Order


def test_save_and_get_order(
    repository: OrderRepository,
    order_factory: Callable[..., Order],
) -> None:
    order = order_factory()

    repository.save(order)

    assert repository.get_by_id(order.id) == order


def test_get_by_id_returns_none_for_unknown_order(
    repository: OrderRepository,
) -> None:
    assert repository.get_by_id("unknown-order") is None


def test_list_all_returns_saved_orders(
    repository: OrderRepository,
    order_factory: Callable[..., Order],
) -> None:
    first_order = order_factory(
        order_id="order-1",
        customer_name="Ana Pérez",
        total="150.50",
    )
    second_order = order_factory(
        order_id="order-2",
        customer_name="Carlos Ruiz",
        total="200.00",
    )

    repository.save(first_order)
    repository.save(second_order)

    assert repository.list_all() == [first_order, second_order]


def test_save_updates_existing_order(
    repository: OrderRepository,
    order_factory: Callable[..., Order],
) -> None:
    original_order = order_factory(
        order_id="order-1",
        customer_name="Ana Pérez",
        total="150.50",
    )
    updated_order = order_factory(
        order_id="order-1",
        customer_name="Ana Pérez Actualizada",
        total="300.00",
    )

    repository.save(original_order)
    repository.save(updated_order)

    assert repository.get_by_id("order-1") == updated_order
    assert repository.list_all() == [updated_order]
