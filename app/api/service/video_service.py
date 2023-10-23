from fastapi import UploadFile
from fastapi.responses import FileResponse
from app.api.models import VideoUploadResponse, ThumbnailResponse

import os
import uuid
import aiofiles
import subprocess
import asyncio

class VideoService:
    """
    A service class that handles video-related operations including uploading videos,
    generating thumbnails, and retrieving thumbnails.
    """
    
    UPLOAD_DIR = "uploads"
    """str: Directory to store uploaded video files."""

    THUMBNAIL_DIR = "thumbnails"
    """str: Directory to store generated thumbnail images."""

    @staticmethod
    async def upload_video(file: UploadFile) -> VideoUploadResponse:
        """
        Handles the uploading of a video file.

        Args:
            file (UploadFile): The video file to be uploaded.

        Returns:
            VideoUploadResponse: An object containing the filename and unique identifier of the uploaded video.
        
        Raises:
            Exception: If the file could not be saved.
        """
        # Generate a unique identifier for the uploaded file
        file_id = str(uuid.uuid4())

        # Extract file extension from the original file name
        file_extension = os.path.splitext(file.filename)[1]
        
        # Ensure the upload directory exists, create if not
        os.makedirs(VideoService.UPLOAD_DIR, exist_ok=True)

        # Construct the full file path to save the uploaded file
        file_location = os.path.join(VideoService.UPLOAD_DIR, f"{file_id}{file_extension}")
        
        # Save the uploaded file asynchronously
        async with aiofiles.open(file_location, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)
        
        # Return response containing the original file name and the unique file identifier
        return VideoUploadResponse(filename=file.filename, file_id=file_id)

    @staticmethod
    async def generate_thumbnail(file_id: str, timestamp: str = "00:00:01", resolution: str = "320x240") -> ThumbnailResponse:
        """
        Generates a thumbnail image for a given video file.

        Args:
            file_id (str): Unique identifier of the video file.
            timestamp (str, optional): Timestamp to capture the thumbnail. Defaults to "00:00:01".
            resolution (str, optional): Resolution of the generated thumbnail. Defaults to "320x240".

        Returns:
            ThumbnailResponse: An object containing the thumbnail identifier.

        Raises:
            FileNotFoundError: If the video file is not found.
            Exception: If FFmpeg fails to generate the thumbnail.
        """
        # Search for the video file in the supported formats
        for extension in ['mp4', 'mkv', 'avi', 'mov']:
            video_path = os.path.join(".", VideoService.UPLOAD_DIR, f"{file_id}.{extension}")
            if os.path.isfile(video_path):
                break
        else:
            raise FileNotFoundError("Video file not found")

        # Generate a unique identifier for the thumbnail
        thumbnail_id = str(uuid.uuid4())
        thumbnail_path = os.path.join(VideoService.THUMBNAIL_DIR, thumbnail_id + '.jpg')

        # Ensure the thumbnail directory exists, create if not
        os.makedirs(VideoService.THUMBNAIL_DIR, exist_ok=True)

        # Prepare FFmpeg command to generate thumbnail
        ffmpeg_cmd = [
            "ffmpeg",
            "-ss", timestamp,
            "-i", video_path,
            "-vframes", "1",
            "-s", resolution,
            thumbnail_path
        ]

        # Run FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()
    
        # Check if FFmpeg command was successful
        if process.returncode != 0:
            print("FFmpeg failed:", stderr.decode())
            raise Exception("FFmpeg failed")
    
        # Return response containing the thumbnail identifier
        return ThumbnailResponse(thumbnail_id=thumbnail_id)

    @staticmethod
    async def get_thumbnail(thumbnail_id: str) -> FileResponse:
        """
        Retrieves a thumbnail image by its identifier.

        Args:
            thumbnail_id (str): The unique identifier of the thumbnail.

        Returns:
            FileResponse: A response object to send the thumbnail file to the client.

        Raises:
            FileNotFoundError: If the thumbnail file is not found.
        """
        # Construct the full file path of the thumbnail image
        file_name = f"{thumbnail_id}.jpg"
        thumbnail_path = os.path.join(VideoService.THUMBNAIL_DIR, file_name)

        # Check if the thumbnail file exists
        if not os.path.isfile(thumbnail_path):
            raise FileNotFoundError("Thumbnail file not found")

        # Return response to send the thumbnail file to the client
        return FileResponse(path=thumbnail_path, filename=file_name, media_type='image/jpeg')
