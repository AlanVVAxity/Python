import pytest
from pydantic import ValidationError

from modulo_04.conversores import (
    convertir_linea_a_linea_out,
    convertir_orden_a_order_out,
    convertir_order_in_a_orden,
    convertir_producto_a_producto_out,
)
from modulo_04.ordenes import LineaOrden, Orden
from modulo_04.productos import Producto
from modulo_04.schemas import OrderIn, ProductoIn


def obtener_datos_order_validos() -> dict[str, object]:
    """Devuelve datos válidos para crear una orden de entrada."""
    return {
        "id_orden": " ORD-001 ",
        "cliente": " Ana ",
        "lineas": [
            {
                "producto": {
                    "sku": " SKU-001 ",
                    "nombre": " Teclado ",
                    "precio_unitario": 500.0,
                },
                "cantidad": 2,
            },
            {
                "producto": {
                    "sku": "SKU-002",
                    "nombre": "Mouse",
                    "precio_unitario": 200.0,
                },
                "cantidad": 3,
            },
        ],
        "descuento_porcentaje": 10.0,
    }


def test_order_in_valida_y_limpia_los_datos() -> None:
    order_in = OrderIn.model_validate(obtener_datos_order_validos())

    assert order_in.id_orden == "ORD-001"
    assert order_in.cliente == "Ana"
    assert order_in.lineas[0].producto.sku == "SKU-001"
    assert order_in.lineas[0].producto.nombre == "Teclado"


@pytest.mark.parametrize(
    ("datos", "campo"),
    [
        (
            {
                "sku": " ",
                "nombre": "Teclado",
                "precio_unitario": 500.0,
            },
            "sku",
        ),
        (
            {
                "sku": "SKU-001",
                "nombre": " ",
                "precio_unitario": 500.0,
            },
            "nombre",
        ),
        (
            {
                "sku": "SKU-001",
                "nombre": "Teclado",
                "precio_unitario": 0.0,
            },
            "precio_unitario",
        ),
    ],
)
def test_producto_in_rechaza_datos_invalidos(
    datos: dict[str, str | float],
    campo: str,
) -> None:
    with pytest.raises(ValidationError) as error:
        ProductoIn.model_validate(datos)

    assert campo in str(error.value)


def test_order_in_rechaza_orden_sin_lineas() -> None:
    datos = obtener_datos_order_validos()
    datos["lineas"] = []

    with pytest.raises(ValidationError, match="lineas"):
        OrderIn.model_validate(datos)


def test_order_in_rechaza_descuento_invalido() -> None:
    datos = obtener_datos_order_validos()
    datos["descuento_porcentaje"] = 110.0

    with pytest.raises(ValidationError, match="descuento_porcentaje"):
        OrderIn.model_validate(datos)


def test_convertir_order_in_a_orden() -> None:
    order_in = OrderIn.model_validate(obtener_datos_order_validos())

    orden = convertir_order_in_a_orden(order_in)

    assert orden.id_orden == "ORD-001"
    assert orden.cliente == "Ana"
    assert len(orden) == 2
    assert orden.subtotal == 1600.0
    assert orden.total == 1440.0


def test_convertir_producto_a_producto_out() -> None:
    producto = Producto(
        sku="SKU-001",
        nombre="Teclado",
        precio_unitario=500.0,
    )

    producto_out = convertir_producto_a_producto_out(producto)

    assert producto_out.model_dump() == {
        "sku": "SKU-001",
        "nombre": "Teclado",
        "precio_unitario": 500.0,
    }


def test_convertir_linea_a_linea_out() -> None:
    producto = Producto(
        sku="SKU-001",
        nombre="Teclado",
        precio_unitario=500.0,
    )
    linea = LineaOrden(producto=producto, cantidad=2)

    linea_out = convertir_linea_a_linea_out(linea)

    assert linea_out.model_dump() == {
        "sku": "SKU-001",
        "nombre_producto": "Teclado",
        "cantidad": 2,
        "subtotal": 1000.0,
    }


def test_convertir_orden_a_order_out() -> None:
    producto = Producto(
        sku="SKU-001",
        nombre="Teclado",
        precio_unitario=500.0,
    )
    orden = Orden(
        id_orden="ORD-001",
        cliente="Ana",
        lineas=[LineaOrden(producto=producto, cantidad=2)],
        descuento_porcentaje=10.0,
    )

    order_out = convertir_orden_a_order_out(orden)

    assert order_out.model_dump() == {
        "id_orden": "ORD-001",
        "cliente": "Ana",
        "cantidad_lineas": 1,
        "subtotal": 1000.0,
        "descuento_porcentaje": 10.0,
        "monto_descuento": 100.0,
        "total": 900.0,
    }
