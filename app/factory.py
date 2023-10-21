"""
factory.py

This module provides a factory function to create and configure an instance of the FastAPI application.
"""

from fastapi import FastAPI
from app.middleware import add_middleware


def create_app() -> FastAPI:
    """
    Create a new instance of the FastAPI application.

    Returns:
        FastAPI: A new FastAPI application instance with added middleware.
    """

    app = FastAPI()

    # Add middlewares to the app
    add_middleware(app)

    return app
