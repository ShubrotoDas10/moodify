"""
Pydantic schemas for file uploads
"""
from pydantic import BaseModel, Field


class AudioUploadResponse(BaseModel):
    """Response after audio upload"""
    filename: str
    size_bytes: int
    format: str
    duration_seconds: float


class ImageUploadResponse(BaseModel):
    """Response after image upload"""
    filename: str
    size_bytes: int
    format: str
    dimensions: tuple
