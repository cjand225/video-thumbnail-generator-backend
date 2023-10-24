import pytest
import aiofiles
import aiofiles.os
import os

from app.storage.local_storage import LocalStorage

@pytest.mark.asyncio
async def test_write_file(tmp_path):
    """
    Test the write_file method to ensure it writes content to a file correctly.

    This test checks if the file is created at the specified location with the correct content. It also verifies
    that the file_exists method correctly identifies that the file now exists.

    Args:
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    file_content = b"Hello, World!"
    file_location = os.path.join(tmp_path, "test_file.txt")

    # Act
    result = await LocalStorage.write_file(file_location, file_content)

    # Assert
    assert result is True
    assert await aiofiles.os.path.exists(file_location)
    async with aiofiles.open(file_location, "rb") as f:
        saved_content = await f.read()
    assert saved_content == file_content
    assert await LocalStorage.file_exists(file_location)

@pytest.mark.asyncio
async def test_read_file(tmp_path):
    """
    Test the read_file method to ensure it reads and returns the file content correctly.

    This test checks if the method can read the content of a pre-existing file and return the correct bytes. It also
    verifies that the file_exists method correctly identifies that the file exists.

    Args:
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    file_content = b"Hello, World!"
    file_location = os.path.join(tmp_path, "test_file.txt")
    async with aiofiles.open(file_location, "wb") as f:
        await f.write(file_content)

    # Act
    read_content = await LocalStorage.read_file(file_location)

    # Assert
    assert read_content == file_content
    assert await LocalStorage.file_exists(file_location)

@pytest.mark.asyncio
async def test_delete_file(tmp_path):
    """
    Test the delete_file method to ensure it deletes a file correctly.

    This test checks if the file is successfully deleted from the specified location. It also verifies
    that the file_exists method correctly identifies that the file no longer exists.

    Args:
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    file_content = b"Hello, World!"
    file_location = os.path.join(tmp_path, "test_file.txt")
    async with aiofiles.open(file_location, "wb") as f:
        await f.write(file_content)
    assert await aiofiles.os.path.exists(file_location)

    # Act
    result = await LocalStorage.delete_file(file_location)

    # Assert
    assert result is True
    assert not await aiofiles.os.path.exists(file_location)
    assert not await LocalStorage.file_exists(file_location)

@pytest.mark.asyncio
async def test_file_exists(tmp_path):
    """
    Test the file_exists method to ensure it correctly identifies existing and non-existing files.

    This test creates a file and then checks that file_exists correctly returns True for it and False for a
    non-existing file.

    Args:
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    existing_file = os.path.join(tmp_path, "existing_file.txt")
    non_existing_file = os.path.join(tmp_path, "non_existing_file.txt")
    async with aiofiles.open(existing_file, "wb") as f:
        await f.write(b"Hello, World!")

    # Act / Assert
    assert await LocalStorage.file_exists(existing_file)
    assert not await LocalStorage.file_exists(non_existing_file)

@pytest.mark.asyncio
async def test_directory_exists(tmp_path):
    """
    Test the directory_exists method to ensure it correctly identifies existing and non-existing directories.

    This test creates a directory and then checks that directory_exists correctly returns True for it and False for a
    non-existing directory.

    Args:
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    existing_directory = os.path.join(tmp_path, "existing_directory")
    non_existing_directory = os.path.join(tmp_path, "non_existing_directory")
    os.mkdir(existing_directory)

    # Act / Assert
    assert await LocalStorage.directory_exists(existing_directory)
    assert not await LocalStorage.directory_exists(non_existing_directory)

@pytest.mark.asyncio
async def test_delete_directory(tmp_path):
    """
    Test the delete_directory method to ensure it deletes a directory correctly.

    This test checks if the directory is successfully deleted from the specified location. It also verifies
    that the directory_exists method correctly identifies that the directory no longer exists.

    Args:
        tmp_path (PosixPath): A pytest fixture that provides a temporary directory unique to the test invocation.
    """
    # Arrange
    directory_location = os.path.join(tmp_path, "test_directory")
    os.mkdir(directory_location)
    assert os.path.exists(directory_location)

    # Act
    result = await LocalStorage.delete_directory(directory_location)

    # Assert
    assert result is True
    assert not os.path.exists(directory_location)
    assert not await LocalStorage.directory_exists(directory_location)
