"""
middlewares.py

This module provides functions to manage and add middleware to the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_config


def add_middleware(app: FastAPI) -> None:
    """
    Add middleware to the provided FastAPI application instance.

    Args:
        app (FastAPI): The FastAPI application instance to which the middleware will be added.

    Returns:
        None
    """
    config = get_config()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=3600
    )
