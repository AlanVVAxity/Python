from uuid import UUID

from modulo_08.domain.entities import Order


class MemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[UUID, Order] = {}

    def save(self, order: Order) -> Order:
        self._orders[order.id] = order
        return order

    def get_by_id(self, order_id: UUID) -> Order | None:
        return self._orders.get(order_id)
