import os
import pytest
from app.storage.local_storage import LocalStorage
from app.storage.storage_service import StorageService
from app.storage.storage_factory import get_storage_service

def test_get_storage_service_local():
    """
    Test if the get_storage_service function correctly returns a StorageService instance 
    configured with LocalStorage when the STORAGE_TYPE environment variable is set to "local".
    """
    # Arrange
    os.environ["STORAGE_TYPE"] = "local"
    
    # Act
    storage_service = get_storage_service()

    # Assert
    assert isinstance(storage_service, StorageService), "The returned object should be an instance of StorageService"
    assert isinstance(storage_service.storage_provider, LocalStorage), "The storage provider should be an instance of LocalStorage"

def test_get_storage_service_unsupported():
    """
    Test if the get_storage_service function raises a ValueError when an unsupported storage type is specified.
    """
    # Arrange
    os.environ["STORAGE_TYPE"] = "unsupported"

    # Act / Assert
    with pytest.raises(ValueError) as excinfo:
        get_storage_service()
    assert "Unsupported storage type: unsupported" in str(excinfo.value), "A ValueError with the correct error message should be raised"

def test_get_storage_service_default():
    """
    Test if the get_storage_service function defaults to returning a StorageService instance configured with LocalStorage when no STORAGE_TYPE is set.
    """
    # Arrange
    if "STORAGE_TYPE" in os.environ:
        del os.environ["STORAGE_TYPE"]
    
    # Act
    storage_service = get_storage_service()

    # Assert
    assert isinstance(storage_service, StorageService), "The returned object should be an instance of StorageService"
    assert isinstance(storage_service.storage_provider, LocalStorage), "The storage provider should be an instance of LocalStorage"
