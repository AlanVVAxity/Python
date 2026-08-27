import json
import logging
from pathlib import Path
from typing import Any

from modulo_02.colecciones import (
    calcular_salario_total,
    obtener_departamentos,
    obtener_empleados_activos,
)
from modulo_02.logica_empleados import validar_correo

Empleado = dict[str, Any]

logger = logging.getLogger(__name__)


def cargar_empleados_desde_json(ruta: Path) -> list[Empleado]:
    """Carga empleados desde un archivo JSON y valida su estructura básica."""
    try:
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError as error:
        mensaje = f"No se encontró el archivo: {ruta}"
        logger.error(mensaje)
        raise FileNotFoundError(mensaje) from error
    except json.JSONDecodeError as error:
        mensaje = f"El archivo no contiene JSON válido: {ruta}"
        logger.error(mensaje)
        raise ValueError(mensaje) from error

    if not isinstance(datos, list):
        mensaje = "El JSON debe contener una lista de empleados."
        logger.error(mensaje)
        raise ValueError(mensaje)

    empleados: list[Empleado] = []

    for indice, empleado in enumerate(datos, start=1):
        if not isinstance(empleado, dict):
            mensaje = f"El elemento {indice} no es un empleado válido."
            logger.error(mensaje)
            raise ValueError(mensaje)

        empleados.append(empleado)

    logger.info("Se cargaron %s empleados desde %s.", len(empleados), ruta)

    return empleados


def validar_empleado(empleado: Empleado) -> None:
    """Valida que un empleado incluya campos requeridos y valores básicos."""
    campos_requeridos = {
        "id",
        "nombre",
        "departamento",
        "salario",
        "activo",
        "correo",
    }

    campos_faltantes = campos_requeridos.difference(empleado)

    if campos_faltantes:
        campos = ", ".join(sorted(campos_faltantes))
        raise ValueError(f"El empleado no incluye los campos: {campos}")

    salario = empleado["salario"]

    if not isinstance(salario, int | float):
        raise ValueError("El salario debe ser numérico.")

    if salario < 0:
        raise ValueError("El salario no puede ser negativo.")

    correo = str(empleado["correo"])

    if not validar_correo(correo):
        raise ValueError(f"El correo '{correo}' no tiene un formato válido.")


def obtener_resumen_activos(empleados: list[Empleado]) -> dict[str, Any]:
    """Genera métricas de empleados activos a partir de una lista."""
    for empleado in empleados:
        validar_empleado(empleado)

    empleados_activos = obtener_empleados_activos(empleados)
    salario_total = calcular_salario_total(empleados_activos)
    departamentos = obtener_departamentos(empleados_activos)

    resumen = {
        "cantidad_total": len(empleados),
        "cantidad_activos": len(empleados_activos),
        "salario_total_activos": salario_total,
        "departamentos_activos": sorted(departamentos),
    }

    logger.info(
        "Resumen generado: %s empleados totales y %s activos.",
        resumen["cantidad_total"],
        resumen["cantidad_activos"],
    )

    return resumen


def exportar_resumen_a_json(resumen: dict[str, Any], ruta: Path) -> None:
    """Exporta el resumen recibido a un archivo JSON."""
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2)

    logger.info("Resumen exportado a %s.", ruta)
