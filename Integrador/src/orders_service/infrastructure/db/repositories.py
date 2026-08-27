from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from orders_service.domain.entities import Order, OrderItem, OrderStatus
from orders_service.infrastructure.db.models import OrderItemModel, OrderModel


class SqlAlchemyOrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, order: Order) -> Order:
        model = self._to_model(order)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, order_id: UUID) -> Order | None:
        statement = (
            select(OrderModel)
            .where(OrderModel.id == order_id)
            .options(selectinload(OrderModel.items))
        )
        model = self.session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)

    def list_all(self) -> list[Order]:
        statement = select(OrderModel).options(selectinload(OrderModel.items))
        models = self.session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    def update(self, order: Order) -> Order:
        model = self.session.get(OrderModel, order.id)

        if model is None:
            raise ValueError("Orden no encontrada.")

        model.status = order.status.value
        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def delete(self, order_id: UUID) -> bool:
        model = self.session.get(OrderModel, order_id)

        if model is None:
            return False

        self.session.delete(model)
        self.session.commit()
        return True

    @staticmethod
    def _to_model(order: Order) -> OrderModel:
        return OrderModel(
            id=order.id,
            customer_email=order.customer_email,
            status=order.status.value,
            items=[
                OrderItemModel(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in order.items
            ],
        )

    @staticmethod
    def _to_entity(model: OrderModel) -> Order:
        return Order(
            id=model.id,
            customer_email=model.customer_email,
            status=OrderStatus(model.status),
            items=[
                OrderItem(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=Decimal(str(item.unit_price)),
                )
                for item in model.items
            ],
        )
