class ApplicationError(Exception):
    """Excepción base para errores de la capa de aplicación."""


class OrderPersistenceError(ApplicationError):
    """Se lanza cuando no es posible guardar una orden."""


class NotificationError(ApplicationError):
    """Se lanza cuando no es posible enviar una notificación."""
