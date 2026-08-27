from fastapi.testclient import TestClient


def test_create_order_returns_created_order(api_client: TestClient) -> None:
    response = api_client.post(
        "/orders",
        json={
            "customer_email": "cliente@example.com",
            "product_name": "Audífonos",
            "quantity": 2,
            "unit_price": "79.90",
        },
    )

    body = response.json()

    assert response.status_code == 201
    assert body["customer_email"] == "cliente@example.com"
    assert body["product_name"] == "Audífonos"
    assert body["quantity"] == 2
    assert body["unit_price"] == "79.90"
    assert body["total_price"] == "159.80"
    assert body["status"] == "pending"
    assert "id" in body
    assert "created_at" in body


def test_create_order_rejects_invalid_request(api_client: TestClient) -> None:
    response = api_client.post(
        "/orders",
        json={
            "customer_email": "correo-invalido",
            "product_name": "",
            "quantity": 0,
            "unit_price": "0",
        },
    )

    assert response.status_code == 422
