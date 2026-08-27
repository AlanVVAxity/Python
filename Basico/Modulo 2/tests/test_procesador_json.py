import json
from pathlib import Path

import pytest

from modulo_02.procesador_json import (
    cargar_empleados_desde_json,
    exportar_resumen_a_json,
    obtener_resumen_activos,
    validar_empleado,
)


def crear_archivo_json(ruta: Path, contenido: object) -> None:
    """Crea un archivo JSON temporal para las pruebas."""
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo)


def obtener_empleado_valido() -> dict[str, object]:
    """Devuelve un empleado válido para pruebas."""
    return {
        "id": 1,
        "nombre": "Ana",
        "departamento": "Tecnologia",
        "salario": 32000.0,
        "activo": True,
        "correo": "ana@empresa.com",
    }


def test_cargar_empleados_desde_json(tmp_path: Path) -> None:
    ruta = tmp_path / "empleados.json"
    empleados_esperados = [obtener_empleado_valido()]
    crear_archivo_json(ruta, empleados_esperados)

    empleados = cargar_empleados_desde_json(ruta)

    assert empleados == empleados_esperados


def test_cargar_empleados_lanza_error_si_archivo_no_existe(
    tmp_path: Path,
) -> None:
    ruta = tmp_path / "inexistente.json"

    with pytest.raises(FileNotFoundError, match="No se encontró el archivo"):
        cargar_empleados_desde_json(ruta)


def test_cargar_empleados_lanza_error_si_json_es_invalido(
    tmp_path: Path,
) -> None:
    ruta = tmp_path / "invalido.json"
    ruta.write_text("{esto no es json}", encoding="utf-8")

    with pytest.raises(ValueError, match="no contiene JSON válido"):
        cargar_empleados_desde_json(ruta)


def test_cargar_empleados_lanza_error_si_json_no_es_lista(
    tmp_path: Path,
) -> None:
    ruta = tmp_path / "empleado.json"
    crear_archivo_json(ruta, obtener_empleado_valido())

    with pytest.raises(ValueError, match="debe contener una lista"):
        cargar_empleados_desde_json(ruta)


def test_validar_empleado_correcto() -> None:
    validar_empleado(obtener_empleado_valido())


def test_validar_empleado_lanza_error_por_campo_faltante() -> None:
    empleado = obtener_empleado_valido()
    del empleado["correo"]

    with pytest.raises(ValueError, match="correo"):
        validar_empleado(empleado)


def test_validar_empleado_lanza_error_por_salario_negativo() -> None:
    empleado = obtener_empleado_valido()
    empleado["salario"] = -100.0

    with pytest.raises(ValueError, match="no puede ser negativo"):
        validar_empleado(empleado)


def test_validar_empleado_lanza_error_por_correo_invalido() -> None:
    empleado = obtener_empleado_valido()
    empleado["correo"] = "correo-invalido"

    with pytest.raises(ValueError, match="no tiene un formato válido"):
        validar_empleado(empleado)


def test_obtener_resumen_activos() -> None:
    empleados = [
        obtener_empleado_valido(),
        {
            "id": 2,
            "nombre": "Bruno",
            "departamento": "Finanzas",
            "salario": 28000.0,
            "activo": False,
            "correo": "bruno@empresa.com",
        },
    ]

    resumen = obtener_resumen_activos(empleados)

    assert resumen == {
        "cantidad_total": 2,
        "cantidad_activos": 1,
        "salario_total_activos": 32000.0,
        "departamentos_activos": ["Tecnologia"],
    }


def test_exportar_resumen_a_json(tmp_path: Path) -> None:
    ruta = tmp_path / "output" / "resumen.json"
    resumen = {
        "cantidad_total": 2,
        "cantidad_activos": 1,
        "salario_total_activos": 32000.0,
        "departamentos_activos": ["Tecnologia"],
    }

    exportar_resumen_a_json(resumen, ruta)

    with ruta.open(encoding="utf-8") as archivo:
        contenido = json.load(archivo)

    assert contenido == resumen
