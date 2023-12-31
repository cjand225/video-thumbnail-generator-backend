from typing import Tuple
from app.storage.storage_service import StorageService
from app.storage.storage_factory import get_storage_service
from app.helpers.video import supported_video_formats

import os
import uuid
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

    storage_service: StorageService = get_storage_service()

    @staticmethod
    async def upload_video(file_name: str, file_data: bytes) -> dict:
        """
        Handles the uploading of a video file.

        Args:
            file (UploadFile): The video file to be uploaded.

        Returns:
            VideoUploadResponse: An object containing the filename and unique identifier of the uploaded video.
        """
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file_name)[1]
        file_location = os.path.join(VideoService.UPLOAD_DIR, f"{file_id}{file_extension}")

        success = await VideoService.storage_service.write_file(file_location, file_data)

        if not success:
            raise Exception("Failed to save video file")

        return file_name, file_id

    @staticmethod
    async def generate_thumbnail(file_id: str, timestamp: str = "00:00:01", resolution: str = "320x240") -> str:
        """
        Generates a thumbnail image for a given video file.

        Args:
            file_id (str): Unique identifier of the video file.
            timestamp (str, optional): Timestamp to capture the thumbnail. Defaults to "00:00:01".
            resolution (str, optional): Resolution of the generated thumbnail. Defaults to "320x240".

        Returns:
            str: The unique identifier of the generated thumbnail.

        Raises:
            FileNotFoundError: If the video file is not found.
            Exception: If FFmpeg fails to generate the thumbnail.
        """
        # Search for the video file in the supported formats
        video_bytes = None
        file_extension = None
        for extension in supported_video_formats():
            potential_path = os.path.join(VideoService.UPLOAD_DIR, f"{file_id}.{extension}")
            if await VideoService.storage_service.file_exists(potential_path):
                video_bytes = await VideoService.storage_service.read_file(potential_path)
                file_extension = extension
                break
        if video_bytes is None:
            raise FileNotFoundError("Video file not found")

        # Generate a unique identifier for the thumbnail
        thumbnail_id = str(uuid.uuid4())
        thumbnail_path = os.path.join(VideoService.THUMBNAIL_DIR, thumbnail_id + '.jpg')

        # Prepare FFmpeg command to generate thumbnail and output to stdout
        ffmpeg_cmd = [
            "ffmpeg",
            "-f", file_extension,
            "-i", "pipe:0",
            "-ss", timestamp,
            "-vframes", "1",
            "-s", resolution,
            "-f", "image2pipe",
            "-c:v", "mjpeg",
            "pipe:1"
        ]

        # Run FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate(input=video_bytes)

        # Check if FFmpeg command was successful
        if process.returncode != 0 or len(stdout) <= 0:
            print("FFmpeg failed:", stderr.decode())
            raise Exception("FFmpeg failed to generate thumbnail")

        # Save thumbnail to storage
        try:
            await VideoService.storage_service.write_file(thumbnail_path, stdout)
        except Exception as e:
            raise Exception(f"Failed to save thumbnail: {str(e)}")

        return thumbnail_id

    @staticmethod
    async def get_thumbnail(thumbnail_id: str) -> Tuple[bytes, str]:
        """
        Retrieves a thumbnail image by its identifier.

        Args:
            thumbnail_id (str): The unique identifier of the thumbnail.

        Returns:
            Tuple[bytes, str]: A tuple containing the file content as bytes and the file name.

        Raises:
            FileNotFoundError: If the thumbnail file is not found.
        """
        # Construct the full file path of the thumbnail image
        file_name = f"{thumbnail_id}.jpg"
        thumbnail_path = os.path.join(VideoService.THUMBNAIL_DIR, file_name)

        # Check if the thumbnail file exists
        if not await VideoService.storage_service.file_exists(thumbnail_path):
            raise FileNotFoundError("Thumbnail file not found")

        # Read the file content
        file_content = await VideoService.storage_service.read_file(thumbnail_path)
        return file_content, file_name
