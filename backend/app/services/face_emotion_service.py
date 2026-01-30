"""
Face emotion detection service
"""
import torch
from app.models.ml_models.model_loader import model_manager
from app.models.schemas.emotion import EmotionResponse
from app.utils.image_processing import process_image_for_emotion
from app.core.constants import EMOTION_LABELS
from app.core.logging_config import log
from app.core.exceptions import EmotionDetectionError, ImageProcessingError
from app.config import settings
from typing import Dict


class FaceEmotionService:
    """Service for face emotion detection"""
    
    def __init__(self):
        self.model = None
    
    def initialize(self):
        """Initialize the CNN model (returns None if unavailable)"""
        self.model = model_manager.get_cnn_model()
        if self.model is None:
            log.warning("CNN model not available - face emotion detection disabled")
    
    async def detect_emotion(self, image_path: str) -> EmotionResponse:
        """
        Detect emotion from face image
        
        Args:
            image_path: Path to image file
            
        Returns:
            EmotionResponse object
            
        Raises:
            EmotionDetectionError: If CNN model is not available
        """
        try:
            if self.model is None:
                self.initialize()
            
            # Check if CNN is available
            if self.model is None:
                raise EmotionDetectionError(
                    "Face emotion detection is not available. "
                    "CNN model not loaded. Please add your trained model to trained_models/ directory."
                )
            
            log.info(f"Detecting emotion from image: {image_path}")
            
            # Process image and detect face
            face_tensor, face_detected, coordinates = process_image_for_emotion(image_path)
            
            if not face_detected:
                raise ImageProcessingError("No face detected in image")
            
            log.info(f"Face detected at coordinates: {coordinates}")
            
            # Predict emotion
            probabilities = self.model.predict(face_tensor)
            
            # Convert to numpy and get predictions
            probs_numpy = probabilities.cpu().numpy()[0]
            
            # Get top emotion
            top_emotion_idx = probs_numpy.argmax()
            top_emotion = EMOTION_LABELS[top_emotion_idx]
            confidence = float(probs_numpy[top_emotion_idx])
            
            # Create probabilities dict
            emotion_probs = {
                EMOTION_LABELS[i]: float(probs_numpy[i])
                for i in range(len(EMOTION_LABELS))
            }
            
            log.info(f"Detected emotion: {top_emotion} (confidence: {confidence:.2f})")
            
            # Check if confidence is too low
            needs_confirmation = confidence < settings.FACE_CONFIDENCE_THRESHOLD
            
            if needs_confirmation:
                log.warning(f"Low confidence ({confidence:.2f}) for face emotion")
            
            return EmotionResponse(
                emotion=top_emotion,
                confidence=confidence,
                probabilities=emotion_probs,
                needs_confirmation=needs_confirmation,
                source="face"
            )
            
        except ImageProcessingError:
            raise
        except Exception as e:
            log.error(f"Face emotion detection failed: {str(e)}")
            raise EmotionDetectionError(f"Face emotion detection failed: {str(e)}")


# Global service instance
face_emotion_service = FaceEmotionService()
