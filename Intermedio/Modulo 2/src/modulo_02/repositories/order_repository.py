from uuid import UUID

from modulo_02.schemas.order import OrderResponse


class OrderRepository:
    def __init__(self) -> None:
        self._orders: dict[UUID, OrderResponse] = {}

    def create(self, order: OrderResponse) -> OrderResponse:
        self._orders[order.id] = order
        return order

    def get_by_id(self, order_id: UUID) -> OrderResponse | None:
        return self._orders.get(order_id)

    def get_all(self) -> list[OrderResponse]:
        return list(self._orders.values())

    def update(self, order: OrderResponse) -> OrderResponse:
        self._orders[order.id] = order
        return order

    def delete(self, order_id: UUID) -> bool:
        if order_id not in self._orders:
            return False

        del self._orders[order_id]
        return True