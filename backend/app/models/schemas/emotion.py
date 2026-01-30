"""
Pydantic schemas for emotion detection
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class EmotionResponse(BaseModel):
    """Response model for emotion detection"""
    emotion: str = Field(..., description="Detected emotion")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    probabilities: Dict[str, float] = Field(default_factory=dict, description="Emotion probabilities")
    needs_confirmation: bool = Field(default=False, description="Whether face confirmation is needed")
    source: str = Field(..., description="Detection source: audio or face")


class EmotionFusionResponse(BaseModel):
    """Response when both audio and face emotions are available"""
    final_emotion: str = Field(..., description="Final determined emotion")
    confidence: float = Field(..., description="Final confidence score")
    audio_emotion: EmotionResponse
    face_emotion: EmotionResponse
    fusion_method: str = Field(..., description="How emotions were combined")
