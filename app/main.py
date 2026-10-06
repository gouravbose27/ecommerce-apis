"""FastAPI application entry point for E-commerce APIs.

Mounts routers for products and orders with metadata and documentation.
"""

from fastapi import FastAPI
from app.routers import orders, products


def create_app() -> FastAPI:
    """Create and configure an instance of the FastAPI application.

    Example:
        >>> test_app = create_app()
        >>> test_app.title
        'E-commerce API'
    """
    app = FastAPI(
        title="E-commerce API",
        description="RESTful API service for browsing products and retrieving customer orders.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(products.router)
    app.include_router(orders.router)

    @app.get("/", tags=["Health"])
    def root() -> dict[str, str]:
        """Return a basic health/welcome message.

        Example:
            >>> root()
            {'message': 'Welcome to the E-commerce API'}
        """
        return {"message": "Welcome to the E-commerce API"}

    return app


app = create_app()
