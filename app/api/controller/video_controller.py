"""
video_controller.py

This module defines the API endpoints related to exchange rates. It uses the VideoService
to process thumbnails and provides an endpoints to upload, create, get, delete a thumbnail based on given parameters.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Path
from app.api.service.video_service import VideoService
from app.api.models import VideoUploadResponse, ThumbnailResponse
from app.helpers.time import seconds_to_timestamp
from typing import Optional

router = APIRouter()

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    try:
        result = await VideoService.upload_video(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Video upload failed")


@router.get("/generate-thumbnail/{file_id}", response_model=ThumbnailResponse)
async def generate_thumbnail(file_id: str, timestamp: int, resolution: Optional[str] = "320x240"):
    try:
        thumbnail_response = await VideoService.generate_thumbnail(file_id, seconds_to_timestamp(timestamp), resolution)
        return thumbnail_response
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
