from datetime import UTC
from decimal import Decimal

from modulo_06.metrics import calculate_metrics
from modulo_06.models import Sale


def test_calculates_sales_metrics(sample_sales: list[Sale]) -> None:
    metrics = calculate_metrics(
        total_rows=5,
        sales=sample_sales,
        rejected_rows=2,
    )

    assert metrics.total_rows == 5
    assert metrics.valid_sales == 3
    assert metrics.rejected_rows == 2
    assert metrics.total_quantity == 6
    assert metrics.total_revenue == Decimal("1627.50")
    assert metrics.revenue_by_category == {
        "Electronica": Decimal("1500.00"),
        "Accesorios": Decimal("127.50"),
    }
    assert metrics.top_product_by_revenue == "Laptop"
    assert metrics.processed_at.tzinfo == UTC


def test_calculates_empty_metrics() -> None:
    metrics = calculate_metrics(
        total_rows=2,
        sales=[],
        rejected_rows=2,
    )

    assert metrics.valid_sales == 0
    assert metrics.rejected_rows == 2
    assert metrics.total_quantity == 0
    assert metrics.total_revenue == Decimal("0")
    assert metrics.revenue_by_category == {}
    assert metrics.top_product_by_revenue is None
    assert metrics.processed_at.tzinfo == UTC
