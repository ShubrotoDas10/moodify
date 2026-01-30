"""
Wrapper for HuggingFace audio emotion recognition models
"""
from transformers import pipeline
from app.config import settings
from app.core.logging_config import log
from app.core.exceptions import ModelLoadError
from typing import Dict
import torch


class AudioEmotionModel:
    """Wrapper for HuggingFace audio emotion recognition"""
    
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        log.info(f"Using device: {self.device}")
    
    def load(self):
        """Load the HuggingFace model"""
        try:
            log.info(f"Loading audio emotion model: {settings.AUDIO_MODEL_NAME}")
            
            # Load the pipeline
            self.model = pipeline(
                "audio-classification",
                model=settings.AUDIO_MODEL_NAME,
                device=0 if self.device == "cuda" else -1,
                token=settings.HF_TOKEN if settings.HF_TOKEN else None
            )
            
            log.info("Audio emotion model loaded successfully")
            
        except Exception as e:
            log.error(f"Failed to load audio emotion model: {str(e)}")
            raise ModelLoadError(f"Failed to load audio model: {str(e)}")
    
    def predict(self, audio_path: str) -> Dict:
        """
        Predict emotion from audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with emotion predictions
        """
        if self.model is None:
            raise ModelLoadError("Model not loaded. Call load() first.")
        
        try:
            # Get predictions
            predictions = self.model(audio_path)
            
            # Convert to dictionary format
            result = {
                "predictions": predictions,
                "top_emotion": predictions[0]["label"],
                "confidence": predictions[0]["score"]
            }
            
            return result
            
        except Exception as e:
            log.error(f"Audio emotion prediction failed: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None


# Global instance
audio_model = AudioEmotionModel()
