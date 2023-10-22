# test_video_controller.py

import os
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
from unittest.mock import patch
from io import BytesIO
import pytest
from app.api.service.video_service import VideoService

# Set the environment variable for testing purposes.
os.environ["ENV"] = "development"

# Now, import the app after setting the environment variable.
from app.main import app

# Initialize a test client for the FastAPI application.
client = TestClient(app)

@patch('app.api.controller.video_controller.VideoService.upload_video')
def test_upload_video_success(mock_upload):
    """
    Test the /upload endpoint for a successful video upload.
    
    The service layer is mocked to return a successful response.
    The test then checks if the API endpoint returns the expected status code and JSON response.
    """
    content = b"file_content"
    mock_upload.return_value = {"filename": "test_video.mp4", "file_id": "1234567890"}
    response = client.post(
        "/video/v1/upload",
        files={"file": ("test_video.mp4", BytesIO(content), "video/mp4")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "filename": "test_video.mp4",
        "file_id": "1234567890"
    }

@patch('app.api.controller.video_controller.VideoService.upload_video')
def test_upload_video_failure(mock_upload):
    content = b"file_content"
    
    # Configure the mock to raise an exception when called
    mock_upload.side_effect = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Video upload failed")
    
    response = client.post(
        "/video/v1/upload",
        files={"file": ("test_video.mp4", BytesIO(content), "video/mp4")}
    )
    
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Video upload failed"}


@pytest.fixture
def video_file(tmp_path):
    video_id = "9abe8652-f7d5-4f9e-8447-6a822a6355bc"
    video_path = os.path.join(".",  VideoService.UPLOAD_DIR)
    os.makedirs(video_path, exist_ok=True)

    resource_path = os.path.join(".", "app", "tests","resources","test_video.mp4")
    
    with open(resource_path, "rb") as f:
        video_content = f.read()

    with open(os.path.join(video_path, f"{video_id}.mp4"), "wb") as f:
        f.write(video_content)
    
    return video_id

def test_generate_thumbnail(video_file):
    timestamp = 1
    resolution = "320x240"

    response = client.post(f"/video/v1/generate-thumbnail/{video_file}?timestamp={timestamp}&resolution={resolution}")

    assert response.status_code == 200
    thumbnail_id = response.json().get("thumbnail_id")
    assert thumbnail_id is not None
    assert os.path.isfile(os.path.join(VideoService.THUMBNAIL_DIR, f"{thumbnail_id}.jpg"))

