from collections.abc import Generator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from modulo_08.application.use_cases.create_order import CreateOrderUseCase
from modulo_08.domain.entities import Order
from modulo_08.infrastructure.database.base import Base
from modulo_08.infrastructure.repositories.memory_order_repository import (
    MemoryOrderRepository,
)
from modulo_08.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)
from modulo_08.main import app
from modulo_08.presentation.dependencies import get_create_order_use_case


class FakeNotificationService:
    def __init__(self) -> None:
        self.sent_orders: list[Order] = []

    def send_order_created(self, order: Order) -> None:
        self.sent_orders.append(order)


@pytest.fixture
def order_data() -> dict[str, object]:
    return {
        "customer_email": "cliente@example.com",
        "product_name": "Teclado mecánico",
        "quantity": 2,
        "unit_price": Decimal("49.90"),
    }


@pytest.fixture
def memory_repository() -> MemoryOrderRepository:
    return MemoryOrderRepository()


@pytest.fixture
def fake_notification_service() -> FakeNotificationService:
    return FakeNotificationService()


@pytest.fixture
def sqlite_session_factory() -> Generator[sessionmaker[Session], None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    yield factory

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def sqlalchemy_repository(
    sqlite_session_factory: sessionmaker[Session],
) -> SqlAlchemyOrderRepository:
    return SqlAlchemyOrderRepository(sqlite_session_factory)


@pytest.fixture
def api_client(
    memory_repository: MemoryOrderRepository,
    fake_notification_service: FakeNotificationService,
) -> Generator[TestClient, None, None]:
    use_case = CreateOrderUseCase(
        order_repository=memory_repository,
        notification_service=fake_notification_service,
    )

    app.dependency_overrides[get_create_order_use_case] = lambda: use_case

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
