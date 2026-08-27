from datetime import UTC
from uuid import UUID

from sqlalchemy.orm import Session, sessionmaker

from modulo_08.domain.entities import Order
from modulo_08.domain.value_objects import OrderStatus
from modulo_08.infrastructure.database.models import OrderModel


class SqlAlchemyOrderRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, order: Order) -> Order:
        order_model = OrderModel(
            id=str(order.id),
            customer_email=order.customer_email,
            product_name=order.product_name,
            quantity=order.quantity,
            unit_price=order.unit_price,
            status=order.status.value,
            created_at=order.created_at,
        )

        with self._session_factory() as session:
            session.add(order_model)
            session.commit()

        return order

    def get_by_id(self, order_id: UUID) -> Order | None:
        with self._session_factory() as session:
            order_model = session.get(OrderModel, str(order_id))

            if order_model is None:
                return None

            created_at = order_model.created_at

            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)

            return Order(
                id=UUID(order_model.id),
                customer_email=order_model.customer_email,
                product_name=order_model.product_name,
                quantity=order_model.quantity,
                unit_price=order_model.unit_price,
                status=OrderStatus(order_model.status),
                created_at=created_at,
            )
