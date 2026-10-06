"""Unit tests for order API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a TestClient fixture for invoking FastAPI routes.

    Example:
        >>> cl = client()
        >>> isinstance(cl, TestClient)
        True
    """
    return TestClient(app)


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
