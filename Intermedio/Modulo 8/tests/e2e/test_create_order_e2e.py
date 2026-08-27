from decimal import Decimal

import httpx
import pytest

from modulo_08.application.dto import CreateOrderInput
from modulo_08.application.use_cases.create_order import CreateOrderUseCase
from modulo_08.infrastructure.notifications.http_notification_service import (
    HttpNotificationService,
)
from modulo_08.infrastructure.repositories.memory_order_repository import (
    MemoryOrderRepository,
)


@pytest.mark.e2e
def test_create_order_sends_notification_to_mock_server() -> None:
    repository = MemoryOrderRepository()

    with httpx.Client(base_url="http://localhost:8081", timeout=5.0) as client:
        notification_service = HttpNotificationService(
            base_url="http://localhost:8081",
            client=client,
        )
        use_case = CreateOrderUseCase(
            order_repository=repository,
            notification_service=notification_service,
        )

        result = use_case.execute(
            CreateOrderInput(
                customer_email="cliente@example.com",
                product_name="Webcam",
                quantity=1,
                unit_price=Decimal("89.90"),
            )
        )

    assert repository.get_by_id(result.id) is not None
