"""API router for order endpoints.

Exposes endpoints to list all orders and retrieve an individual order by ID.
"""

from fastapi import APIRouter, HTTPException, status
from app.data import get_all_orders, get_order_by_id
from app.models import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get(
    "",
    response_model=list[Order],
    summary="List all orders",
    description="Retrieve the complete list of customer orders.",
)
def list_orders() -> list[Order]:
    """Return all orders in the store.

    Example:
        >>> from app.routers.orders import list_orders
        >>> orders = list_orders()
        >>> isinstance(orders, list)
        True
        >>> len(orders) > 0
        True
    """
    return get_all_orders()


@router.get(
    "/{order_id}",
    response_model=Order,
    summary="Get an order by ID",
    description="Retrieve full details for an order using its integer identifier.",
    responses={
        404: {"description": "Order not found"},
    },
)
def get_order(order_id: int) -> Order:
    """Return a single order by its unique identifier.

    Raises:
        HTTPException: 404 if no order exists with the given ID.

    Example:
        >>> from app.routers.orders import get_order
        >>> order = get_order(1)
        >>> order.id
        1
    """
    order = get_order_by_id(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found",
        )
    return order
