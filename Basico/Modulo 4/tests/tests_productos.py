from dataclasses import FrozenInstanceError

import pytest

from modulo_04.productos import Producto


def test_producto_se_crea_correctamente() -> None:
    producto = Producto(
        sku="SKU-001",
        nombre="Teclado",
        precio_unitario=500.0,
    )

    assert producto.sku == "SKU-001"
    assert producto.nombre == "Teclado"
    assert producto.precio_unitario == 500.0


def test_productos_iguales_se_comparan_por_valor() -> None:
    producto_a = Producto("SKU-001", "Teclado", 500.0)
    producto_b = Producto("SKU-001", "Teclado", 500.0)

    assert producto_a == producto_b


@pytest.mark.parametrize(
    ("sku", "nombre", "precio_unitario", "mensaje"),
    [
        ("", "Teclado", 500.0, "SKU"),
        ("SKU-001", "", 500.0, "nombre"),
        ("SKU-001", "Teclado", 0.0, "mayor que cero"),
        ("SKU-001", "Teclado", -100.0, "mayor que cero"),
    ],
)
def test_producto_rechaza_datos_invalidos(
    sku: str,
    nombre: str,
    precio_unitario: float,
    mensaje: str,
) -> None:
    with pytest.raises(ValueError, match=mensaje):
        Producto(sku, nombre, precio_unitario)


def test_producto_es_inmutable() -> None:
    producto = Producto("SKU-001", "Teclado", 500.0)

    with pytest.raises(FrozenInstanceError):
        producto.precio_unitario = 600.0  # type: ignore[misc]
