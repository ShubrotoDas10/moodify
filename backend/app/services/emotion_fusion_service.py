"""
Emotion fusion service - combines audio and face emotions
"""
from app.models.schemas.emotion import EmotionResponse, EmotionFusionResponse
from app.utils.emotion_mapping import combine_emotions
from app.core.logging_config import log


class EmotionFusionService:
    """Service for combining emotions from multiple sources"""
    
    async def fuse_emotions(
        self,
        audio_emotion: EmotionResponse,
        face_emotion: EmotionResponse
    ) -> EmotionFusionResponse:
        """
        Fuse audio and face emotions into a single determination
        
        Args:
            audio_emotion: Emotion from audio
            face_emotion: Emotion from face
            
        Returns:
            EmotionFusionResponse with combined result
        """
        try:
            log.info("Fusing audio and face emotions")
            
            # Combine emotions
            final_emotion, final_confidence, fusion_method = combine_emotions(
                audio_emotion=audio_emotion.emotion,
                face_emotion=face_emotion.emotion,
                audio_confidence=audio_emotion.confidence,
                face_confidence=face_emotion.confidence
            )
            
            log.info(
                f"Fusion result: {final_emotion} (confidence: {final_confidence:.2f}, "
                f"method: {fusion_method})"
            )
            
            return EmotionFusionResponse(
                final_emotion=final_emotion,
                confidence=final_confidence,
                audio_emotion=audio_emotion,
                face_emotion=face_emotion,
                fusion_method=fusion_method
            )
            
        except Exception as e:
            log.error(f"Emotion fusion failed: {str(e)}")
            # Fallback to audio emotion if fusion fails
            return EmotionFusionResponse(
                final_emotion=audio_emotion.emotion,
                confidence=audio_emotion.confidence,
                audio_emotion=audio_emotion,
                face_emotion=face_emotion,
                fusion_method="fallback_audio"
            )


# Global service instance
emotion_fusion_service = EmotionFusionService()
