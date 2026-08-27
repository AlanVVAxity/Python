from modulo_02.colecciones import (
    calcular_salario_total,
    obtener_departamentos,
    obtener_empleados_activos,
    obtener_empleados_demo,
    obtener_resumen_empleados,
)


def test_obtener_empleados_demo_devuelve_cuatro_empleados() -> None:
    empleados = obtener_empleados_demo()

    assert len(empleados) == 4
    assert empleados[0]["nombre"] == "Ana"


def test_obtener_empleados_activos_filtra_correctamente() -> None:
    empleados = obtener_empleados_demo()

    empleados_activos = obtener_empleados_activos(empleados)

    assert len(empleados_activos) == 3
    assert all(empleado["activo"] for empleado in empleados_activos)


def test_obtener_departamentos_elimina_repetidos() -> None:
    empleados = obtener_empleados_demo()

    departamentos = obtener_departamentos(empleados)

    assert departamentos == {"Tecnologia", "Finanzas", "Operacion"}


def test_calcular_salario_total() -> None:
    empleados = obtener_empleados_demo()

    salario_total = calcular_salario_total(empleados)

    assert salario_total == 121000.0


def test_obtener_resumen_empleados() -> None:
    empleados = obtener_empleados_demo()

    cantidad, salario_total = obtener_resumen_empleados(empleados)

    assert cantidad == 4
    assert salario_total == 121000.0
