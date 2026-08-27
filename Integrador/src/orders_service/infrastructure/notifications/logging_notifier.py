import logging

from orders_service.domain.entities import Order

logger = logging.getLogger(__name__)


class LoggingOrderNotifier:
    def order_created(self, order: Order) -> None:
        logger.info(
            "Orden creada: id=%s customer_email=%s total=%s",
            order.id,
            order.customer_email,
            order.total,
        )
