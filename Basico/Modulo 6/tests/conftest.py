import logging
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from modulo_06.models import Sale


@pytest.fixture
def test_logger() -> logging.Logger:
    """Crea un logger silencioso para las pruebas."""

    logger = logging.getLogger("modulo_06_tests")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    return logger


@pytest.fixture
def valid_csv_path(tmp_path: Path) -> Path:
    """Crea un CSV temporal con ventas válidas."""

    csv_path = tmp_path / "ventas_validas.csv"
    csv_path.write_text(
        (
            "id_venta,fecha,producto,categoria,cantidad,precio_unitario\n"
            "1,2025-01-02T09:15:00+00:00,Laptop,Electronica,1,1500.00\n"
            "2,2025-01-02T10:30:00+00:00,Mouse,Accesorios,3,25.50\n"
        ),
        encoding="utf-8",
    )

    return csv_path


@pytest.fixture
def invalid_csv_path(tmp_path: Path) -> Path:
    """Crea un CSV temporal con una venta válida y varias inválidas."""

    csv_path = tmp_path / "ventas_invalidas.csv"
    csv_path.write_text(
        (
            "id_venta,fecha,producto,categoria,cantidad,precio_unitario\n"
            "1,2025-01-02T09:15:00+00:00,Laptop,Electronica,1,1500.00\n"
            "2,fecha-invalida,Mouse,Accesorios,3,25.50\n"
            "3,2025-01-03T14:00:00,Teclado,Accesorios,2,65.00\n"
            "4,2025-01-03T16:45:00+00:00,Monitor,Electronica,0,320.75\n"
            "5,2025-01-04T11:20:00+00:00,,Accesorios,2,10.00\n"
        ),
        encoding="utf-8",
    )

    return csv_path


@pytest.fixture
def sample_sales() -> list[Sale]:
    """Devuelve ventas de ejemplo para las pruebas de métricas."""

    return [
        Sale(
            sale_id=1,
            sold_at=datetime(2025, 1, 2, 9, 15, tzinfo=UTC),
            product="Laptop",
            category="Electronica",
            quantity=1,
            unit_price=Decimal("1500.00"),
        ),
        Sale(
            sale_id=2,
            sold_at=datetime(2025, 1, 2, 10, 30, tzinfo=UTC),
            product="Mouse",
            category="Accesorios",
            quantity=3,
            unit_price=Decimal("25.50"),
        ),
        Sale(
            sale_id=3,
            sold_at=datetime(2025, 1, 3, 14, 0, tzinfo=UTC),
            product="Mouse",
            category="Accesorios",
            quantity=2,
            unit_price=Decimal("25.50"),
        ),
    ]
