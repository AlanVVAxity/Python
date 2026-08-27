from uuid import UUID

from orders_service.application.exceptions import OrderNotFoundApplicationError
from orders_service.domain.repositories import OrderRepository


class DeleteOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self, order_id: UUID) -> None:
        deleted = self.repository.delete(order_id)

        if not deleted:
            raise OrderNotFoundApplicationError("Orden no encontrada.")
