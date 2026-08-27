from decimal import Decimal

from modulo_08.application.dto import CreateOrderInput
from modulo_08.application.use_cases.create_order import CreateOrderUseCase
from modulo_08.infrastructure.repositories.memory_order_repository import (
    MemoryOrderRepository,
)
from tests.conftest import FakeNotificationService


def test_create_order_saves_order_and_sends_notification() -> None:
    repository = MemoryOrderRepository()
    notification_service = FakeNotificationService()
    use_case = CreateOrderUseCase(
        order_repository=repository,
        notification_service=notification_service,
    )

    result = use_case.execute(
        CreateOrderInput(
            customer_email="cliente@example.com",
            product_name="Mouse inalámbrico",
            quantity=3,
            unit_price=Decimal("15.50"),
        )
    )

    saved_order = repository.get_by_id(result.id)

    assert saved_order is not None
    assert saved_order.id == result.id
    assert result.total_price == Decimal("46.50")
    assert len(notification_service.sent_orders) == 1
    assert notification_service.sent_orders[0].id == result.id
