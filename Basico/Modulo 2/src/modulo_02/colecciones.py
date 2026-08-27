from typing import Any

Empleado = dict[str, Any]


def obtener_empleados_demo() -> list[Empleado]:
    """Devuelve una lista de empleados de ejemplo."""
    empleados = [
        {
            "id": 1,
            "nombre": "Ana",
            "departamento": "Tecnologia",
            "salario": 32000.0,
            "activo": True,
        },
        {
            "id": 2,
            "nombre": "Bruno",
            "departamento": "Finanzas",
            "salario": 28000.0,
            "activo": True,
        },
        {
            "id": 3,
            "nombre": "Carla",
            "departamento": "Tecnologia",
            "salario": 35000.0,
            "activo": False,
        },
        {
            "id": 4,
            "nombre": "Diego",
            "departamento": "Operacion",
            "salario": 26000.0,
            "activo": True,
        },
    ]

    return empleados


def obtener_empleados_activos(empleados: list[Empleado]) -> list[Empleado]:
    """Filtra y devuelve únicamente los empleados activos."""
    return [empleado for empleado in empleados if empleado["activo"]]


def obtener_departamentos(empleados: list[Empleado]) -> set[str]:
    """Obtiene los nombres únicos de los departamentos."""
    return {str(empleado["departamento"]) for empleado in empleados}


def calcular_salario_total(empleados: list[Empleado]) -> float:
    """Calcula la suma de los salarios de los empleados recibidos."""
    return sum(float(empleado["salario"]) for empleado in empleados)


def obtener_resumen_empleados(empleados: list[Empleado]) -> tuple[int, float]:
    """Devuelve la cantidad de empleados y el salario total."""
    cantidad = len(empleados)
    salario_total = calcular_salario_total(empleados)

    return cantidad, salario_total
