"""Unit tests for order API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.data import SAMPLE_ORDERS
from app.main import app
from app.models import OrderStatus


@pytest.fixture
def client() -> TestClient:
    """Create a TestClient fixture for invoking FastAPI routes.

    Example:
        >>> cl = client()
        >>> isinstance(cl, TestClient)
        True
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_order_statuses() -> None:
    """Reset mutable sample order statuses before each test.

    Example:
        >>> reset_order_statuses()
    """
    original_statuses = {
        1: OrderStatus.DELIVERED,
        2: OrderStatus.SHIPPED,
        3: OrderStatus.PROCESSING,
    }
    for order in SAMPLE_ORDERS:
        if order.id in original_statuses:
            order.status = original_statuses[order.id]


def test_list_orders_success(client: TestClient) -> None:
    """Test GET /orders returns HTTP 200 and a populated list of orders."""
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

    first = data[0]
    assert "id" in first
    assert "customer_name" in first
    assert "customer_email" in first
    assert "items" in first
    assert "total_amount" in first
    assert "status" in first


def test_get_order_by_id_success(client: TestClient) -> None:
    """Test GET /orders/{order_id} returns 200 with matching order details."""
    response = client.get("/orders/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["customer_name"] == "Alice Johnson"
    assert data["customer_email"] == "alice.johnson@example.com"
    assert len(data["items"]) == 2
    assert data["total_amount"] == 249.89
    assert data["status"] == "delivered"


def test_get_order_by_id_not_found(client: TestClient) -> None:
    """Test GET /orders/{order_id} returns 404 when ID does not exist."""
    response = client.get("/orders/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Order with id 99999 not found"


def test_get_order_by_invalid_id_type(client: TestClient) -> None:
    """Test GET /orders/{order_id} returns 422 when ID is not an integer."""
    response = client.get("/orders/invalid-id")
    assert response.status_code == 422


def test_cancel_order_success(client: TestClient) -> None:
    """Test PATCH /orders/{order_id}/cancel cancels an eligible order.

    Example:
        >>> isinstance("cancelled", str)
        True
    """
    response = client.patch("/orders/3/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["status"] == "cancelled"


def test_cancel_order_not_found(client: TestClient) -> None:
    """Test PATCH /orders/{order_id}/cancel returns 404 for a missing order.

    Example:
        >>> 99999 > 0
        True
    """
    response = client.patch("/orders/99999/cancel")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Order with id 99999 not found"


def test_cancel_shipped_order_conflict(client: TestClient) -> None:
    """Test PATCH /orders/{order_id}/cancel returns 409 for a shipped order.

    Example:
        >>> "shipped" in "Order has shipped"
        True
    """
    response = client.patch("/orders/2/cancel")
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Order with id 2 cannot be cancelled after it has shipped"


def test_cancel_delivered_order_conflict(client: TestClient) -> None:
    """Test PATCH /orders/{order_id}/cancel returns 409 for a delivered order.

    Example:
        >>> "delivered" in "Order has delivered"
        True
    """
    response = client.patch("/orders/1/cancel")
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Order with id 1 cannot be cancelled after it has delivered"


def test_cancel_already_cancelled_order_conflict(client: TestClient) -> None:
    """Test PATCH /orders/{order_id}/cancel returns 409 when already cancelled.

    Example:
        >>> "cancelled" == "cancelled"
        True
    """
    first_response = client.patch("/orders/3/cancel")
    assert first_response.status_code == 200

    second_response = client.patch("/orders/3/cancel")
    assert second_response.status_code == 409
    data = second_response.json()
    assert data["detail"] == "Order with id 3 is already cancelled"


def test_cancel_order_invalid_id_type(client: TestClient) -> None:
    """Test PATCH /orders/{order_id}/cancel returns 422 for non-integer ID.

    Example:
        >>> isinstance("invalid-id", str)
        True
    """
    response = client.patch("/orders/invalid-id/cancel")
    assert response.status_code == 422
