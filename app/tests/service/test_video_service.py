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
