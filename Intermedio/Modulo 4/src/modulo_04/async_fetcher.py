"""Funciones para descargar URLs de forma asíncrona."""

import asyncio

import httpx

from modulo_04.config import (
    MAX_CONCURRENT_REQUESTS,
    REQUEST_TIMEOUT_SECONDS,
)
from modulo_04.sync_fetcher import FetchResult


async def fetch_url_async(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    url: str,
) -> FetchResult:
    """Descarga una URL respetando el límite de concurrencia."""
    async with semaphore:
        response = await client.get(url)
        response.raise_for_status()

    return FetchResult(
        url=url,
        status_code=response.status_code,
        content_length=len(response.content),
    )


async def fetch_all_async(urls: list[str]) -> list[FetchResult]:
    """Descarga todas las URLs de manera concurrente."""
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [
            fetch_url_async(client=client, semaphore=semaphore, url=url) for url in urls
        ]
        return await asyncio.gather(*tasks)
