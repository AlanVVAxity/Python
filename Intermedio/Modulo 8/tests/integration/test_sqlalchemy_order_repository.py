from decimal import Decimal

from modulo_08.domain.entities import Order
from modulo_08.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)


def test_sqlalchemy_repository_persists_order(
    sqlalchemy_repository: SqlAlchemyOrderRepository,
) -> None:
    order = Order.create(
        customer_email="cliente@example.com",
        product_name="Laptop",
        quantity=1,
        unit_price=Decimal("1299.99"),
    )

    sqlalchemy_repository.save(order)
    found_order = sqlalchemy_repository.get_by_id(order.id)

    assert found_order == order
    assert found_order is not None
    assert found_order.total_price == Decimal("1299.99")
