from fastapi.testclient import TestClient

from modulo_02.main import app

client = TestClient(app)


def create_order_payload() -> dict[str, object]:
    return {
        "customer_name": "María González",
        "items": [
            {
                "product_name": "Teclado mecánico",
                "quantity": 2,
                "unit_price": "999.99",
            }
        ],
    }


def test_create_order_returns_created_order() -> None:
    response = client.post("/orders", json=create_order_payload())

    assert response.status_code == 201

    body = response.json()
    assert body["customer_name"] == "María González"
    assert body["total"] == "1999.98"
    assert "id" in body


def test_list_orders_returns_orders() -> None:
    client.post("/orders", json=create_order_payload())

    response = client.get("/orders")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_order_returns_order() -> None:
    created_response = client.post("/orders", json=create_order_payload())
    order_id = created_response.json()["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_get_order_returns_not_found_for_unknown_id() -> None:
    unknown_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/orders/{unknown_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_update_order_updates_customer_and_total() -> None:
    created_response = client.post("/orders", json=create_order_payload())
    order_id = created_response.json()["id"]

    update_payload = {
        "customer_name": "María González López",
        "items": [
            {
                "product_name": "Monitor",
                "quantity": 1,
                "unit_price": "3500.00",
            }
        ],
    }

    response = client.put(f"/orders/{order_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["customer_name"] == "María González López"
    assert response.json()["total"] == "3500.00"


def test_delete_order_removes_order() -> None:
    created_response = client.post("/orders", json=create_order_payload())
    order_id = created_response.json()["id"]

    delete_response = client.delete(f"/orders/{order_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.status_code == 404