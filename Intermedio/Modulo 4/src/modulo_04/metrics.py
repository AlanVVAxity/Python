"""Utilidades para medir tiempos de ejecución."""

from collections.abc import Callable
from time import perf_counter
from typing import TypeVar

T = TypeVar("T")


def measure_execution(
    function: Callable[..., T],
    *args: object,
    **kwargs: object,
) -> tuple[T, float]:
    """Ejecuta una función y devuelve su resultado junto con el tiempo usado."""
    start_time = perf_counter()
    result = function(*args, **kwargs)
    elapsed_time = perf_counter() - start_time

    return result, elapsed_time
