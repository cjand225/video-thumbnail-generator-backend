import os
from app.storage.local_storage import LocalStorage
from app.storage.aws_storage import AWSStorage
from app.storage.storage_service import StorageService

def get_storage_service() -> StorageService:
    """
    Get the appropriate storage service based on the environment configuration.

    Returns:
        StorageService: An instance of StorageService configured with the appropriate storage provider.
    """
    storage_type = os.getenv("STORAGE_TYPE", "aws").lower()

    if storage_type == "local":
        return StorageService(LocalStorage())
    if storage_type == "aws":
        return StorageService(AWSStorage())
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")
