# test_video_controller.py

import os
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
from unittest.mock import patch
from io import BytesIO

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
