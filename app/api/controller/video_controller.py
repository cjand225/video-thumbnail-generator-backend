"""
video_controller.py

This module defines the API endpoints related to video thumbnail generation and retrieval. 
It uses the VideoService to process thumbnails and provides endpoints to upload videos,
generate thumbnails, and retrieve thumbnails.

Imported Modules:
- APIRouter from fastapi: To create API routes.
- File, UploadFile from fastapi: To handle file uploads.
- HTTPException, status from fastapi: To handle HTTP errors and statuses.
- VideoService from app.api.service.video_service: To use video processing services.
- VideoUploadResponse, ThumbnailResponse, ThumbnailRequest from app.api.models: To define request and response models.
- seconds_to_timestamp from app.helpers.time: To convert seconds to timestamp format.

Available Routes:
- POST /upload: 
  - Description: Uploads a video file and returns a response with the video ID.
  - Parameters:
    - file (UploadFile): The video file to be uploaded.
  - Responses:
    - 200: Video uploaded successfully, returns VideoUploadResponse.
    - 500: Video upload failed.

- POST /generate-thumbnail:
  - Description: Generates a thumbnail for a given video at a specific timestamp and resolution.
  - Request Body (JSON): 
    - file_id (str): ID of the video file.
    - timestamp (int): Timestamp in seconds to generate the thumbnail.
    - resolution (Optional[str], default="320x240"): Resolution of the thumbnail.
  - Responses:
    - 200: Thumbnail generated successfully, returns ThumbnailResponse.
    - 404: Video file not found.
    - 500: Internal server error.

- GET /get-thumbnail/{thumbnail_id}:
  - Description: Retrieves a thumbnail image by its ID.
  - Path Parameters:
    - thumbnail_id (str): ID of the thumbnail.
  - Responses:
    - 200: Thumbnail retrieved successfully, returns the thumbnail image.
    - 404: Thumbnail file not found.
    - 500: Internal server error.
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from app.api.service.video_service import VideoService
from app.api.models import VideoUploadResponse, ThumbnailResponse, ThumbnailRequest
from app.helpers.time import seconds_to_timestamp

router = APIRouter()

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """Handles video file uploads."""
    try:
        result = await VideoService.upload_video(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Video upload failed")

@router.post("/generate-thumbnail", response_model=ThumbnailResponse)
async def generate_thumbnail(request: ThumbnailRequest):
    """Generates a thumbnail for a video."""
    try:
        thumbnail_response = await VideoService.generate_thumbnail(request.file_id, seconds_to_timestamp(request.timestamp), request.resolution)
        return thumbnail_response
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get-thumbnail/{thumbnail_id}")
async def get_thumbnail(thumbnail_id: str):
    """Retrieves a thumbnail image."""
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
