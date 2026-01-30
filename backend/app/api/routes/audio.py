from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.audio_emotion_service import audio_emotion_service
from app.utils.file_handlers import validate_audio_file, save_upload_file, delete_file
import os
import logging

# Logger setup
logger = logging.getLogger(__name__)

# Prefix ko '/audio' rakha hai taaki frontend ki request (404 error) fix ho jaye
router = APIRouter(prefix="/audio", tags=["audio"])

@router.post("/detect-emotion")
async def detect_emotion_from_audio(
    audio: UploadFile = File(..., description="Audio file for mood detection")
):
    """
    Endpoint to receive audio, transcribe it, detect emotion, and get AI response.
    Matches the frontend call: POST /audio/detect-emotion
    """
    audio_path = None
    try:
        # 1. Validate the incoming file
        validate_audio_file(audio)
        
        # 2. Save file temporarily to disk
        audio_path = await save_upload_file(audio, file_type="audio")
        logger.info(f"Audio file saved temporarily at: {audio_path}")
        
        # 3. Process audio through the service (ML Model + Groq API)
        # Isme humne Groq syntax pehle hi fix kar diya hai
        result = await audio_emotion_service.detect_emotion_and_respond(audio_path)
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing audio request: {str(e)}")
        # Frontend ko clear error message bhejna
        raise HTTPException(status_code=500, detail=f"Failed to process audio: {str(e)}")
        
    finally:
        # 4. Clean up: Delete the temporary file to save space
        if audio_path and os.path.exists(audio_path):
            delete_file(audio_path)
            logger.info(f"Temporary file deleted: {audio_path}")