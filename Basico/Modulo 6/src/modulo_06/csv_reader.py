import csv
import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from modulo_06.models import ProcessingResult, Sale

REQUIRED_COLUMNS = {
    "id_venta",
    "fecha",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
}


def read_sales_csv(csv_path: Path, logger: logging.Logger) -> ProcessingResult:
    """Lee un CSV, valida sus filas y devuelve ventas aceptadas y errores."""

    if not csv_path.exists():
        message = f"No se encontró el archivo CSV: {csv_path}"
        logger.error(message)
        raise FileNotFoundError(message)

    sales: list[Sale] = []
    errors: list[str] = []
    total_rows = 0

    logger.info("Leyendo archivo CSV: %s", csv_path)

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            message = "El archivo CSV no contiene encabezados."
            logger.error(message)
            raise ValueError(message)

        missing_columns = REQUIRED_COLUMNS.difference(reader.fieldnames)

        if missing_columns:
            missing_columns_text = ", ".join(sorted(missing_columns))
            message = (
                "El archivo CSV no contiene las columnas obligatorias: "
                f"{missing_columns_text}"
            )
            logger.error(message)
            raise ValueError(message)

        for row_number, row in enumerate(reader, start=2):
            total_rows += 1

            try:
                sale = _parse_sale(row)
            except ValueError as error:
                message = f"Fila {row_number}: {error}"
                errors.append(message)
                logger.warning(message)
                continue

            sales.append(sale)

    logger.info("Filas de datos encontradas: %s", total_rows)
    logger.info("Ventas válidas: %s", len(sales))
    logger.info("Filas rechazadas: %s", len(errors))

    return ProcessingResult(
        sales=sales,
        errors=errors,
        total_rows=total_rows,
    )


def _parse_sale(row: dict[str, str | None]) -> Sale:
    """Convierte una fila de CSV a Sale y valida sus valores."""

    product = _get_required_text(row, "producto")
    category = _get_required_text(row, "categoria")

    sale_id = _parse_positive_int(row, "id_venta")
    quantity = _parse_positive_int(row, "cantidad")
    unit_price = _parse_positive_decimal(row, "precio_unitario")
    sold_at = _parse_aware_datetime(row, "fecha")

    return Sale(
        sale_id=sale_id,
        sold_at=sold_at,
        product=product,
        category=category,
        quantity=quantity,
        unit_price=unit_price,
    )


def _get_required_text(row: dict[str, str | None], field_name: str) -> str:
    """Obtiene un texto obligatorio y no vacío."""

    value = row.get(field_name)

    if value is None or not value.strip():
        raise ValueError(f"el campo '{field_name}' es obligatorio")

    return value.strip()


def _parse_positive_int(row: dict[str, str | None], field_name: str) -> int:
    """Convierte un campo a entero positivo."""

    raw_value = _get_required_text(row, field_name)

    try:
        value = int(raw_value)
    except ValueError as error:
        raise ValueError(
            f"el campo '{field_name}' debe ser un número entero válido"
        ) from error

    if value <= 0:
        raise ValueError(f"el campo '{field_name}' debe ser mayor que cero")

    return value


def _parse_positive_decimal(
    row: dict[str, str | None],
    field_name: str,
) -> Decimal:
    """Convierte un campo a Decimal positivo."""

    raw_value = _get_required_text(row, field_name)

    try:
        value = Decimal(raw_value)
    except InvalidOperation as error:
        raise ValueError(
            f"el campo '{field_name}' debe ser un número decimal válido"
        ) from error

    if value <= Decimal("0"):
        raise ValueError(f"el campo '{field_name}' debe ser mayor que cero")

    return value


def _parse_aware_datetime(
    row: dict[str, str | None],
    field_name: str,
) -> datetime:
    """Convierte un campo ISO 8601 a fecha con zona horaria."""

    raw_value = _get_required_text(row, field_name)

    try:
        value = datetime.fromisoformat(raw_value)
    except ValueError as error:
        raise ValueError(
            f"el campo '{field_name}' debe tener una fecha ISO 8601 válida"
        ) from error

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"el campo '{field_name}' debe incluir zona horaria")

    return value
