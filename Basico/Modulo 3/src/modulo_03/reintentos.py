import logging
from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger(__name__)


def reintentar(
    intentos: int = 3,
    espera_inicial: float = 0.5,
    factor_backoff: float = 2.0,
    excepciones: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Reintenta una función cuando falla con una excepción permitida."""
    if intentos < 1:
        raise ValueError("La cantidad de intentos debe ser al menos 1.")

    if espera_inicial < 0:
        raise ValueError("La espera inicial no puede ser negativa.")

    if factor_backoff < 1:
        raise ValueError("El factor de backoff debe ser mayor o igual a 1.")

    def decorador(funcion: Callable[P, T]) -> Callable[P, T]:
        @wraps(funcion)
        def envoltura(*args: P.args, **kwargs: P.kwargs) -> T:
            espera_actual = espera_inicial

            for numero_intento in range(1, intentos + 1):
                try:
                    return funcion(*args, **kwargs)
                except excepciones as error:
                    if numero_intento == intentos:
                        logger.error(
                            "La función '%s' falló después de %s intento(s).",
                            funcion.__name__,
                            intentos,
                        )
                        raise

                    logger.warning(
                        "La función '%s' falló en el intento %s/%s: %s. "
                        "Nuevo intento en %.2f segundos.",
                        funcion.__name__,
                        numero_intento,
                        intentos,
                        error,
                        espera_actual,
                    )

                    sleep(espera_actual)
                    espera_actual *= factor_backoff

            raise RuntimeError("No se pudo ejecutar la función.")

        return envoltura

    return decorador
