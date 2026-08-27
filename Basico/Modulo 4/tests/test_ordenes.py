import pytest

from modulo_04.ordenes import LineaOrden, Orden
from modulo_04.productos import Producto


def crear_producto() -> Producto:
    """Crea un producto de ejemplo para las pruebas."""
    return Producto(
        sku="SKU-001",
        nombre="Teclado",
        precio_unitario=500.0,
    )


def test_linea_orden_calcula_subtotal() -> None:
    linea = LineaOrden(producto=crear_producto(), cantidad=3)

    assert linea.subtotal == 1500.0


def test_linea_orden_rechaza_cantidad_invalida() -> None:
    with pytest.raises(ValueError, match="mayor que cero"):
        LineaOrden(producto=crear_producto(), cantidad=0)


def test_orden_calcula_totales_y_descuento() -> None:
    producto_teclado = crear_producto()
    producto_mouse = Producto(
        sku="SKU-002",
        nombre="Mouse",
        precio_unitario=200.0,
    )

    orden = Orden(
        id_orden="ORD-001",
        cliente="Ana",
        descuento_porcentaje=10.0,
    )
    orden.agregar_linea(LineaOrden(producto_teclado, cantidad=2))
    orden.agregar_linea(LineaOrden(producto_mouse, cantidad=3))

    assert orden.subtotal == 1600.0
    assert orden.monto_descuento == 160.0
    assert orden.total == 1440.0


def test_orden_soporta_len_y_contains() -> None:
    orden = Orden(id_orden="ORD-001", cliente="Ana")
    orden.agregar_linea(LineaOrden(crear_producto(), cantidad=1))

    assert len(orden) == 1
    assert "SKU-001" in orden
    assert "SKU-INEXISTENTE" not in orden


def test_orden_compara_por_total() -> None:
    orden_menor = Orden(id_orden="ORD-001", cliente="Ana")
    orden_menor.agregar_linea(LineaOrden(crear_producto(), cantidad=1))

    orden_mayor = Orden(id_orden="ORD-002", cliente="Bruno")
    orden_mayor.agregar_linea(LineaOrden(crear_producto(), cantidad=2))

    assert orden_menor < orden_mayor


@pytest.mark.parametrize(
    ("id_orden", "cliente", "descuento_porcentaje", "mensaje"),
    [
        ("", "Ana", 0.0, "identificador"),
        ("ORD-001", "", 0.0, "cliente"),
        ("ORD-001", "Ana", -1.0, "entre 0 y 100"),
        ("ORD-001", "Ana", 101.0, "entre 0 y 100"),
    ],
)
def test_orden_rechaza_datos_invalidos(
    id_orden: str,
    cliente: str,
    descuento_porcentaje: float,
    mensaje: str,
) -> None:
    with pytest.raises(ValueError, match=mensaje):
        Orden(
            id_orden=id_orden,
            cliente=cliente,
            descuento_porcentaje=descuento_porcentaje,
        )
