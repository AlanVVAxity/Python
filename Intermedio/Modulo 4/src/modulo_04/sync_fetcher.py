"""Funciones para descargar URLs de forma síncrona."""

from dataclasses import dataclass

import httpx

from modulo_04.config import REQUEST_TIMEOUT_SECONDS


@dataclass(frozen=True)
class FetchResult:
    """Resultado de una solicitud HTTP."""

    url: str
    status_code: int
    content_length: int


def fetch_url_sync(url: str) -> FetchResult:
    """Descarga una URL de forma síncrona."""
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url)
        response.raise_for_status()

    return FetchResult(
        url=url,
        status_code=response.status_code,
        content_length=len(response.content),
    )


def fetch_all_sync(urls: list[str]) -> list[FetchResult]:
    """Descarga todas las URLs una por una."""
    return [fetch_url_sync(url) for url in urls]
