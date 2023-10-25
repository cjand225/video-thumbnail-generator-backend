# test_video_controller.py

import os
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
from unittest.mock import patch
from io import BytesIO
import pytest
from app.api.service.video_service import VideoService
import shutil

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
def video_file():
    video_id = "9abe8652-f7d5-4f9e-8447-6a822a6355bc"
    video_path = os.path.abspath(os.path.join(".", VideoService.UPLOAD_DIR))
    os.makedirs(video_path, exist_ok=True)

    resource_path = os.path.abspath(os.path.join(".", "app", "tests", "resources", "test_video.mp4"))

    # Ensure the resource file exists
    assert os.path.isfile(resource_path), "The source video file does not exist."
    
    video_file_path = os.path.join(video_path, f"{video_id}.mp4")
    shutil.copy(resource_path, video_file_path)

    # Ensure the video file was copied successfully
    assert os.path.isfile(video_file_path), "The video file was not created successfully."
    
    print(f"Video file created at: {video_file_path}")

    return video_id

def test_generate_thumbnail(video_file):

    data = {
        "file_id" : video_file,
        "timestamp": 1,
        "resolution": "320x240"
    }
    response = client.post(f"/video/v1/generate-thumbnail", json=data)

    assert response.status_code == 200
    thumbnail_id = response.json().get("thumbnail_id")
    assert thumbnail_id is not None
    assert os.path.isfile(os.path.join(VideoService.THUMBNAIL_DIR, f"{thumbnail_id}.jpg"))


@pytest.fixture
def thumbnail_file():
    thumbnail_id = "84838f56-d9d7-4f54-881b-6021e34ae0e2"
    thumbnail_path = os.path.abspath(os.path.join(".", VideoService.THUMBNAIL_DIR))
    os.makedirs(thumbnail_path, exist_ok=True)

    resource_path = os.path.abspath(os.path.join(".", "app", "tests", "resources", "test_thumbnail.jpg"))

    # Ensure the resource file exists
    assert os.path.isfile(resource_path), "The source file does not exist."
    
    thumbnail_file_path = os.path.join(thumbnail_path, f"{thumbnail_id}.jpg")
    shutil.copy(resource_path, thumbnail_file_path)

    # Ensure the thumbnail file was copied successfully
    assert os.path.isfile(thumbnail_file_path), "The thumbnail file was not created successfully."
    
    print(f"Thumbnail file created at: {thumbnail_file_path}")

    yield thumbnail_id, thumbnail_path
    
    shutil.rmtree(thumbnail_path)

def test_get_thumbnail_success(thumbnail_file):
    thumbnail_id, thumbnail_path = thumbnail_file
    thumbnail_file_path = os.path.join(thumbnail_path, f"{thumbnail_id}.jpg")

    with open(thumbnail_file_path, 'rb') as f:
        thumbnail_content = f.read()

    response = client.get(f"/video/v1/get-thumbnail/{thumbnail_id}")

    assert response.status_code == 200
    assert response.content == thumbnail_content
    assert response.headers["content-type"] == "image/jpeg"
    assert "Content-Disposition" in response.headers

def test_get_thumbnail_not_found():
    nonexistent_thumbnail_id = "nonexistent"

    response = client.get(f"/video/v1/get-thumbnail/{nonexistent_thumbnail_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Thumbnail file not found"}
