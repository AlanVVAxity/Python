from modulo_04.ordenes import LineaOrden, Orden
from modulo_04.productos import Producto
from modulo_04.schemas import (
    LineaOrdenOut,
    OrderIn,
    OrderOut,
    ProductoOut,
)


def convertir_order_in_a_orden(datos_entrada: OrderIn) -> Orden:
    """Convierte un modelo Pydantic de entrada en una entidad Orden."""
    lineas = [
        LineaOrden(
            producto=Producto(
                sku=linea.producto.sku,
                nombre=linea.producto.nombre,
                precio_unitario=linea.producto.precio_unitario,
            ),
            cantidad=linea.cantidad,
        )
        for linea in datos_entrada.lineas
    ]

    return Orden(
        id_orden=datos_entrada.id_orden,
        cliente=datos_entrada.cliente,
        lineas=lineas,
        descuento_porcentaje=datos_entrada.descuento_porcentaje,
    )


def convertir_producto_a_producto_out(producto: Producto) -> ProductoOut:
    """Convierte una entidad Producto a su modelo serializable."""
    return ProductoOut.model_validate(producto)


def convertir_linea_a_linea_out(linea: LineaOrden) -> LineaOrdenOut:
    """Convierte una línea de orden a un modelo serializable."""
    return LineaOrdenOut(
        sku=linea.producto.sku,
        nombre_producto=linea.producto.nombre,
        cantidad=linea.cantidad,
        subtotal=linea.subtotal,
    )


def convertir_orden_a_order_out(orden: Orden) -> OrderOut:
    """Convierte una entidad Orden a un modelo de salida."""
    return OrderOut(
        id_orden=orden.id_orden,
        cliente=orden.cliente,
        cantidad_lineas=len(orden),
        subtotal=orden.subtotal,
        descuento_porcentaje=orden.descuento_porcentaje,
        monto_descuento=orden.monto_descuento,
        total=orden.total,
    )
