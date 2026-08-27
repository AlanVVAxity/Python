"""Pruebas básicas para los módulos de descarga HTTP."""

from modulo_04.async_fetcher import fetch_all_async
from modulo_04.sync_fetcher import FetchResult


def test_fetch_result_stores_expected_values() -> None:
    """Verifica que FetchResult conserve los datos proporcionados."""
    result = FetchResult(
        url="https://example.com",
        status_code=200,
        content_length=100,
    )

    assert result.url == "https://example.com"
    assert result.status_code == 200
    assert result.content_length == 100


async def test_async_fetcher_with_empty_url_list() -> None:
    """Verifica que una lista vacía devuelva una lista vacía."""
    results = await fetch_all_async([])

    assert results == []
