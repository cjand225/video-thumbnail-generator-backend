"""
video_controller.py

This module defines API endpoints for video-related operations including video thumbnail generation and retrieval.
The functionalities are implemented using the VideoService, and the module provides endpoints for uploading videos,
generating thumbnails, and retrieving thumbnails.

Dependencies:
- fastapi: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- app.api.service.video_service: A module providing video processing services.
- app.api.models: A module defining request and response models for the API.
- app.helpers.time: A helper module for time-related functionalities.

Available Routes:
- POST /upload: Upload a video file and return a response with the video's filename and unique identifier.
- POST /generate-thumbnail: Generate a thumbnail for a given video at a specific timestamp and resolution, returning the thumbnail's unique identifier.
- GET /get-thumbnail/{thumbnail_id}: Retrieve a thumbnail image by its unique identifier.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from app.api.service.video_service import VideoService
from app.api.models import VideoUploadResponse, ThumbnailResponse, ThumbnailRequest
from app.helpers.time import seconds_to_timestamp

router = APIRouter()

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    Handle video file uploads.

    Args:
        file (UploadFile): The video file to be uploaded, wrapped in FastAPI's File class for form data.

    Returns:
        VideoUploadResponse: An object containing the uploaded video's filename and unique identifier.

    Raises:
        HTTPException: An HTTP 500 error indicating the video upload failed.
    """
    try:
        file_data = await file.read()
        file_name, file_id = await VideoService.upload_video(file_name=file.filename, file_data=file_data)
        return VideoUploadResponse(filename=file_name, file_id=file_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Video upload failed")

@router.post("/generate-thumbnail", response_model=ThumbnailResponse)
async def generate_thumbnail(request: ThumbnailRequest):
    """
    Generate a thumbnail for a video.

    Args:
        request (ThumbnailRequest): A request object containing the video file's ID, the timestamp for the thumbnail,
                                    and optionally the resolution of the thumbnail.

    Returns:
        ThumbnailResponse: An object containing the unique identifier of the generated thumbnail.

    Raises:
        HTTPException: An HTTP 404 error if the video file is not found.
        HTTPException: An HTTP 500 error for any other server-side error.
    """
    try:
        thumbnail_id = await VideoService.generate_thumbnail(request.file_id, seconds_to_timestamp(request.timestamp), request.resolution)
        return ThumbnailResponse(thumbnail_id=thumbnail_id)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get-thumbnail/{thumbnail_id}")
async def get_thumbnail(thumbnail_id: str):
    """
    Retrieve a thumbnail image.

    Args:
        thumbnail_id (str): The unique identifier of the thumbnail to retrieve.

    Returns:
        StreamingResponse: A streaming response containing the thumbnail image.

    Raises:
        HTTPException: An HTTP 404 error if the thumbnail file is not found.
        HTTPException: An HTTP 500 error for any other server-side error.
    """
    try:
        file_content, file_name = await VideoService.get_thumbnail(thumbnail_id)

        headers = {
            "Content-Disposition": f"attachment; filename={file_name}",
            "Content-Type": "image/jpeg",
        }

        return StreamingResponse(iter([file_content]), headers=headers)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail file not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
