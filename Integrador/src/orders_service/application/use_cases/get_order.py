from uuid import UUID

from orders_service.application.dto import OrderItemOutput, OrderOutput
from orders_service.application.exceptions import OrderNotFoundApplicationError
from orders_service.domain.repositories import OrderRepository


class GetOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self, order_id: UUID) -> OrderOutput:
        order = self.repository.get_by_id(order_id)

        if order is None:
            raise OrderNotFoundApplicationError("Orden no encontrada.")

        return OrderOutput(
            id=order.id,
            customer_email=order.customer_email,
            status=order.status,
            items=[
                OrderItemOutput(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                )
                for item in order.items
            ],
            total=order.total,
        )
