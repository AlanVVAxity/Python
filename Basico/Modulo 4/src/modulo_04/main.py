from pydantic import ValidationError

from modulo_04.conversores import (
    convertir_orden_a_order_out,
    convertir_order_in_a_orden,
)
from modulo_04.schemas import OrderIn


def obtener_datos_orden_demo() -> dict[str, object]:
    """Devuelve una orden de ejemplo similar a una entrada JSON."""
    return {
        "id_orden": "ORD-001",
        "cliente": "Ana",
        "lineas": [
            {
                "producto": {
                    "sku": "SKU-001",
                    "nombre": "Teclado",
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


def main() -> None:
    """Valida una entrada, crea una entidad de dominio y la serializa."""
    datos_entrada = obtener_datos_orden_demo()

    try:
        order_in = OrderIn.model_validate(datos_entrada)
        orden = convertir_order_in_a_orden(order_in)
        order_out = convertir_orden_a_order_out(orden)
    except ValidationError as error:
        print("La orden recibida no es válida:")
        print(error)
        return

    print("=== Orden creada correctamente ===")
    print(f"Orden: {order_out.id_orden}")
    print(f"Cliente: {order_out.cliente}")
    print(f"Líneas: {order_out.cantidad_lineas}")
    print(f"Subtotal: ${order_out.subtotal:,.2f}")
    print(f"Descuento: ${order_out.monto_descuento:,.2f}")
    print(f"Total: ${order_out.total:,.2f}")

    print("\n=== Orden serializada ===")
    print(order_out.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
