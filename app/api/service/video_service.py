from fastapi import UploadFile
from fastapi.responses import FileResponse
from app.api.models import VideoUploadResponse, ThumbnailResponse

import os
import uuid
import aiofiles
import subprocess
import asyncio


class VideoService:
    
    UPLOAD_DIR = "uploads"

    THUMBNAIL_DIR = "thumbnails"

    @staticmethod
    async def upload_video(file: UploadFile) -> VideoUploadResponse:
        file_id = str(uuid.uuid4())

        # Extract file extension
        file_extension = os.path.splitext(file.filename)[1]
        
        # Ensure the upload directory exists
        os.makedirs(VideoService.UPLOAD_DIR, exist_ok=True)

        file_location = os.path.join(VideoService.UPLOAD_DIR, f"{file_id}{file_extension}")
        
        # Save the uploaded file
        async with aiofiles.open(file_location, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)
        
        return VideoUploadResponse(filename=file.filename, file_id=file_id)

    @staticmethod
    async def generate_thumbnail(file_id : str, timestamp: str = "00:00:01", resolution: str = "320x240") -> ThumbnailResponse:
        # Search for video, assume supported formats.
        for extension in ['mp4', 'mkv', 'avi', 'mov']:
            video_path = os.path.join(".", VideoService.UPLOAD_DIR, f"{file_id}.{extension}")

            if os.path.isfile(video_path):
                break

        if not os.path.isfile(video_path):
            raise FileNotFoundError("Video file not found")

        # Generate a unique ID for the thumbnail
        thumbnail_id = str(uuid.uuid4())
        thumbnail_path = os.path.join(VideoService.THUMBNAIL_DIR, thumbnail_id + '.jpg')

        # Ensure the upload directory exists
        os.makedirs(VideoService.THUMBNAIL_DIR, exist_ok=True)

        # Prepare ffmpeg command
        ffmpeg_cmd = [
            "ffmpeg",
            "-ss", timestamp,
            "-i", video_path,
            "-vframes", "1",
            "-s", resolution,
            thumbnail_path
        ]

        # Run ffmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        # Wait for the process to complete
        stdout, stderr = await process.communicate()
    
        # Check if process was successful
        if process.returncode != 0:
            print("FFmpeg failed:", stderr.decode())
            raise Exception("FFmpeg failed")
    
        return ThumbnailResponse(thumbnail_id=thumbnail_id)

    @staticmethod
    async def get_thumbnail(thumbnail_id : str) -> FileResponse:
        file_name = f"{thumbnail_id}.jpg"
        thumbnail_path = os.path.join(VideoService.THUMBNAIL_DIR, file_name)

        if not os.path.isfile(thumbnail_path):
            raise FileNotFoundError("Thumbnail file not found")

        return FileResponse(path=thumbnail_path, filename=file_name, media_type='image/jpeg')
