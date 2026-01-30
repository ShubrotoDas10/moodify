"""
Pydantic schemas for chat functionality
"""
from pydantic import BaseModel, Field
from typing import Optional
from app.models.schemas.emotion import EmotionResponse, EmotionFusionResponse


class ChatRequest(BaseModel):
    """Request model for chat"""
    message: Optional[str] = Field(None, description="Optional text message")
    emotion_context: Optional[str] = Field(None, description="Detected emotion context")
    conversation_history: Optional[list] = Field(default_factory=list, description="Previous messages")


class ChatResponse(BaseModel):
    """Response model for chat"""
    message: str = Field(..., description="AI generated response")
    emotion_detected: Optional[str] = Field(None, description="Emotion that was detected")
    strategy_used: Optional[str] = Field(None, description="Response strategy applied")


class AudioChatRequest(BaseModel):
    """Request combining audio emotion and chat"""
    pass  # File will be uploaded as multipart


class AudioChatResponse(BaseModel):
    """Response combining emotion detection and chat"""
    emotion: EmotionResponse
    chat_response: ChatResponse


class ImageChatRequest(BaseModel):
    """Request combining image emotion and chat"""
    pass  # File will be uploaded as multipart


class ImageChatResponse(BaseModel):
    """Response combining emotion detection and chat"""
    emotion: EmotionResponse
    chat_response: ChatResponse


class MultimodalChatResponse(BaseModel):
    """Response when both audio and image are provided"""
    emotion: EmotionFusionResponse
    chat_response: ChatResponse
