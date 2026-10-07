"""Unit tests for product API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.data import SAMPLE_PRODUCTS
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


@pytest.fixture(autouse=True)
def reset_product_descriptions() -> None:
    """Reset mutable sample product descriptions before each test.

    Example:
        >>> reset_product_descriptions()
    """
    original_descriptions = {prod.id: prod.description for prod in SAMPLE_PRODUCTS}
    yield
    for prod in SAMPLE_PRODUCTS:
        if prod.id in original_descriptions:
            prod.description = original_descriptions[prod.id]


def test_list_products_success(client: TestClient) -> None:
    """Test GET /products returns HTTP 200 and a populated list of products."""
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5

    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "price" in first
    assert "category" in first
    assert "inventory" in first


def test_get_product_by_id_success(client: TestClient) -> None:
    """Test GET /products/{product_id} returns 200 with the matching product."""
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Wireless Noise-Canceling Headphones"
    assert data["price"] == 199.99
    assert data["category"] == "Electronics"


def test_get_product_by_id_not_found(client: TestClient) -> None:
    """Test GET /products/{product_id} returns 404 when ID does not exist."""
    response = client.get("/products/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product with id 99999 not found"


def test_get_product_by_invalid_id_type(client: TestClient) -> None:
    """Test GET /products/{product_id} returns 422 when ID is not an integer."""
    response = client.get("/products/abc")
    assert response.status_code == 422


def test_update_product_description_success(client: TestClient) -> None:
    """Test PATCH /products/{product_id}/description successfully updates description."""
    payload = {"description": "Updated over-ear Bluetooth headphones with 45-hour battery."}
    response = client.patch("/products/1/description", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["description"] == payload["description"]
    assert data["name"] == "Wireless Noise-Canceling Headphones"

    # Verify updated description persists on retrieval
    get_response = client.get("/products/1")
    assert get_response.status_code == 200
    assert get_response.json()["description"] == payload["description"]


def test_update_product_description_not_found(client: TestClient) -> None:
    """Test PATCH /products/{product_id}/description returns 404 for non-existent product."""
    payload = {"description": "New description for missing product."}
    response = client.patch("/products/99999/description", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product with id 99999 not found"


def test_update_product_description_invalid_id_type(client: TestClient) -> None:
    """Test PATCH /products/{product_id}/description returns 422 when ID is not an integer."""
    payload = {"description": "Updated description"}
    response = client.patch("/products/invalid-id/description", json=payload)
    assert response.status_code == 422


def test_update_product_description_empty_string(client: TestClient) -> None:
    """Test PATCH /products/{product_id}/description returns 422 for empty description."""
    payload = {"description": ""}
    response = client.patch("/products/1/description", json=payload)
    assert response.status_code == 422


def test_update_product_description_missing_field(client: TestClient) -> None:
    """Test PATCH /products/{product_id}/description returns 422 when description is missing."""
    response = client.patch("/products/1/description", json={})
    assert response.status_code == 422

