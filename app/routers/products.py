"""API router for product endpoints.

Exposes endpoints to list all products and retrieve an individual product by ID.
"""

from fastapi import APIRouter, HTTPException, status
from app.data import get_all_products, get_product_by_id, update_product_description
from app.models import Product, ProductDescriptionUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    "",
    response_model=list[Product],
    summary="List all products",
    description="Retrieve the complete list of products currently available in the catalog.",
)
def list_products() -> list[Product]:
    """Return all products in the store.

    Example:
        >>> from app.routers.products import list_products
        >>> products = list_products()
        >>> isinstance(products, list)
        True
        >>> len(products) > 0
        True
    """
    return get_all_products()


@router.get(
    "/{product_id}",
    response_model=Product,
    summary="Get a product by ID",
    description="Retrieve details of a specific product using its integer identifier.",
    responses={
        404: {"description": "Product not found"},
    },
)
def get_product(product_id: int) -> Product:
    """Return a single product by its unique identifier.

    Raises:
        HTTPException: 404 if no product exists with the given ID.

    Example:
        >>> from app.routers.products import get_product
        >>> product = get_product(1)
        >>> product.id
        1
    """
    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return product


@router.patch(
    "/{product_id}/description",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    summary="Update product description",
    description="Update the description field for an existing product in the catalog.",
    responses={
        404: {"description": "Product not found"},
    },
)
def update_description(
    product_id: int,
    payload: ProductDescriptionUpdate,
) -> Product:
    """Update the description of a product by ID.

    Raises:
        HTTPException: 404 if no product exists with the given ID.

    Example:
        >>> from app.routers.products import update_description
        >>> from app.models import ProductDescriptionUpdate
        >>> update = ProductDescriptionUpdate(description="Fresh ergonomic features")
        >>> product = update_description(1, update)
        >>> product.description
        'Fresh ergonomic features'
    """
    updated_product = update_product_description(product_id, payload.description)
    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return updated_product
