from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class OrderItem(BaseModel):
    product_name: str = Field(
        min_length=1,
        max_length=100,
        examples=["Teclado mecánico"],
    )
    quantity: int = Field(
        gt=0,
        examples=[2],
    )
    unit_price: Decimal = Field(
        gt=0,
        decimal_places=2,
        examples=["999.99"],
    )


class OrderCreate(BaseModel):
    customer_name: str = Field(
        min_length=1,
        max_length=100,
        examples=["María González"],
    )
    items: list[OrderItem] = Field(
        min_length=1,
        examples=[
            [
                {
                    "product_name": "Teclado mecánico",
                    "quantity": 2,
                    "unit_price": "999.99",
                }
            ]
        ],
    )


class OrderUpdate(BaseModel):
    customer_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        examples=["María González López"],
    )
    items: list[OrderItem] | None = Field(
        default=None,
        min_length=1,
    )


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_name: str
    items: list[OrderItem]
    total: Decimal


def calculate_total(items: list[OrderItem]) -> Decimal:
    return sum(
        (item.unit_price * item.quantity for item in items),
        start=Decimal("0.00"),
    )


def create_order_id() -> UUID:
    return uuid4()