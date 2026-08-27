from modulo_08.application.ports.notification_port import NotificationPort
from modulo_08.application.ports.order_repository_port import OrderRepositoryPort
from modulo_08.application.use_cases.create_order import CreateOrderUseCase
from modulo_08.infrastructure.config import Settings
from modulo_08.infrastructure.database.session import (
    create_database_engine,
    create_database_tables,
    create_session_factory,
)
from modulo_08.infrastructure.notifications.http_notification_service import (
    HttpNotificationService,
)
from modulo_08.infrastructure.repositories.memory_order_repository import (
    MemoryOrderRepository,
)
from modulo_08.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)


class Container:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._order_repository = self._create_order_repository()
        self._notification_service = self._create_notification_service()

    def _create_order_repository(self) -> OrderRepositoryPort:
        if self._settings.repository_type == "memory":
            return MemoryOrderRepository()

        if self._settings.repository_type == "sqlalchemy":
            engine = create_database_engine(self._settings.database_url)
            create_database_tables(engine)
            session_factory = create_session_factory(engine)

            return SqlAlchemyOrderRepository(session_factory)

        raise ValueError("REPOSITORY_TYPE debe tener el valor 'memory' o 'sqlalchemy'.")

    def _create_notification_service(self) -> NotificationPort:
        return HttpNotificationService(
            base_url=self._settings.notification_base_url,
        )

    def create_order_use_case(self) -> CreateOrderUseCase:
        return CreateOrderUseCase(
            order_repository=self._order_repository,
            notification_service=self._notification_service,
        )
