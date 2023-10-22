"""
factory.py

This module provides a factory function to create and configure an instance of the FastAPI application.
"""

from fastapi import FastAPI
from app.middleware import add_middleware
from app.api.controller.video_controller import router as video_router


def create_app() -> FastAPI:
    """
    Create a new instance of the FastAPI application.

    Returns:
        FastAPI: A new FastAPI application instance with added middleware.
    """

    app = FastAPI()

    # Add middlewares to the app
    add_middleware(app)

    # Include the video router
    app.include_router(video_router, prefix="/video/v1")

    return app
