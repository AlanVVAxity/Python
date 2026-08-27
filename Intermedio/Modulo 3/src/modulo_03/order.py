from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class OrderItem:
    product_name: str
    unit_price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        if not self.product_name.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

        if self.unit_price <= Decimal("0"):
            raise ValueError("El precio unitario debe ser mayor que cero.")

        if self.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    customer_email: str
    items: list[OrderItem]

    def __post_init__(self) -> None:
        if not self.order_id.strip():
            raise ValueError("El identificador del pedido no puede estar vacío.")

        if not self._is_valid_email(self.customer_email):
            raise ValueError("El correo electrónico del cliente no es válido.")

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), start=Decimal("0.00"))

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return (
            bool(email.strip())
            and "@" in email
            and not email.startswith("@")
            and not email.endswith("@")
        )
