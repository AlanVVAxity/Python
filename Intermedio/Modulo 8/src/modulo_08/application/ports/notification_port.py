from typing import Protocol

from modulo_08.domain.entities import Order


class NotificationPort(Protocol):
    def send_order_created(self, order: Order) -> None:
        """Envía una notificación cuando se crea una orden."""
