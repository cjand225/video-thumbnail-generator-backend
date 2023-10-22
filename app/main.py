"""
main.py

This is the main entry point for the FastAPI application. It initializes the app instance and includes necessary routers.
"""
from app.factory import create_app

# Create a new FastAPI app instance using the factory function.
app = create_app()
