from typing import Protocol

from modulo_05.domain.order import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...

    def get_by_id(self, order_id: str) -> Order | None: ...

    def list_all(self) -> list[Order]: ...
