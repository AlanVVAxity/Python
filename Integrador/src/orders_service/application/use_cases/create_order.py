from orders_service.application.dto import (
    CreateOrderInput,
    OrderItemOutput,
    OrderOutput,
)
from orders_service.application.ports import OrderNotifier
from orders_service.domain.entities import Order, OrderItem
from orders_service.domain.repositories import OrderRepository


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepository,
        notifier: OrderNotifier,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def execute(self, data: CreateOrderInput) -> OrderOutput:
        items = [
            OrderItem(
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in data.items
        ]

        order = Order(
            customer_email=data.customer_email,
            items=items,
        )

        saved_order = self.repository.add(order)
        self.notifier.order_created(saved_order)

        return OrderOutput(
            id=saved_order.id,
            customer_email=saved_order.customer_email,
            status=saved_order.status,
            items=[
                OrderItemOutput(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                )
                for item in saved_order.items
            ],
            total=saved_order.total,
        )
