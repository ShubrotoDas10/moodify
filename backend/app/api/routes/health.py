"""
Health check and status endpoints
"""
from fastapi import APIRouter
from app.models.ml_models.model_loader import model_manager
from app.core.logging_config import log

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "service": "moodify-backend"}


@router.get("/models")
async def models_status():
    """Check if ML models are loaded"""
    try:
        models_loaded = model_manager.are_models_loaded()
        cnn_available = model_manager.is_cnn_available()
        
        return {
            "models_loaded": models_loaded,
            "audio_model": model_manager.audio_loader.is_loaded(),
            "cnn_model": cnn_available,
            "status": "ready" if models_loaded else "not_ready",
            "message": "Audio emotion detection available" + 
                      (" + Face emotion detection available" if cnn_available else " (Face detection unavailable - CNN not loaded)")
        }
    except Exception as e:
        log.error(f"Model status check failed: {str(e)}")
        return {
            "models_loaded": False,
            "error": str(e)
        }


@router.get("/ready")
async def readiness_check():
    """Readiness check for deployment"""
    try:
        models_loaded = model_manager.are_models_loaded()
        
        if models_loaded:
            return {"ready": True, "message": "Service is ready"}
        else:
            return {"ready": False, "message": "Models not loaded"}
            
    except Exception as e:
        return {"ready": False, "message": str(e)}
