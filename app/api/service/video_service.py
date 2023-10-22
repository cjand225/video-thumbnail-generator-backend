import os
import uuid
from fastapi import UploadFile
from app.api.models import VideoUploadResponse
import aiofiles

class VideoService:
    
    UPLOAD_DIR = "uploads"

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
