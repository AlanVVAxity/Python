import sqlite3
from collections.abc import Callable
from decimal import Decimal
from typing import Protocol

import pytest

from modulo_05.domain.order import Order
from modulo_05.infrastructure.in_memory_order_repository import (
    InMemoryOrderRepository,
)
from modulo_05.infrastructure.sqlite_order_repository import SQLiteOrderRepository


class RepositoryFactory(Protocol):
    def __call__(self) -> "Repository": ...


class Repository(Protocol):
    def save(self, order: Order) -> None: ...

    def get_by_id(self, order_id: str) -> Order | None: ...

    def list_all(self) -> list[Order]: ...


@pytest.fixture(params=["memory", "sqlite"])
def repository(request: pytest.FixtureRequest) -> Repository:
    if request.param == "memory":
        return InMemoryOrderRepository()

    connection = sqlite3.connect(":memory:")
    return SQLiteOrderRepository(connection)


@pytest.fixture
def order_factory() -> Callable[[str, str, str], Order]:
    def create_order(
        order_id: str = "order-1",
        customer_name: str = "Alan Vazquez",
        total: str = "150.50",
    ) -> Order:
        return Order(
            id=order_id,
            customer_name=customer_name,
            total=Decimal(total),
        )

    return create_order
