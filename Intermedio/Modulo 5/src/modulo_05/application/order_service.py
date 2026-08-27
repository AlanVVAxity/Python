from decimal import Decimal

from modulo_05.application.ports import OrderRepository
from modulo_05.domain.order import Order


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def create_order(
        self,
        order_id: str,
        customer_name: str,
        total: Decimal,
    ) -> Order:
        existing_order = self._repository.get_by_id(order_id)

        if existing_order is not None:
            raise ValueError(f"Ya existe un pedido con el id '{order_id}'.")

        order = Order(
            id=order_id,
            customer_name=customer_name,
            total=total,
        )

        self._repository.save(order)

        return order

    def get_order(self, order_id: str) -> Order | None:
        return self._repository.get_by_id(order_id)

    def list_orders(self) -> list[Order]:
        return self._repository.list_all()
