from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Producto:
    """Representa un producto que puede agregarse a una orden."""

    sku: str
    nombre: str
    precio_unitario: float

    def __post_init__(self) -> None:
        """Valida los valores básicos del producto."""
        if not self.sku.strip():
            raise ValueError("El SKU no puede estar vacío.")

        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if self.precio_unitario <= 0:
            raise ValueError("El precio unitario debe ser mayor que cero.")
