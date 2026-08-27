class DomainError(Exception):
    """Excepción base para errores de reglas del dominio."""


class InvalidOrderError(DomainError):
    """Se lanza cuando los datos de una orden no cumplen las reglas del dominio."""
