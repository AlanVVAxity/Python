import sqlite3
from decimal import Decimal

from modulo_05.domain.order import Order
from modulo_05.infrastructure.sqlite_order_repository import SQLiteOrderRepository


def test_sqlite_repository_lists_orders_sorted_by_id() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SQLiteOrderRepository(connection)

    order_b = Order(
        id="order-b",
        customer_name="Carlos Ruiz",
        total=Decimal("200.00"),
    )
    order_a = Order(
        id="order-a",
        customer_name="Ana Pérez",
        total=Decimal("150.50"),
    )

    repository.save(order_b)
    repository.save(order_a)

    assert repository.list_all() == [order_a, order_b]
