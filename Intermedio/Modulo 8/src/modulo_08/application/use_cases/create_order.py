from modulo_08.application.dto import CreateOrderInput, OrderOutput
from modulo_08.application.ports.notification_port import NotificationPort
from modulo_08.application.ports.order_repository_port import OrderRepositoryPort
from modulo_08.domain.entities import Order


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        notification_service: NotificationPort,
    ) -> None:
        self._order_repository = order_repository
        self._notification_service = notification_service

    def execute(self, data: CreateOrderInput) -> OrderOutput:
        order = Order.create(
            customer_email=data.customer_email,
            product_name=data.product_name,
            quantity=data.quantity,
            unit_price=data.unit_price,
        )

        saved_order = self._order_repository.save(order)
        self._notification_service.send_order_created(saved_order)

        return OrderOutput(
            id=saved_order.id,
            customer_email=saved_order.customer_email,
            product_name=saved_order.product_name,
            quantity=saved_order.quantity,
            unit_price=saved_order.unit_price,
            total_price=saved_order.total_price,
            status=saved_order.status,
            created_at=saved_order.created_at,
        )
