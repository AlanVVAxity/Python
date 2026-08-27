import logging
from pathlib import Path

from modulo_02.procesador_json import (
    cargar_empleados_desde_json,
    exportar_resumen_a_json,
    obtener_resumen_activos,
)


def configurar_logging() -> None:
    """Configura el formato y nivel de los mensajes de registro."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
    )


def main() -> None:
    """Carga empleados, genera métricas y exporta un resumen JSON."""
    configurar_logging()

    ruta_entrada = Path("data") / "empleados.json"
    ruta_salida = Path("output") / "resumen_empleados.json"

    try:
        empleados = cargar_empleados_desde_json(ruta_entrada)
        resumen = obtener_resumen_activos(empleados)
        exportar_resumen_a_json(resumen, ruta_salida)
    except (FileNotFoundError, ValueError) as error:
        logging.error("No fue posible procesar los empleados: %s", error)
        return

    print("=== Resumen exportado correctamente ===")
    print(f"Archivo generado: {ruta_salida}")
    print(f"Empleados totales: {resumen['cantidad_total']}")
    print(f"Empleados activos: {resumen['cantidad_activos']}")
    print(f"Salario total activo: ${resumen['salario_total_activos']:,.2f}")
    print(f"Departamentos activos: {', '.join(resumen['departamentos_activos'])}")


if __name__ == "__main__":
    main()
