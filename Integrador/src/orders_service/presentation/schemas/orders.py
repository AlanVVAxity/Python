from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from orders_service.domain.entities import OrderStatus


class OrderItemCreateRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=255)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class OrderCreateRequest(BaseModel):
    customer_email: EmailStr
    items: list[OrderItemCreateRequest] = Field(min_length=1)


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_email: EmailStr
    status: OrderStatus
    items: list[OrderItemResponse]
    total: Decimal
