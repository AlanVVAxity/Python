import pytest

from modulo_07.client import ApiClient
from modulo_07.exceptions import ApiResponseError


def test_get_returns_http_response(httpx_mock: object) -> None:
    httpx_mock.add_response(
        url="https://api.example.com/users/1",
        json={"id": 1, "name": "Ada"},
        status_code=200,
    )

    client = ApiClient(base_url="https://api.example.com")

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.data == {"id": 1, "name": "Ada"}


def test_get_raises_error_for_client_http_error(httpx_mock: object) -> None:
    httpx_mock.add_response(
        url="https://api.example.com/users/999",
        status_code=404,
        json={"detail": "Not found"},
    )

    client = ApiClient(base_url="https://api.example.com")

    with pytest.raises(ApiResponseError):
        client.get("/users/999")
