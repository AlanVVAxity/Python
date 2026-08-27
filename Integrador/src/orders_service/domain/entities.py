from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from orders_service.domain.exceptions import (
    InvalidOrderItemError,
    InvalidOrderStatusError,
)


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderItem:
    product_name: str
    quantity: int
    unit_price: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity

    def __post_init__(self) -> None:
        if not self.product_name.strip():
            raise InvalidOrderItemError("El nombre del producto es obligatorio.")

        if self.quantity <= 0:
            raise InvalidOrderItemError("La cantidad debe ser mayor que cero.")

        if self.unit_price <= Decimal("0"):
            raise InvalidOrderItemError("El precio unitario debe ser mayor que cero.")


@dataclass
class Order:
    customer_email: str
    items: list[OrderItem]
    id: UUID = field(default_factory=uuid4)
    status: OrderStatus = OrderStatus.PENDING

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), start=Decimal("0"))

    def mark_as_paid(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise InvalidOrderStatusError(
                "Solo una orden pendiente puede marcarse como pagada."
            )

        self.status = OrderStatus.PAID

    def cancel(self) -> None:
        if self.status == OrderStatus.PAID:
            raise InvalidOrderStatusError("Una orden pagada no puede cancelarse.")

        self.status = OrderStatus.CANCELLED
