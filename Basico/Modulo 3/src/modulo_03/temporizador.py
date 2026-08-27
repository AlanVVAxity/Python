import logging
from time import perf_counter
from typing import Self

logger = logging.getLogger(__name__)


class Temporizador:
    """Mide el tiempo de ejecución de un bloque gestionado con with."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.inicio = 0.0
        self.duracion = 0.0

    def __enter__(self) -> Self:
        """Inicia la medición y devuelve el temporizador."""
        self.inicio = perf_counter()
        return self

    def __exit__(
        self,
        tipo_excepcion: type[BaseException] | None,
        valor_excepcion: BaseException | None,
        traceback: object | None,
    ) -> bool:
        """Finaliza la medición y no oculta posibles excepciones."""
        self.duracion = perf_counter() - self.inicio

        logger.info(
            "El bloque '%s' tardó %.6f segundos.",
            self.nombre,
            self.duracion,
        )

        return False
