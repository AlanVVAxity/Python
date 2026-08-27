from fastapi.testclient import TestClient


def get_auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "Admin1234!",
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_create_and_get_order(client_app) -> None:
    with TestClient(client_app) as client:
        headers = get_auth_headers(client)

        create_response = client.post(
            "/orders",
            headers=headers,
            json={
                "customer_email": "cliente@example.com",
                "items": [
                    {
                        "product_name": "Producto A",
                        "quantity": 2,
                        "unit_price": 12.50,
                    }
                ],
            },
        )

        assert create_response.status_code == 201

        order_id = create_response.json()["id"]

        get_response = client.get(
            f"/orders/{order_id}",
            headers=headers,
        )

        assert get_response.status_code == 200
        assert get_response.json()["total"] == "25.00"
