from typing import Any

import httpx

from modulo_08.application.exceptions import NotificationError
from modulo_08.domain.entities import Order


class HttpNotificationService:
    def __init__(
        self,
        base_url: str,
        client: httpx.Client | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = client

    def send_order_created(self, order: Order) -> None:
        payload: dict[str, Any] = {
            "event": "order.created",
            "order_id": str(order.id),
            "customer_email": order.customer_email,
            "product_name": order.product_name,
            "quantity": order.quantity,
            "unit_price": str(order.unit_price),
            "total_price": str(order.total_price),
            "status": order.status.value,
            "created_at": order.created_at.isoformat(),
        }

        try:
            if self._client is not None:
                response = self._client.post(
                    url="/notifications",
                    json=payload,
                )
            else:
                response = httpx.post(
                    url=f"{self._base_url}/notifications",
                    json=payload,
                    timeout=5.0,
                )

            response.raise_for_status()
        except httpx.HTTPError as error:
            raise NotificationError(
                "No fue posible enviar la notificación de orden creada."
            ) from error
