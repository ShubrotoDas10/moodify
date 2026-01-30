"""
Image/Face emotion detection endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.face_emotion_service import face_emotion_service
from app.models.schemas.emotion import EmotionResponse
from app.core.exceptions import EmotionDetectionError
from app.utils.file_handlers import (
    validate_image_file, save_upload_file, delete_file
)
from app.core.logging_config import log

router = APIRouter(prefix="/image", tags=["image"])


@router.post("/detect-emotion", response_model=EmotionResponse)
async def detect_emotion_from_image(
    image: UploadFile = File(..., description="Image file for face emotion detection")
):
    """
    Detect emotion from facial expression in image
    
    - **image**: Image file containing a face (jpg, jpeg, png)
    
    Returns detected emotion with confidence score
    
    Note: Requires CNN model to be loaded. Returns 503 if CNN is unavailable.
    """
    image_path = None
    try:
        log.info(f"Received image file: {image.filename}")
        
        # Validate file
        validate_image_file(image)
        
        # Save file
        image_path = await save_upload_file(image, file_type="image")
        
        # Detect emotion
        emotion_result = await face_emotion_service.detect_emotion(image_path)
        
        return emotion_result
        
    except EmotionDetectionError as e:
        # CNN not available
        log.warning(f"Face emotion detection unavailable: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Face emotion detection is currently unavailable. CNN model not loaded. Please use audio emotion detection instead."
        )
    except Exception as e:
        log.error(f"Face emotion detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temporary file
        if image_path:
            delete_file(image_path)
