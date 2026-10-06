"""Data models for e-commerce products and orders.

Every model and helper method in this module provides type hints, descriptions,
and usage examples.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Lifecycle status of a customer order."""

    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Product(BaseModel):
    """Represents a product item in the e-commerce catalog.

    Example:
        >>> product = Product(
        ...     id=1,
        ...     name="Mechanical Keyboard",
        ...     description="RGB backlit mechanical gaming keyboard",
        ...     price=89.99,
        ...     category="Electronics",
        ...     inventory=25,
        ... )
        >>> product.name
        'Mechanical Keyboard'
    """

    id: int = Field(..., description="Unique product identifier", ge=1)
    name: str = Field(..., description="Name of the product", min_length=1)
    description: str = Field(..., description="Detailed product description")
    price: float = Field(..., description="Product price in USD", ge=0.0)
    category: str = Field(..., description="Category the product belongs to")
    inventory: int = Field(..., description="Units available in stock", ge=0)


class OrderItem(BaseModel):
    """Line item within an order containing product reference and quantity.

    Example:
        >>> item = OrderItem(product_id=1, product_name="Mechanical Keyboard", quantity=2, unit_price=89.99)
        >>> item.total_price()
        179.98
    """

    product_id: int = Field(..., description="Identifier of the purchased product", ge=1)
    product_name: str = Field(..., description="Name of the product at purchase time")
    quantity: int = Field(..., description="Number of units ordered", ge=1)
    unit_price: float = Field(..., description="Price per unit at purchase time", ge=0.0)

    def total_price(self) -> float:
        """Calculate the total price for this line item.

        Example:
            >>> item = OrderItem(product_id=1, product_name="Wireless Mouse", quantity=3, unit_price=20.0)
            >>> item.total_price()
            60.0
        """
        return round(self.quantity * self.unit_price, 2)


class Order(BaseModel):
    """Represents a customer order placed in the store.

    Example:
        >>> order = Order(
        ...     id=1,
        ...     customer_name="Alice Johnson",
        ...     customer_email="alice@example.com",
        ...     items=[
        ...         OrderItem(product_id=1, product_name="Mechanical Keyboard", quantity=1, unit_price=89.99)
        ...     ],
        ...     total_amount=89.99,
        ...     status=OrderStatus.PENDING,
        ...     created_at=datetime(2026, 1, 15, 10, 30),
        ... )
        >>> order.id
        1
    """

    id: int = Field(..., description="Unique order identifier", ge=1)
    customer_name: str = Field(..., description="Customer's full name", min_length=1)
    customer_email: str = Field(..., description="Customer's email address")
    items: list[OrderItem] = Field(..., description="List of items included in the order")
    total_amount: float = Field(..., description="Total price of the order in USD", ge=0.0)
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Current fulfillment status")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when order was placed")
