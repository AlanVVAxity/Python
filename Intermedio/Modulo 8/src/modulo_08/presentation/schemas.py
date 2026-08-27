from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from modulo_08.domain.value_objects import OrderStatus


class CreateOrderRequest(BaseModel):
    customer_email: str = Field(min_length=3, max_length=255)
    product_name: str = Field(min_length=1, max_length=255)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=Decimal("0"), max_digits=10, decimal_places=2)


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_email: str
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
