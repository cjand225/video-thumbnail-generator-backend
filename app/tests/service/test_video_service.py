import os
import shutil
import pytest
from fastapi import UploadFile
from app.api.service.video_service import VideoService
from app.api.models import VideoUploadResponse

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
    if os.path.exists(VideoService.UPLOAD_DIR):
        shutil.rmtree(VideoService.UPLOAD_DIR)

@pytest.mark.asyncio
async def test_upload_video(upload_file):
    response = await VideoService.upload_video(upload_file)
    assert isinstance(response, VideoUploadResponse)
    assert response.filename == "test_video.mp4"
    assert os.path.exists(os.path.join(VideoService.UPLOAD_DIR, response.file_id + os.path.splitext(upload_file.filename)[1]))


@pytest.fixture
def video_file():
    try:
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

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        pass
        # Cleanup
        try:
            os.remove(os.path.join(video_path, f"{video_id}.mp4"))
        except FileNotFoundError:
            pass


@pytest.mark.asyncio
async def test_generate_thumbnail(video_file):
    video_id, video_path = video_file

    try:
        # Generate thumbnail
        timestamp = "00:00:01"
        resolution = "320x240"
        response = await VideoService.generate_thumbnail(video_id, timestamp, resolution)
        thumbnail_id = response.thumbnail_id
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

        # Make uploads directory
        os.makedirs(thumbnail_path, exist_ok=True)

        # Copy test video to uploads
        source = os.path.join(resource_path, "test_thumbnail.jpg")
        destination = os.path.join(thumbnail_path, f"{thumbnail_id}.jpg")
        shutil.copy(source, destination)

        yield thumbnail_id

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        pass
        # Cleanup
        try:
            os.remove(os.path.join(thumbnail_path, f"{thumbnail_id}.jpg"))
        except FileNotFoundError:
            pass

@pytest.mark.asyncio
async def test_get_thumbnail(thumbnail_file):
    thumbnail_id = thumbnail_file
    response = await VideoService.get_thumbnail(thumbnail_id)
    assert response.filename == f"{thumbnail_id}.jpg"
    assert response.media_type == "image/jpeg"
