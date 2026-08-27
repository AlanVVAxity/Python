from modulo_06.csv_reader import read_sales_csv
from modulo_06.json_writer import write_summary_json
from modulo_06.logging_config import configure_logging
from modulo_06.metrics import calculate_metrics
from modulo_06.paths import input_csv_path, output_json_path
from modulo_06.system_check import run_python_version_check


def main() -> int:
    """Ejecuta el flujo completo de ingesta, métricas y exportación."""

    logger = configure_logging()

    try:
        logger.info("Inicio del módulo 06.")

        run_python_version_check(logger)

        csv_path = input_csv_path()
        result = read_sales_csv(csv_path, logger)

        result.metrics = calculate_metrics(
            total_rows=result.total_rows,
            sales=result.sales,
            rejected_rows=len(result.errors),
        )

        logger.info(
            "Métricas calculadas: filas=%s, válidas=%s, rechazadas=%s, "
            "cantidad_total=%s, importe_total=%s",
            result.metrics.total_rows,
            result.metrics.valid_sales,
            result.metrics.rejected_rows,
            result.metrics.total_quantity,
            result.metrics.total_revenue,
        )

        json_path = output_json_path()
        write_summary_json(result, json_path, logger)

        logger.info("Módulo 06 finalizado correctamente.")
        return 0

    except (FileNotFoundError, RuntimeError, ValueError) as error:
        logger.error("El módulo 06 terminó con error: %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
