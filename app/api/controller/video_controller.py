"""
video_controller.py

This module defines the API endpoints related to exchange rates. It uses the VideoService
to process thumbnails and provides an endpoints to upload, create, get, delete a thumbnail based on given parameters.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from app.api.service.video_service import VideoService
from app.api.models import VideoUploadResponse, ThumbnailResponse, ThumbnailRequest
from app.helpers.time import seconds_to_timestamp

router = APIRouter()

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    try:
        result = await VideoService.upload_video(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Video upload failed")


@router.post("/generate-thumbnail", response_model=ThumbnailResponse)
async def generate_thumbnail(request: ThumbnailRequest):
    try:
        thumbnail_response = await VideoService.generate_thumbnail(request.file_id, seconds_to_timestamp(request.timestamp), request.resolution)
        return thumbnail_response
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/get-thumbnail/{thumbnail_id}")
async def generate_thumbnail(thumbnail_id : str):
    try:
        get_thumbnail_response = await VideoService.get_thumbnail(thumbnail_id)
        return get_thumbnail_response
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail file not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
