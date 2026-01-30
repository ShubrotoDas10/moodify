"""
Chat endpoints - main functionality
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.services.audio_emotion_service import audio_emotion_service
from app.services.face_emotion_service import face_emotion_service
from app.services.emotion_fusion_service import emotion_fusion_service
from app.services.response_generator import response_generator
from app.models.schemas.chat import (
    AudioChatResponse, ImageChatResponse, MultimodalChatResponse,
    ChatRequest, ChatResponse
)
from app.models.schemas.emotion import EmotionResponse, EmotionFusionResponse
from app.core.exceptions import EmotionDetectionError
from app.utils.file_handlers import (
    validate_audio_file, validate_image_file,
    save_upload_file, delete_file
)
from app.core.logging_config import log
import json

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/audio", response_model=AudioChatResponse)
async def chat_with_audio(
    audio: UploadFile = File(..., description="Audio file for emotion detection"),
    message: Optional[str] = Form(None, description="Optional text message"),
    conversation_history: Optional[str] = Form(None, description="JSON string of conversation history")
):
    """
    Chat with audio emotion detection
    
    - **audio**: Audio file (wav, mp3, ogg, webm, m4a)
    - **message**: Optional text message from user
    - **conversation_history**: Optional JSON string of previous messages
    
    Returns emotion detection + AI response
    """
    audio_path = None
    try:
        log.info(f"Audio chat request: {audio.filename}")
        
        # Validate and save audio
        validate_audio_file(audio)
        audio_path = await save_upload_file(audio, file_type="audio")
        
        # Detect emotion from audio
        emotion_result = await audio_emotion_service.detect_emotion(audio_path)
        
        # Parse conversation history
        history = None
        if conversation_history:
            try:
                history = json.loads(conversation_history)
            except:
                log.warning("Failed to parse conversation history")
        
        # Generate response
        chat_response = await response_generator.generate_response(
            emotion=emotion_result.emotion,
            user_message=message,
            conversation_history=history
        )
        
        return AudioChatResponse(
            emotion=emotion_result,
            chat_response=chat_response
        )
        
    except Exception as e:
        log.error(f"Audio chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if audio_path:
            delete_file(audio_path)


@router.post("/image", response_model=ImageChatResponse)
async def chat_with_image(
    image: UploadFile = File(..., description="Image file for face emotion detection"),
    message: Optional[str] = Form(None, description="Optional text message"),
    conversation_history: Optional[str] = Form(None, description="JSON string of conversation history")
):
    """
    Chat with face emotion detection (confirmation/fallback)
    
    - **image**: Image file with face (jpg, jpeg, png)
    - **message**: Optional text message from user
    - **conversation_history**: Optional JSON string of previous messages
    
    Returns emotion detection + AI response
    
    Note: Requires CNN model to be loaded. Returns error if CNN is unavailable.
    """
    image_path = None
    try:
        log.info(f"Image chat request: {image.filename}")
        
        # Validate and save image
        validate_image_file(image)
        image_path = await save_upload_file(image, file_type="image")
        
        # Detect emotion from face
        try:
            emotion_result = await face_emotion_service.detect_emotion(image_path)
        except EmotionDetectionError as e:
            raise HTTPException(
                status_code=503,
                detail="Face emotion detection is currently unavailable. CNN model not loaded. Please use audio emotion detection instead."
            )
        
        # Parse conversation history
        history = None
        if conversation_history:
            try:
                history = json.loads(conversation_history)
            except:
                log.warning("Failed to parse conversation history")
        
        # Generate response
        chat_response = await response_generator.generate_response(
            emotion=emotion_result.emotion,
            user_message=message,
            conversation_history=history
        )
        
        return ImageChatResponse(
            emotion=emotion_result,
            chat_response=chat_response
        )
        
    except Exception as e:
        log.error(f"Image chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if image_path:
            delete_file(image_path)


@router.post("/multimodal", response_model=MultimodalChatResponse)
async def chat_with_audio_and_image(
    audio: UploadFile = File(..., description="Audio file for emotion detection"),
    image: UploadFile = File(..., description="Image file for face emotion detection"),
    message: Optional[str] = Form(None, description="Optional text message"),
    conversation_history: Optional[str] = Form(None, description="JSON string of conversation history")
):
    """
    Chat with both audio and face emotion detection (highest confidence)
    
    - **audio**: Audio file (wav, mp3, ogg, webm, m4a)
    - **image**: Image file with face (jpg, jpeg, png)
    - **message**: Optional text message from user
    - **conversation_history**: Optional JSON string of previous messages
    
    Returns fused emotion detection + AI response
    
    Note: If CNN is unavailable, falls back to audio-only detection.
    """
    audio_path = None
    image_path = None
    try:
        log.info(f"Multimodal chat request: {audio.filename}, {image.filename}")
        
        # Validate and save both files
        validate_audio_file(audio)
        validate_image_file(image)
        audio_path = await save_upload_file(audio, file_type="audio")
        image_path = await save_upload_file(image, file_type="image")
        
        # Detect emotions from both sources
        audio_emotion = await audio_emotion_service.detect_emotion(audio_path)
        
        # Try to get face emotion, fall back to audio-only if CNN unavailable
        try:
            face_emotion = await face_emotion_service.detect_emotion(image_path)
            
            # Fuse emotions
            fused_emotion = await emotion_fusion_service.fuse_emotions(
                audio_emotion=audio_emotion,
                face_emotion=face_emotion
            )
        except EmotionDetectionError as e:
            log.warning(f"Face detection unavailable, using audio only: {str(e)}")
            # Use audio emotion only
            fused_emotion = EmotionFusionResponse(
                final_emotion=audio_emotion.emotion,
                confidence=audio_emotion.confidence,
                audio_emotion=audio_emotion,
                face_emotion=EmotionResponse(
                    emotion="unavailable",
                    confidence=0.0,
                    probabilities={},
                    needs_confirmation=False,
                    source="face"
                ),
                fusion_method="audio_only_cnn_unavailable"
            )
        
        # Parse conversation history
        history = None
        if conversation_history:
            try:
                history = json.loads(conversation_history)
            except:
                log.warning("Failed to parse conversation history")
        
        # Generate response based on fused emotion
        chat_response = await response_generator.generate_response(
            emotion=fused_emotion.final_emotion,
            user_message=message,
            conversation_history=history
        )
        
        return MultimodalChatResponse(
            emotion=fused_emotion,
            chat_response=chat_response
        )
        
    except Exception as e:
        log.error(f"Multimodal chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if audio_path:
            delete_file(audio_path)
        if image_path:
            delete_file(image_path)


@router.post("/text", response_model=ChatResponse)
async def chat_with_text(request: ChatRequest):
    """
    Chat with text only (no emotion detection)
    
    - **message**: Text message from user
    - **emotion_context**: Optional emotion context from previous detection
    - **conversation_history**: Optional previous messages
    
    Returns AI response
    """
    try:
        log.info("Text-only chat request")
        
        # Use provided emotion context or default to neutral
        emotion = request.emotion_context or "neutral"
        
        # Generate response
        chat_response = await response_generator.generate_response(
            emotion=emotion,
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        return chat_response
        
    except Exception as e:
        log.error(f"Text chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
