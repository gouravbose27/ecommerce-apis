"""In-memory data store for products and orders.

Provides helper lookup functions and seed data.
"""

from datetime import datetime, timezone
from app.models import Order, OrderItem, OrderStatus, Product

# Seed products
SAMPLE_PRODUCTS: list[Product] = [
    Product(
        id=1,
        name="Wireless Noise-Canceling Headphones",
        description="Over-ear Bluetooth headphones with active noise cancellation and 30-hour battery life.",
        price=199.99,
        category="Electronics",
        inventory=45,
    ),
    Product(
        id=2,
        name="Ergonomic Mechanical Keyboard",
        description="Hot-swappable tactile switches with customizable RGB backlighting and wrist rest.",
        price=129.50,
        category="Electronics",
        inventory=80,
    ),
    Product(
        id=3,
        name="Ultra-Wide Curved Monitor 34-inch",
        description="WQHD 3440x1440 resolution, 144Hz refresh rate, HDR400, USB-C connectivity.",
        price=499.00,
        category="Computers",
        inventory=15,
    ),
    Product(
        id=4,
        name="Stainless Steel Water Bottle",
        description="Double-wall vacuum insulated 32oz bottle keeping drinks cold for 24 hours.",
        price=24.95,
        category="Home & Kitchen",
        inventory=150,
    ),
    Product(
        id=5,
        name="Standing Desk Converter",
        description="Adjustable height desk riser with spacious dual-tier platform for dual monitors.",
        price=159.99,
        category="Office",
        inventory=25,
    ),
]

# Seed orders
SAMPLE_ORDERS: list[Order] = [
    Order(
        id=1,
        customer_name="Alice Johnson",
        customer_email="alice.johnson@example.com",
        items=[
            OrderItem(
                product_id=1,
                product_name="Wireless Noise-Canceling Headphones",
                quantity=1,
                unit_price=199.99,
            ),
            OrderItem(
                product_id=4,
                product_name="Stainless Steel Water Bottle",
                quantity=2,
                unit_price=24.95,
            ),
        ],
        total_amount=249.89,
        status=OrderStatus.DELIVERED,
        created_at=datetime(2026, 2, 10, 14, 25, 0, tzinfo=timezone.utc),
    ),
    Order(
        id=2,
        customer_name="Bob Smith",
        customer_email="bob.smith@example.com",
        items=[
            OrderItem(
                product_id=2,
                product_name="Ergonomic Mechanical Keyboard",
                quantity=1,
                unit_price=129.50,
            ),
        ],
        total_amount=129.50,
        status=OrderStatus.SHIPPED,
        created_at=datetime(2026, 3, 1, 9, 15, 0, tzinfo=timezone.utc),
    ),
    Order(
        id=3,
        customer_name="Carol White",
        customer_email="carol.white@example.com",
        items=[
            OrderItem(
                product_id=3,
                product_name="Ultra-Wide Curved Monitor 34-inch",
                quantity=1,
                unit_price=499.00,
            ),
            OrderItem(
                product_id=5,
                product_name="Standing Desk Converter",
                quantity=1,
                unit_price=159.99,
            ),
        ],
        total_amount=658.99,
        status=OrderStatus.PROCESSING,
        created_at=datetime(2026, 3, 15, 16, 40, 0, tzinfo=timezone.utc),
    ),
]


def get_all_products() -> list[Product]:
    """Retrieve all available products from the store.

    Example:
        >>> products = get_all_products()
        >>> len(products) >= 5
        True
        >>> products[0].id
        1
    """
    return SAMPLE_PRODUCTS


def get_product_by_id(product_id: int) -> Product | None:
    """Find a product by its unique integer identifier.

    Example:
        >>> prod = get_product_by_id(1)
        >>> prod is not None
        True
        >>> prod.name
        'Wireless Noise-Canceling Headphones'
        >>> get_product_by_id(9999) is None
        True
    """
    for product in SAMPLE_PRODUCTS:
        if product.id == product_id:
            return product
    return None


def get_all_orders() -> list[Order]:
    """Retrieve all orders recorded in the store.

    Example:
        >>> orders = get_all_orders()
        >>> len(orders) >= 3
        True
        >>> orders[0].id
        1
    """
    return SAMPLE_ORDERS


def get_order_by_id(order_id: int) -> Order | None:
    """Find an order by its unique integer identifier.

    Example:
        >>> order = get_order_by_id(1)
        >>> order is not None
        True
        >>> order.customer_name
        'Alice Johnson'
        >>> get_order_by_id(9999) is None
        True
    """
    for order in SAMPLE_ORDERS:
        if order.id == order_id:
            return order
    return None
