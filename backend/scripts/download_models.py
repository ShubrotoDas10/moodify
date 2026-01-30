"""
Script to download HuggingFace models
"""
from transformers import pipeline
from app.config import settings
from app.core.logging_config import log


def download_audio_model():
    """Download the audio emotion recognition model"""
    try:
        log.info(f"Downloading model: {settings.AUDIO_MODEL_NAME}")
        
        # This will download and cache the model
        pipeline(
            "audio-classification",
            model=settings.AUDIO_MODEL_NAME,
            token=settings.HF_TOKEN if settings.HF_TOKEN else None
        )
        
        log.info("Model downloaded successfully")
        log.info(f"Model cached in: ~/.cache/huggingface/")
        
    except Exception as e:
        log.error(f"Failed to download model: {str(e)}")
        raise


if __name__ == "__main__":
    download_audio_model()
