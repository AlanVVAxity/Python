from orders_service.application.dto import OrderItemOutput, OrderOutput
from orders_service.domain.repositories import OrderRepository


class ListOrdersUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self) -> list[OrderOutput]:
        orders = self.repository.list_all()

        return [
            OrderOutput(
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
            for order in orders
        ]
