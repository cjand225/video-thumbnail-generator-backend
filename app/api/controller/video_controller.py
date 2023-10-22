"""
video_controller.py

This module defines the API endpoints related to exchange rates. It uses the VideoService
to process thumbnails and provides an endpoints to upload, create, get, delete a thumbnail based on given parameters.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from app.api.service.video_service import VideoService
from app.api.models import VideoUploadResponse

router = APIRouter()

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    try:
        result = await VideoService.upload_video(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Video upload failed")

