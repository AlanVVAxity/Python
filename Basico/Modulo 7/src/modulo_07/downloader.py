from pathlib import Path

import httpx

from modulo_07.exceptions import (
    ApiConnectionError,
    ApiResponseError,
    ApiTimeoutError,
)


def download_file(
    url: str,
    destination: Path,
    timeout_seconds: float = 30.0,
    chunk_size: int = 8192,
) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        with httpx.stream(
            "GET",
            url,
            timeout=httpx.Timeout(timeout_seconds),
            follow_redirects=True,
        ) as response:
            response.raise_for_status()

            with destination.open("wb") as file:
                for chunk in response.iter_bytes(chunk_size=chunk_size):
                    file.write(chunk)

    except httpx.TimeoutException as error:
        raise ApiTimeoutError(
            f"La descarga desde {url} excedió el tiempo de espera."
        ) from error

    except httpx.ConnectError as error:
        raise ApiConnectionError(f"No fue posible conectar con {url}.") from error

    except httpx.HTTPStatusError as error:
        raise ApiResponseError(
            f"No fue posible descargar el archivo. "
            f"Estado HTTP: {error.response.status_code}."
        ) from error

    return destination
