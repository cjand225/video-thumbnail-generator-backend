import pytest
import asyncio
import os

from app.storage.local_storage import LocalStorage


@pytest.mark.asyncio
async def test_write_file(tmp_path):
    # Given
    file_content = b"Hello, World!"
    file_location = os.path.join(tmp_path, "test_file.txt")

    # When
    await LocalStorage.write_file(file_location, file_content)

    # Then
    assert os.path.exists(file_location)
    with open(file_location, "rb") as f:
        saved_content = f.read()
    assert saved_content == file_content
    assert await LocalStorage.file_exists(file_location)

@pytest.mark.asyncio
async def test_read_file(tmp_path):
    # Given
    file_content = b"Hello, World!"
    file_location = os.path.join(tmp_path, "test_file.txt")
    with open(file_location, "wb") as f:
        f.write(file_content)

    # When
    read_content = await LocalStorage.read_file(file_location)

    # Then
    assert read_content == file_content
    assert await LocalStorage.file_exists(file_location)

@pytest.mark.asyncio
async def test_file_exists(tmp_path):
    # Given
    existing_file = os.path.join(tmp_path, "existing_file.txt")
    non_existing_file = os.path.join(tmp_path, "non_existing_file.txt")
    with open(existing_file, "wb") as f:
        f.write(b"Hello, World!")

    # When / Then
    assert await LocalStorage.file_exists(existing_file)
    assert not await LocalStorage.file_exists(non_existing_file)
