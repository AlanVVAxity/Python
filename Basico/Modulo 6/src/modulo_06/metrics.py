from collections import defaultdict
from datetime import UTC, datetime
from decimal import Decimal

from modulo_06.models import Sale, SalesMetrics


def calculate_metrics(
    total_rows: int,
    sales: list[Sale],
    rejected_rows: int,
) -> SalesMetrics:
    """Calcula las métricas de las ventas válidas."""

    revenue_by_category: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    revenue_by_product: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))

    total_quantity = 0
    total_revenue = Decimal("0")

    for sale in sales:
        sale_total = sale.total_amount

        total_quantity += sale.quantity
        total_revenue += sale_total
        revenue_by_category[sale.category] += sale_total
        revenue_by_product[sale.product] += sale_total

    top_product_by_revenue = _get_top_product(revenue_by_product)

    return SalesMetrics(
        total_rows=total_rows,
        valid_sales=len(sales),
        rejected_rows=rejected_rows,
        total_quantity=total_quantity,
        total_revenue=total_revenue,
        revenue_by_category=dict(revenue_by_category),
        top_product_by_revenue=top_product_by_revenue,
        processed_at=datetime.now(UTC),
    )


def _get_top_product(
    revenue_by_product: dict[str, Decimal],
) -> str | None:
    """Devuelve el producto con mayor importe acumulado."""

    if not revenue_by_product:
        return None

    return max(
        revenue_by_product,
        key=revenue_by_product.__getitem__,
    )
