---
name: fastapi-rest-api
description: "Develop REST API endpoints, Pydantic schemas, and APIRouter modules with FastAPI and TestClient. Use when designing, creating, or extending REST APIs, implementing request/response validation, adding route handlers, or writing integration tests with pytest."
user-invocable: true
argument-hint: "Resource or endpoint to build (e.g., 'customers CRUD' or 'POST /cart/items')"
---

# FastAPI REST API Development

Standardized workflow for designing, implementing, and testing modular REST API endpoints in this repository using FastAPI, Pydantic, and pytest.

## When to Use

- Creating a new RESTful resource or router module under `app/routers/`
- Adding new endpoints (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) to existing routers
- Defining or refining Pydantic models for request validation and response serialization in `app/models.py`
- Writing integration tests using `fastapi.testclient.TestClient` under `tests/`
- Reviewing or refactoring endpoints to ensure compliance with codebase conventions (Python 3.13+ typing, doctest docstrings, OpenAPI metadata)

---

## Step-by-Step Workflow

### 1. Define Pydantic Models (`app/models.py`)
- Use built-in Python 3.13+ types (`list[T]`, `dict[K, V]`, `str | None`) rather than typing module aliases (`List`, `Optional`).
- Separate request/create schemas from response/domain models when client inputs differ from persisted entities (e.g., omit auto-generated IDs or internal timestamps from creation payloads).
- Add field constraints and descriptions with `Field(...)` (`ge`, `le`, `min_length`, `description`).
- Include a docstring with an `Example:` doctest block on every model and helper method.

### 2. Implement Data Access / Store Helpers (`app/data.py`)
- Define helper functions for retrieval, insertion, and mutation.
- Return model instances or `None` on missing records.
- Annotate parameter and return types strictly.
- Include a docstring with an `Example:` doctest block for each function.

### 3. Create or Extend the Router (`app/routers/<resource>.py`)
- Instantiate `router = APIRouter(prefix="/<resource>", tags=["<ResourceTag>"])`.
- Follow REST resource naming conventions (plural nouns, kebab-case path parameters like `{product_id}`).
- Decorate routes with explicit HTTP method decorators (`@router.get`, `@router.post`, etc.).
- Set OpenAPI metadata: `summary`, `description`, `response_model`, and `responses={...}` for error codes.
- Use semantic HTTP status codes via `fastapi.status` (e.g., `status.HTTP_201_CREATED` for resource creation).
- Raise explicit `HTTPException(status_code=..., detail=...)` for error states (e.g., 404 for missing resources).
- Provide a docstring with an `Example:` doctest block for each route handler function.

### 4. Register the Router (`app/main.py`)
- If creating a new router, import it and register with `app.include_router(<module>.router)` in `create_app()`.

### 5. Write Integration Tests (`tests/test_<resource>.py`)
- Create a test module prefixed with `test_` under `tests/`.
- Use a `TestClient(app)` fixture to exercise endpoints over HTTP.
- Cover:
  - **Happy paths**: Status 200/201/204 with payload validation.
  - **Error handling**: Status 404 for missing IDs, 409 for conflicts.
  - **Validation errors**: Status 422 for malformed payloads or missing required fields.
- Include docstrings on fixtures and test functions.

### 6. Run & Verify
- Execute the test suite using `pytest` to confirm all endpoints, status codes, and contracts pass.

---

## Blueprint Code Examples

### 1. Model Blueprint (`app/models.py`)

```python
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """Payload schema for submitting a product review.

    Example:
        >>> payload = ReviewCreate(rating=5, comment="Excellent build quality!")
        >>> payload.rating
        5
    """

    rating: int = Field(..., ge=1, le=5, description="Review rating between 1 and 5 stars")
    comment: str = Field(..., min_length=3, description="Customer review commentary")


class Review(ReviewCreate):
    """Review entity representation including system-assigned fields.

    Example:
        >>> review = Review(id=1, product_id=10, rating=5, comment="Great product!")
        >>> review.id
        1
    """

    id: int = Field(..., ge=1, description="Unique review identifier")
    product_id: int = Field(..., ge=1, description="Identifier of the reviewed product")
```

### 2. Router Blueprint (`app/routers/<resource>.py`)

```python
from fastapi import APIRouter, HTTPException, status
from app.models import Review, ReviewCreate

router = APIRouter(prefix="/products/{product_id}/reviews", tags=["Reviews"])


@router.post(
    "",
    response_model=Review,
    status_code=status.HTTP_201_CREATED,
    summary="Create a review for a product",
    description="Submit a new rating and comment for the specified product.",
    responses={
        404: {"description": "Product not found"},
        422: {"description": "Validation error"},
    },
)
def create_product_review(product_id: int, review_in: ReviewCreate) -> Review:
    """Create and persist a new review for a given product.

    Raises:
        HTTPException: 404 if the target product does not exist.

    Example:
        >>> from app.models import ReviewCreate
        >>> payload = ReviewCreate(rating=5, comment="Solid performance.")
        >>> review = create_product_review(1, payload)
        >>> review.product_id
        1
    """
    # Verify parent resource existence
    # Persist and return created entity
    ...
```

### 3. Test Blueprint (`tests/test_<resource>.py`)

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Provide a TestClient instance bound to the FastAPI application.

    Example:
        >>> cl = client()
        >>> isinstance(cl, TestClient)
        True
    """
    return TestClient(app)


def test_create_review_success(client: TestClient) -> None:
    """Test POST review returns HTTP 201 with populated review payload."""
    payload = {"rating": 5, "comment": "Outstanding build quality!"}
    response = client.post("/products/1/reviews", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == 1
    assert data["rating"] == 5
    assert "id" in data


def test_create_review_validation_error(client: TestClient) -> None:
    """Test POST review with invalid rating returns HTTP 422."""
    payload = {"rating": 10, "comment": "Too high rating"}
    response = client.post("/products/1/reviews", json=payload)
    assert response.status_code == 422
```

---

## Pre-Commit Checklist

Before finalizing any FastAPI endpoint implementation or modification:

- [ ] **Python 3.13+ Typing**: Used modern syntax (`list[T]`, `dict[K, V]`, `T | None`) without importing `Optional` or `List` from `typing`.
- [ ] **Docstrings with Doctest Examples**: Every model, route handler, helper, and test fixture includes a docstring containing an `Example:` doctest block (`>>>`).
- [ ] **Modularity**: Endpoints are grouped in an `APIRouter` with dedicated `prefix` and `tags`.
- [ ] **Contract Validation**: `response_model` is explicitly specified on route decorators to ensure correct serialization and avoid data leaks.
- [ ] **Status Codes**: Accurate semantic status codes are used (e.g., `201` for creation, `204` for deletion, `200` for retrieval/update).
- [ ] **Error Handling**: Raised `HTTPException` with informative detail messages for missing or invalid resources.
- [ ] **Router Registration**: Router is included in `app/main.py` via `app.include_router()`.
- [ ] **Test Coverage**: Added tests in `tests/test_<resource>.py` covering status 200/201, 404, and 422 validation errors using `fastapi.testclient.TestClient`.
- [ ] **Test Suite Passing**: Ran `pytest` and verified all tests pass without errors.
