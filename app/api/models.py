from pydantic import BaseModel, Field
from typing import Optional

class VideoUploadResponse(BaseModel):
    filename: str = Field(..., description="Original name of the uploaded video file")
    file_id: str = Field(..., description="Generated unique ID for the uploaded video file")
    
class ThumbnailResponse(BaseModel):
    thumbnail_id: str

class ThumbnailRequest(BaseModel):
    file_id: str
    timestamp: int
    resolution: Optional[str] = "320x240"
