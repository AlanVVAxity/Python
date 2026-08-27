import pytest

from modulo_02.colecciones import obtener_empleados_demo
from modulo_02.logica_empleados import (
    calcular_bono,
    clasificar_nivel_salarial,
    contar_empleados_por_departamento,
    convertir_salario,
    obtener_estado_empleado,
    validar_correo,
)


def test_obtener_estado_empleado_activo() -> None:
    empleados = obtener_empleados_demo()

    estado = obtener_estado_empleado(empleados[0])

    assert estado == "Activo"


def test_obtener_estado_empleado_inactivo() -> None:
    empleados = obtener_empleados_demo()

    estado = obtener_estado_empleado(empleados[2])

    assert estado == "Inactivo"


def test_calcular_bono_para_empleado_activo_con_salario_medio() -> None:
    empleados = obtener_empleados_demo()

    bono = calcular_bono(empleados[0])

    assert bono == 3200.0


def test_calcular_bono_para_empleado_inactivo_es_cero() -> None:
    empleados = obtener_empleados_demo()

    bono = calcular_bono(empleados[2])

    assert bono == 0.0


def test_contar_empleados_por_departamento() -> None:
    empleados = obtener_empleados_demo()

    conteo = contar_empleados_por_departamento(empleados)

    assert conteo == {
        "Tecnologia": 2,
        "Finanzas": 1,
        "Operacion": 1,
    }


def test_clasificar_nivel_salarial_senior() -> None:
    empleados = obtener_empleados_demo()

    nivel = clasificar_nivel_salarial(empleados[2])

    assert nivel == "Senior"


def test_clasificar_nivel_salarial_semi_senior() -> None:
    empleados = obtener_empleados_demo()

    nivel = clasificar_nivel_salarial(empleados[0])

    assert nivel == "Semi Senior"


def test_clasificar_nivel_salarial_junior() -> None:
    empleados = obtener_empleados_demo()

    nivel = clasificar_nivel_salarial(empleados[3])

    assert nivel == "Junior"


def test_convertir_salario_valido() -> None:
    salario = convertir_salario("32500.50")

    assert salario == 32500.50


def test_convertir_salario_invalido_lanza_error() -> None:
    with pytest.raises(ValueError, match="no es un número válido"):
        convertir_salario("treinta mil")


def test_convertir_salario_negativo_lanza_error() -> None:
    with pytest.raises(ValueError, match="no puede ser negativo"):
        convertir_salario("-100")


def test_validar_correo_valido() -> None:
    assert validar_correo("ana@example.com") is True


def test_validar_correo_valido_con_subdominio() -> None:
    assert validar_correo("bruno.lopez@empresa.com.mx") is True


def test_validar_correo_invalido() -> None:
    assert validar_correo("correo-invalido") is False


def test_validar_correo_sin_dominio() -> None:
    assert validar_correo("ana@") is False
