import os
import aiofiles.os
import shutil
import pytest
from fastapi import UploadFile
from app.api.service.video_service import VideoService
from app.api.models import VideoUploadResponse
from app.storage.storage_provider import StorageProvider

# Create a fixture for the UploadFile
@pytest.fixture
async def upload_file(tmp_path):
    file_content = b"Test content"
    file_path = tmp_path / "test_video.mp4"
    file_path.write_bytes(file_content)

    upload_file = UploadFile(filename="test_video.mp4", file=file_path.open("rb"))
    yield upload_file
    upload_file.file.close()

    # Clean up the uploaded files folder after the test
    storage_service: StorageProvider = VideoService.storage_service
    if await storage_service.file_exists(str(VideoService.UPLOAD_DIR)):
        await storage_service.delete_directory(str(VideoService.UPLOAD_DIR))

@pytest.mark.asyncio
async def test_upload_video(upload_file):
    response = await VideoService.upload_video(upload_file)
    assert isinstance(response, VideoUploadResponse)
    assert response.filename == "test_video.mp4"
    
    storage_service: StorageProvider = VideoService.storage_service
    expected_file_path = os.path.join(str(VideoService.UPLOAD_DIR), response.file_id + os.path.splitext(upload_file.filename)[1])
    assert await storage_service.file_exists(expected_file_path)

    await storage_service.delete_file(expected_file_path)

@pytest.fixture
async def video_file():
    video_id = "9abe8652-f7d5-4f9e-8447-6a822a6355bc"
    video_path = os.path.join(".", VideoService.UPLOAD_DIR)
    resource_path = os.path.abspath(os.path.join("app", "tests", "resources"))

    # Make uploads directory
    os.makedirs(video_path, exist_ok=True)

    # Copy test video to uploads
    source = os.path.join(resource_path, "test_video.mp4")
    destination = os.path.join(video_path, f"{video_id}.mp4")
    shutil.copy(source, destination)

    yield video_id, video_path

    # Cleanup
    try:
        await aiofiles.os.remove(destination)
    except FileNotFoundError:
        pass

@pytest.mark.asyncio
async def test_generate_thumbnail(video_file):
    video_id, video_path = video_file

    try:
        # Generate thumbnail
        timestamp = "00:00:01"
        resolution = "320x240"
        thumbnail_id = await VideoService.generate_thumbnail(video_id, timestamp, resolution)
        thumbnail_path = os.path.join(".", VideoService.THUMBNAIL_DIR, thumbnail_id + '.jpg')

        # Check if thumbnail is generated
        assert os.path.isfile(thumbnail_path)
    finally:
        # Cleanup
        if os.path.isdir(video_path):
            shutil.rmtree(video_path)
        if os.path.isdir(VideoService.THUMBNAIL_DIR):
            shutil.rmtree(VideoService.THUMBNAIL_DIR)

@pytest.fixture
async def thumbnail_file():
    try:
        thumbnail_id = "84838f56-d9d7-4f54-881b-6021e34ae0e2"
        thumbnail_path = os.path.join(".", VideoService.THUMBNAIL_DIR)
        resource_path = os.path.abspath(os.path.join("app", "tests", "resources"))

        # Make thumbnails directory
        os.makedirs(thumbnail_path, exist_ok=True)

        # Copy test thumbnail to thumbnails directory
        source = os.path.join(resource_path, "test_thumbnail.jpg")
        destination = os.path.join(thumbnail_path, f"{thumbnail_id}.jpg")
        shutil.copy(source, destination)

        yield thumbnail_id

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if os.path.isdir(VideoService.THUMBNAIL_DIR):
            shutil.rmtree(VideoService.THUMBNAIL_DIR)

@pytest.mark.asyncio
async def test_get_thumbnail(thumbnail_file):
    thumbnail_id = thumbnail_file
    file_content, file_name = await VideoService.get_thumbnail(thumbnail_id)
    assert file_name == f"{thumbnail_id}.jpg", "File name should match the expected value"
    assert file_content, "File content should not be empty"
