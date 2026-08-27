from typing import Protocol

from orders_service.domain.entities import Order


class OrderNotifier(Protocol):
    def order_created(self, order: Order) -> None: ...
