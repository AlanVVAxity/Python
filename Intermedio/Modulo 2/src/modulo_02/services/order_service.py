from uuid import UUID

from modulo_02.repositories.order_repository import OrderRepository
from modulo_02.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
    calculate_total,
    create_order_id,
)


class OrderNotFoundError(Exception):
    """Se lanza cuando una orden solicitada no existe."""


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        order = OrderResponse(
            id=create_order_id(),
            customer_name=order_data.customer_name,
            items=order_data.items,
            total=calculate_total(order_data.items),
        )
        return self._repository.create(order)

    def list_orders(self) -> list[OrderResponse]:
        return self._repository.get_all()

    def get_order(self, order_id: UUID) -> OrderResponse:
        order = self._repository.get_by_id(order_id)

        if order is None:
            raise OrderNotFoundError

        return order

    def update_order(
        self,
        order_id: UUID,
        order_data: OrderUpdate,
    ) -> OrderResponse:
        current_order = self.get_order(order_id)

        customer_name = order_data.customer_name or current_order.customer_name
        items = order_data.items or current_order.items

        updated_order = OrderResponse(
            id=current_order.id,
            customer_name=customer_name,
            items=items,
            total=calculate_total(items),
        )

        return self._repository.update(updated_order)

    def delete_order(self, order_id: UUID) -> None:
        deleted = self._repository.delete(order_id)

        if not deleted:
            raise OrderNotFoundError