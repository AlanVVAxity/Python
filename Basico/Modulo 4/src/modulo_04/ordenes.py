from dataclasses import dataclass, field

from modulo_04.productos import Producto


@dataclass(frozen=True, slots=True)
class LineaOrden:
    """Representa un producto y la cantidad solicitada dentro de una orden."""

    producto: Producto
    cantidad: int

    def __post_init__(self) -> None:
        """Valida la cantidad solicitada."""
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

    @property
    def subtotal(self) -> float:
        """Calcula el importe de la línea."""
        return self.producto.precio_unitario * self.cantidad


@dataclass(slots=True)
class Orden:
    """Representa una orden de compra compuesta por líneas de productos."""

    id_orden: str
    cliente: str
    lineas: list[LineaOrden] = field(default_factory=list)
    descuento_porcentaje: float = 0.0

    def __post_init__(self) -> None:
        """Valida los datos generales de la orden."""
        if not self.id_orden.strip():
            raise ValueError("El identificador de orden no puede estar vacío.")

        if not self.cliente.strip():
            raise ValueError("El cliente no puede estar vacío.")

        if not 0 <= self.descuento_porcentaje <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")

    def agregar_linea(self, linea: LineaOrden) -> None:
        """Agrega una línea de producto a la orden."""
        self.lineas.append(linea)

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal de todas las líneas."""
        return sum(linea.subtotal for linea in self.lineas)

    @property
    def monto_descuento(self) -> float:
        """Calcula el monto monetario del descuento."""
        return self.subtotal * (self.descuento_porcentaje / 100)

    @property
    def total(self) -> float:
        """Calcula el total final de la orden."""
        return self.subtotal - self.monto_descuento

    def __len__(self) -> int:
        """Devuelve la cantidad de líneas incluidas en la orden."""
        return len(self.lineas)

    def __contains__(self, sku: str) -> bool:
        """Indica si una línea de la orden contiene el SKU indicado."""
        return any(linea.producto.sku == sku for linea in self.lineas)

    def __lt__(self, otra: object) -> bool:
        """Compara órdenes por su total."""
        if not isinstance(otra, Orden):
            return NotImplemented

        return self.total < otra.total
