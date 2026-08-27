import json
import logging
from pathlib import Path
from typing import Any

from modulo_06.models import ProcessingResult


def write_summary_json(
    result: ProcessingResult,
    output_path: Path,
    logger: logging.Logger,
) -> None:
    """Exporta el resumen de procesamiento en un archivo JSON."""

    if result.metrics is None:
        raise ValueError("No se puede generar el JSON porque faltan las métricas.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "processed_at": result.metrics.processed_at.isoformat(),
        "source": {
            "file": "data/ventas.csv",
        },
        "metrics": {
            "total_rows": result.metrics.total_rows,
            "valid_sales": result.metrics.valid_sales,
            "rejected_rows": result.metrics.rejected_rows,
            "total_quantity": result.metrics.total_quantity,
            "total_revenue": str(result.metrics.total_revenue),
            "revenue_by_category": {
                category: str(revenue)
                for category, revenue in result.metrics.revenue_by_category.items()
            },
            "top_product_by_revenue": result.metrics.top_product_by_revenue,
        },
        "rejected_rows": result.errors,
    }

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(
            payload,
            json_file,
            ensure_ascii=False,
            indent=2,
        )

    logger.info("Archivo JSON generado: %s", output_path)


def read_json_file(json_path: Path) -> dict[str, Any]:
    """Lee un archivo JSON para facilitar validaciones desde las pruebas."""

    with json_path.open(encoding="utf-8") as json_file:
        content: Any = json.load(json_file)

    if not isinstance(content, dict):
        raise ValueError("El contenido del archivo JSON debe ser un objeto.")

    return content
