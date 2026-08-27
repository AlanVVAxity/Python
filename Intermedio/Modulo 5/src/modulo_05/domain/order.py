from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Order:
    id: str
    customer_name: str
    total: Decimal
