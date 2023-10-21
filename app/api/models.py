from pydantic import BaseModel, Field

class VideoUploadResponse(BaseModel):
    filename: str = Field(..., description="Original name of the uploaded video file")
    file_id: str = Field(..., description="Generated unique ID for the uploaded video file")
