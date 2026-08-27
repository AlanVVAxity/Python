import time
from typing import Any

import httpx

from modulo_07.exceptions import (
    ApiConnectionError,
    ApiResponseError,
    ApiTimeoutError,
)
from modulo_07.models import HttpResponse


class ApiClient:
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 10.0,
        max_retries: int = 3,
        retry_delay_seconds: float = 1.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

    def get(self, path: str) -> HttpResponse:
        url = f"{self.base_url}/{path.lstrip('/')}"
        timeout = httpx.Timeout(self.timeout_seconds)

        for attempt in range(1, self.max_retries + 1):
            try:
                with httpx.Client(timeout=timeout) as client:
                    response = client.get(url)

                if response.status_code >= 500:
                    if attempt == self.max_retries:
                        raise ApiResponseError(
                            f"El servidor respondió con estado "
                            f"{response.status_code} después de "
                            f"{self.max_retries} intentos."
                        )

                    time.sleep(self.retry_delay_seconds)
                    continue

                response.raise_for_status()

                data: dict[str, Any] = response.json()
                return HttpResponse(
                    status_code=response.status_code,
                    data=data,
                )

            except httpx.TimeoutException as error:
                if attempt == self.max_retries:
                    raise ApiTimeoutError(
                        f"La solicitud a {url} excedió el tiempo de espera."
                    ) from error

                time.sleep(self.retry_delay_seconds)

            except httpx.ConnectError as error:
                if attempt == self.max_retries:
                    raise ApiConnectionError(
                        f"No fue posible conectar con {url}."
                    ) from error

                time.sleep(self.retry_delay_seconds)

            except httpx.HTTPStatusError as error:
                raise ApiResponseError(
                    f"El servicio respondió con estado {error.response.status_code}."
                ) from error

        raise ApiResponseError("No fue posible completar la solicitud.")
