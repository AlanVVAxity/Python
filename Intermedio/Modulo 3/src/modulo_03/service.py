from dataclasses import dataclass

from modulo_03.order import Order, OrderItem
from modulo_03.repository import OrderRepository


@dataclass
class OrderService:
    repository: OrderRepository

    def create_order(
        self,
        order_id: str,
        customer_email: str,
        items: list[OrderItem],
    ) -> Order:
        order = Order(
            order_id=order_id,
            customer_email=customer_email,
            items=items,
        )

        self.repository.save(order)

        return order
