from collections.abc import Iterator, Sequence
from typing import TypeVar

T = TypeVar("T")


def dividir_en_lotes[T](
    elementos: Sequence[T],
    tamano_lote: int,
) -> Iterator[list[T]]:
    """Genera listas de elementos divididas en lotes del tamaño indicado."""
    if tamano_lote <= 0:
        raise ValueError("El tamaño del lote debe ser mayor que cero.")

    for inicio in range(0, len(elementos), tamano_lote):
        fin = inicio + tamano_lote
        yield list(elementos[inicio:fin])
