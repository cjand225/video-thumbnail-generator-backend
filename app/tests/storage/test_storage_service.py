import pytest
from app.storage.local_storage import LocalStorage
from app.storage.storage_service import StorageService

@pytest.fixture
async def storage_service():
    """
    A pytest fixture to provide an instance of StorageService.

    Returns:
        StorageService: An instance of StorageService configured to use LocalStorage as the storage provider.
    """
    local_storage_provider = LocalStorage()
    return StorageService(local_storage_provider)

@pytest.mark.asyncio
async def test_write_file(storage_service, tmp_path):
    """
    Test to ensure that a file is written correctly using the StorageService with LocalStorage.
    
    Args:
        storage_service (StorageService): An instance of StorageService for file operations.
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    file_path = tmp_path / "test_file.txt"
    content = b"Hello, World!"

    # Act
    result = await storage_service.write_file(file_path, content)

    # Assert
    assert result is True, "Writing file should be successful"
    assert file_path.read_bytes() == content, "Content of the file should match the written content"
    assert await storage_service.file_exists(file_path), "File should exist after writing"

@pytest.mark.asyncio
async def test_read_file(storage_service, tmp_path):
    """
    Test to ensure that a file is read correctly using the StorageService with LocalStorage.
    
    Args:
        storage_service (StorageService): An instance of StorageService for file operations.
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    file_path = tmp_path / "test_file.txt"
    content = b"Hello, World!"
    file_path.write_bytes(content)

    # Act
    read_content = await storage_service.read_file(file_path)

    # Assert
    assert read_content == content, "Read content should match the original content"

@pytest.mark.asyncio
async def test_delete_file(storage_service, tmp_path):
    """
    Test to ensure that a file is deleted correctly using the StorageService with LocalStorage.
    
    Args:
        storage_service (StorageService): An instance of StorageService for file operations.
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    file_path = tmp_path / "test_file.txt"
    content = b"Hello, World!"
    file_path.write_bytes(content)
    assert file_path.exists(), "File should exist before deletion"

    # Act
    result = await storage_service.delete_file(file_path)

    # Assert
    assert result is True, "File deletion should be successful"
    assert not file_path.exists(), "File should not exist after deletion"

@pytest.mark.asyncio
async def test_file_exists(storage_service, tmp_path):
    """
    Test to check file existence using the StorageService with LocalStorage.
    
    Args:
        storage_service (StorageService): An instance of StorageService for file operations.
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    existing_file = tmp_path / "existing_file.txt"
    non_existing_file = tmp_path / "non_existing_file.txt"
    existing_file.write_bytes(b"Hello, World!")

    # Act / Assert
    assert await storage_service.file_exists(existing_file), "Should return True for existing file"
    assert not await storage_service.file_exists(non_existing_file), "Should return False for non-existing file"
