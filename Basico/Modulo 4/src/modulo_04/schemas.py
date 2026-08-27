from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductoIn(BaseModel):
    """Representa los datos de entrada de un producto."""

    sku: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    precio_unitario: float = Field(gt=0)

    @field_validator("sku", "nombre")
    @classmethod
    def validar_texto_no_vacio(cls, valor: str) -> str:
        """Elimina espacios y rechaza textos vacíos."""
        valor_limpio = valor.strip()

        if not valor_limpio:
            raise ValueError("El texto no puede estar vacío.")

        return valor_limpio


class LineaOrdenIn(BaseModel):
    """Representa una línea de orden recibida como entrada."""

    producto: ProductoIn
    cantidad: int = Field(gt=0)


class OrderIn(BaseModel):
    """Representa los datos de entrada para crear una orden."""

    id_orden: str = Field(min_length=1, max_length=50)
    cliente: str = Field(min_length=1, max_length=100)
    lineas: list[LineaOrdenIn] = Field(min_length=1)
    descuento_porcentaje: float = Field(default=0.0, ge=0, le=100)

    @field_validator("id_orden", "cliente")
    @classmethod
    def validar_texto_no_vacio(cls, valor: str) -> str:
        """Elimina espacios y rechaza identificadores o clientes vacíos."""
        valor_limpio = valor.strip()

        if not valor_limpio:
            raise ValueError("El texto no puede estar vacío.")

        return valor_limpio


class ProductoOut(BaseModel):
    """Representa un producto serializado como respuesta."""

    model_config = ConfigDict(from_attributes=True)

    sku: str
    nombre: str
    precio_unitario: float


class LineaOrdenOut(BaseModel):
    """Representa una línea de orden serializada como respuesta."""

    model_config = ConfigDict(from_attributes=True)

    sku: str
    nombre_producto: str
    cantidad: int
    subtotal: float


class OrderOut(BaseModel):
    """Representa una orden serializada como respuesta."""

    id_orden: str
    cliente: str
    cantidad_lineas: int
    subtotal: float
    descuento_porcentaje: float
    monto_descuento: float
    total: float
