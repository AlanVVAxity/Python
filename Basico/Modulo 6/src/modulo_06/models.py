from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Sale:
    """Representa una venta válida obtenida desde el archivo CSV."""

    sale_id: int
    sold_at: datetime
    product: str
    category: str
    quantity: int
    unit_price: Decimal

    @property
    def total_amount(self) -> Decimal:
        """Calcula el importe total de la venta."""
        return self.unit_price * self.quantity


@dataclass(frozen=True, slots=True)
class SalesMetrics:
    """Contiene las métricas obtenidas del procesamiento de ventas."""

    total_rows: int
    valid_sales: int
    rejected_rows: int
    total_quantity: int
    total_revenue: Decimal
    revenue_by_category: dict[str, Decimal]
    top_product_by_revenue: str | None
    processed_at: datetime


@dataclass(slots=True)
class ProcessingResult:
    """Agrupa las ventas válidas, los errores y las métricas calculadas."""

    sales: list[Sale] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    total_rows: int = 0
    metrics: SalesMetrics | None = None
