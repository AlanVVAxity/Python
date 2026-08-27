import logging
from decimal import Decimal
from pathlib import Path

import pytest

from modulo_06.csv_reader import read_sales_csv


def test_reads_valid_sales(
    valid_csv_path: Path,
    test_logger: logging.Logger,
) -> None:
    result = read_sales_csv(valid_csv_path, test_logger)

    assert result.total_rows == 2
    assert len(result.sales) == 2
    assert result.errors == []

    first_sale = result.sales[0]
    assert first_sale.sale_id == 1
    assert first_sale.product == "Laptop"
    assert first_sale.quantity == 1
    assert first_sale.unit_price == Decimal("1500.00")
    assert first_sale.sold_at.tzinfo is not None


def test_rejects_invalid_rows_and_continues(
    invalid_csv_path: Path,
    test_logger: logging.Logger,
) -> None:
    result = read_sales_csv(invalid_csv_path, test_logger)

    assert result.total_rows == 5
    assert len(result.sales) == 1
    assert len(result.errors) == 4
    assert result.sales[0].product == "Laptop"


def test_rejects_invalid_date(
    invalid_csv_path: Path,
    test_logger: logging.Logger,
) -> None:
    result = read_sales_csv(invalid_csv_path, test_logger)

    assert any("fecha ISO 8601 válida" in error for error in result.errors)


def test_rejects_datetime_without_timezone(
    invalid_csv_path: Path,
    test_logger: logging.Logger,
) -> None:
    result = read_sales_csv(invalid_csv_path, test_logger)

    assert any("debe incluir zona horaria" in error for error in result.errors)


def test_rejects_zero_quantity(
    invalid_csv_path: Path,
    test_logger: logging.Logger,
) -> None:
    result = read_sales_csv(invalid_csv_path, test_logger)

    assert any("cantidad' debe ser mayor que cero" in error for error in result.errors)


def test_rejects_empty_product(
    invalid_csv_path: Path,
    test_logger: logging.Logger,
) -> None:
    result = read_sales_csv(invalid_csv_path, test_logger)

    assert any("producto' es obligatorio" in error for error in result.errors)


def test_raises_error_when_file_does_not_exist(
    tmp_path: Path,
    test_logger: logging.Logger,
) -> None:
    missing_file = tmp_path / "archivo_inexistente.csv"

    with pytest.raises(FileNotFoundError):
        read_sales_csv(missing_file, test_logger)


def test_raises_error_when_required_columns_are_missing(
    tmp_path: Path,
    test_logger: logging.Logger,
) -> None:
    csv_path = tmp_path / "columnas_incompletas.csv"
    csv_path.write_text(
        "id_venta,producto\n1,Laptop\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="columnas obligatorias"):
        read_sales_csv(csv_path, test_logger)
