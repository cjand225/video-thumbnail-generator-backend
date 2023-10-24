import os
from app.storage.local_storage import LocalStorage
from app.storage.storage_service import StorageService

def get_storage_service() -> StorageService:
    """
    Get the appropriate storage service based on the environment configuration.

    Returns:
        StorageService: An instance of StorageService configured with the appropriate storage provider.
    """
    storage_type = os.getenv("STORAGE_TYPE", "local").lower()

    if storage_type == "local":
        return StorageService(LocalStorage())
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")
