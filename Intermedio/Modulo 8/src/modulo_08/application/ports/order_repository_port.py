from typing import Protocol
from uuid import UUID

from modulo_08.domain.entities import Order


class OrderRepositoryPort(Protocol):
    def save(self, order: Order) -> Order:
        """Guarda una orden y devuelve la orden persistida."""

    def get_by_id(self, order_id: UUID) -> Order | None:
        """Busca una orden por su identificador."""
