from decimal import Decimal
from typing import Protocol
from uuid import UUID

import pytest
from sqlalchemy.orm import Session, sessionmaker

from modulo_08.domain.entities import Order
from modulo_08.infrastructure.repositories.memory_order_repository import (
    MemoryOrderRepository,
)
from modulo_08.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)


class OrderRepository(Protocol):
    def save(self, order: Order) -> Order: ...

    def get_by_id(self, order_id: UUID) -> Order | None: ...


@pytest.fixture(
    params=["memory", "sqlalchemy"],
    ids=["memory-repository", "sqlalchemy-repository"],
)
def repository(
    request: pytest.FixtureRequest,
    sqlite_session_factory: sessionmaker[Session],
) -> OrderRepository:
    if request.param == "memory":
        return MemoryOrderRepository()

    return SqlAlchemyOrderRepository(sqlite_session_factory)


def test_repository_saves_and_gets_an_order(repository: OrderRepository) -> None:
    order = Order.create(
        customer_email="cliente@example.com",
        product_name="Monitor",
        quantity=1,
        unit_price=Decimal("199.99"),
    )

    saved_order = repository.save(order)
    found_order = repository.get_by_id(order.id)

    assert saved_order == order
    assert found_order == order


def test_repository_returns_none_when_order_does_not_exist(
    repository: OrderRepository,
) -> None:
    unknown_order = Order.create(
        customer_email="otro@example.com",
        product_name="Producto temporal",
        quantity=1,
        unit_price=Decimal("1.00"),
    )

    assert repository.get_by_id(unknown_order.id) is None
