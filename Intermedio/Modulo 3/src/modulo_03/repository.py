from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Protocol

from modulo_03.order import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        """Guarda un pedido."""

    def get_by_id(self, order_id: str) -> Order | None:
        """Obtiene un pedido por su identificador."""

    def list_all(self) -> list[Order]:
        """Obtiene todos los pedidos guardados."""


@dataclass
class InMemoryOrderRepository:
    _orders: dict[str, Order] = field(default_factory=dict)

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def list_all(self) -> list[Order]:
        return list(self._orders.values())

    def __iter__(self) -> Iterator[Order]:
        return iter(self._orders.values())
