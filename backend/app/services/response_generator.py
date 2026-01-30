"""
Response generation service - combines emotion detection with Groq
"""
from app.services.groq_service import groq_service
from app.models.schemas.chat import ChatResponse
from app.utils.emotion_mapping import get_emotion_strategy
from app.core.logging_config import log
from typing import Optional, List, Dict


class ResponseGenerator:
    """Service for generating emotion-aware responses"""
    
    def __init__(self):
        self.groq = groq_service
    
    async def generate_response(
        self,
        emotion: str,
        user_message: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> ChatResponse:
        """
        Generate a response based on detected emotion
        
        Args:
            emotion: Detected emotion
            user_message: Optional user message
            conversation_history: Optional conversation history
            
        Returns:
            ChatResponse object
        """
        try:
            log.info(f"Generating response for emotion: {emotion}")
            
            # Get emotion strategy
            strategy = get_emotion_strategy(emotion)
            
            # Generate response using Groq
            response_text = await self.groq.generate_response(
                emotion=emotion,
                user_message=user_message,
                conversation_history=conversation_history
            )
            
            return ChatResponse(
                message=response_text,
                emotion_detected=emotion,
                strategy_used=strategy['approach']
            )
            
        except Exception as e:
            log.error(f"Response generation failed: {str(e)}")
            # Fallback response
            return ChatResponse(
                message=self._get_fallback_response(emotion),
                emotion_detected=emotion,
                strategy_used="fallback"
            )
    
    def _get_fallback_response(self, emotion: str) -> str:
        """
        Get a fallback response if Groq fails
        
        Args:
            emotion: Detected emotion
            
        Returns:
            Fallback response string
        """
        fallback_responses = {
            "happy": "That's great to hear! Keep that positive energy going! 😊",
            "sad": "I'm here for you. Sometimes just talking about things helps. What's on your mind?",
            "angry": "I understand you're frustrated. Take a deep breath. Want to talk about it?",
            "fear": "It's okay to feel anxious. You're not alone. Let's take this one step at a time.",
            "surprise": "Wow, that's unexpected! How are you feeling about it?",
            "disgust": "I hear you. That doesn't sound pleasant at all. Need to vent?",
            "neutral": "Hey there! How can I help brighten your day? 😊"
        }
        
        return fallback_responses.get(emotion, "I'm here to chat! What's on your mind?")


# Global service instance
response_generator = ResponseGenerator()
