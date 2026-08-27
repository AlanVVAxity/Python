import re
from typing import Any

Empleado = dict[str, Any]
PATRON_CORREO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def obtener_estado_empleado(empleado: Empleado) -> str:
    """Devuelve un texto según el estado activo del empleado."""
    if empleado["activo"]:
        return "Activo"

    return "Inactivo"


"""Calcula un bono según el salario y estado del empleado."""


def calcular_bono(empleado: Empleado) -> float:
    salario = float(empleado["salario"])

    if not empleado["activo"]:
        return 0.0

    if salario >= 35_000:
        return salario * 0.15

    if salario >= 30_000:
        return salario * 0.10

    return salario * 0.05


"""Cuenta cuántos empleados existen en cada departamento."""


def contar_empleados_por_departamento(
    empleados: list[Empleado],
) -> dict[str, int]:
    conteo: dict[str, int] = {}

    for empleado in empleados:
        departamento = str(empleado["departamento"])

        if departamento in conteo:
            conteo[departamento] += 1
        else:
            conteo[departamento] = 1

    return conteo


"""Clasifica el salario del empleado en un nivel."""


def clasificar_nivel_salarial(empleado: Empleado) -> str:
    salario = float(empleado["salario"])

    match salario:
        case valor if valor >= 35_000:
            return "Senior"
        case valor if valor >= 30_000:
            return "Semi Senior"
        case _:
            return "Junior"


"""Convierte un texto a salario y lanza un error claro si no es válido."""


def convertir_salario(valor: str) -> float:
    try:
        salario = float(valor)
    except ValueError as error:
        mensaje = f"El salario '{valor}' no es un número válido."
        raise ValueError(mensaje) from error

    if salario < 0:
        raise ValueError("El salario no puede ser negativo.")

    return salario


def validar_correo(correo: str) -> bool:
    return PATRON_CORREO.fullmatch(correo) is not None
