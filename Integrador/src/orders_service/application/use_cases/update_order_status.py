from uuid import UUID

from orders_service.application.dto import OrderItemOutput, OrderOutput
from orders_service.application.exceptions import OrderNotFoundApplicationError
from orders_service.domain.entities import OrderStatus
from orders_service.domain.repositories import OrderRepository


class UpdateOrderStatusUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self, order_id: UUID, status: OrderStatus) -> OrderOutput:
        order = self.repository.get_by_id(order_id)

        if order is None:
            raise OrderNotFoundApplicationError("Orden no encontrada.")

        if status == OrderStatus.PAID:
            order.mark_as_paid()

        if status == OrderStatus.CANCELLED:
            order.cancel()

        updated_order = self.repository.update(order)

        return OrderOutput(
            id=updated_order.id,
            customer_email=updated_order.customer_email,
            status=updated_order.status,
            items=[
                OrderItemOutput(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                )
                for item in updated_order.items
            ],
            total=updated_order.total,
        )
