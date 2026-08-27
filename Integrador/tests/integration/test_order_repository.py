from decimal import Decimal

from orders_service.domain.entities import Order, OrderItem, OrderStatus
from orders_service.infrastructure.db.repositories import SqlAlchemyOrderRepository


def test_repository_saves_and_retrieves_order(db_session) -> None:
    repository = SqlAlchemyOrderRepository(db_session)

    order = Order(
        customer_email="cliente@example.com",
        items=[
            OrderItem(
                product_name="Producto A",
                quantity=2,
                unit_price=Decimal("15.00"),
            )
        ],
    )

    saved_order = repository.add(order)
    found_order = repository.get_by_id(saved_order.id)

    assert found_order is not None
    assert found_order.id == saved_order.id
    assert found_order.customer_email == "cliente@example.com"
    assert found_order.status == OrderStatus.PENDING
    assert found_order.total == Decimal("30.00")
