from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from orders_service.domain.entities import OrderStatus


@dataclass(frozen=True)
class CreateOrderItemInput:
    product_name: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class CreateOrderInput:
    customer_email: str
    items: list[CreateOrderItemInput]


@dataclass(frozen=True)
class OrderItemOutput:
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


@dataclass(frozen=True)
class OrderOutput:
    id: UUID
    customer_email: str
    status: OrderStatus
    items: list[OrderItemOutput]
    total: Decimal
