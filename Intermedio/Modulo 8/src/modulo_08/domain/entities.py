from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from modulo_08.domain.exceptions import InvalidOrderError
from modulo_08.domain.value_objects import OrderStatus


@dataclass(frozen=True, slots=True)
class Order:
    id: UUID
    customer_email: str
    product_name: str
    quantity: int
    unit_price: Decimal
    status: OrderStatus
    created_at: datetime

    @classmethod
    def create(
        cls,
        *,
        customer_email: str,
        product_name: str,
        quantity: int,
        unit_price: Decimal,
    ) -> "Order":
        cls._validate_customer_email(customer_email)
        cls._validate_product_name(product_name)
        cls._validate_quantity(quantity)
        cls._validate_unit_price(unit_price)

        return cls(
            id=uuid4(),
            customer_email=customer_email,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
            status=OrderStatus.PENDING,
            created_at=datetime.now(UTC),
        )

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity

    @staticmethod
    def _validate_customer_email(customer_email: str) -> None:
        normalized_email = customer_email.strip()

        if not normalized_email:
            raise InvalidOrderError("El correo del cliente es obligatorio.")

        if "@" not in normalized_email:
            raise InvalidOrderError("El correo del cliente no tiene un formato válido.")

    @staticmethod
    def _validate_product_name(product_name: str) -> None:
        if not product_name.strip():
            raise InvalidOrderError("El nombre del producto es obligatorio.")

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if quantity <= 0:
            raise InvalidOrderError("La cantidad debe ser mayor que cero.")

    @staticmethod
    def _validate_unit_price(unit_price: Decimal) -> None:
        if unit_price <= Decimal("0"):
            raise InvalidOrderError("El precio unitario debe ser mayor que cero.")
