from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from modulo_08.domain.value_objects import OrderStatus


@dataclass(frozen=True, slots=True)
class CreateOrderInput:
    customer_email: str
    product_name: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True, slots=True)
class OrderOutput:
    id: UUID
    customer_email: str
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
