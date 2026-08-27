import json
import logging
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from modulo_06.json_writer import read_json_file, write_summary_json
from modulo_06.models import ProcessingResult, SalesMetrics


def test_writes_summary_json(
    tmp_path: Path,
    test_logger: logging.Logger,
) -> None:
    metrics = SalesMetrics(
        total_rows=3,
        valid_sales=2,
        rejected_rows=1,
        total_quantity=4,
        total_revenue=Decimal("1551.00"),
        revenue_by_category={
            "Electronica": Decimal("1500.00"),
            "Accesorios": Decimal("51.00"),
        },
        top_product_by_revenue="Laptop",
        processed_at=datetime(2025, 1, 1, 12, 0, tzinfo=UTC),
    )

    result = ProcessingResult(
        errors=["Fila 4: el campo 'cantidad' debe ser mayor que cero"],
        total_rows=3,
        metrics=metrics,
    )

    output_path = tmp_path / "subcarpeta" / "resumen.json"

    write_summary_json(result, output_path, test_logger)

    assert output_path.exists()

    content = read_json_file(output_path)

    assert content["processed_at"] == "2025-01-01T12:00:00+00:00"
    assert content["metrics"]["total_revenue"] == "1551.00"
    assert content["metrics"]["revenue_by_category"]["Electronica"] == "1500.00"
    assert content["metrics"]["top_product_by_revenue"] == "Laptop"
    assert len(content["rejected_rows"]) == 1


def test_raises_error_when_metrics_are_missing(
    tmp_path: Path,
    test_logger: logging.Logger,
) -> None:
    result = ProcessingResult()
    output_path = tmp_path / "resumen.json"

    try:
        write_summary_json(result, output_path, test_logger)
    except ValueError as error:
        assert "faltan las métricas" in str(error)
    else:
        raise AssertionError("Se esperaba ValueError cuando faltan métricas.")


def test_generated_file_contains_valid_json(
    tmp_path: Path,
    test_logger: logging.Logger,
) -> None:
    metrics = SalesMetrics(
        total_rows=0,
        valid_sales=0,
        rejected_rows=0,
        total_quantity=0,
        total_revenue=Decimal("0"),
        revenue_by_category={},
        top_product_by_revenue=None,
        processed_at=datetime(2025, 1, 1, tzinfo=UTC),
    )

    output_path = tmp_path / "resumen.json"

    write_summary_json(
        ProcessingResult(metrics=metrics),
        output_path,
        test_logger,
    )

    with output_path.open(encoding="utf-8") as json_file:
        content = json.load(json_file)

    assert content["metrics"]["total_revenue"] == "0"
