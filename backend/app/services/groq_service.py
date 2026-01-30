"""
Groq API service for generating responses
"""
from groq import Groq
from app.config import settings
from app.core.logging_config import log
from app.core.exceptions import GroqAPIError
from app.utils.prompt_templates import create_system_prompt, create_user_prompt
from typing import List, Dict, Optional


class GroqService:
    """Service for Groq API interactions"""
    
    def __init__(self):
        self.client = None
        self.model = "llama-3.1-70b-versatile"  # or mixtral-8x7b-32768
    
    def initialize(self):
        """Initialize Groq client"""
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            log.info("Groq client initialized")
        except Exception as e:
            log.error(f"Failed to initialize Groq client: {str(e)}")
            raise GroqAPIError(f"Groq initialization failed: {str(e)}")
    
    async def generate_response(
        self,
        emotion: str,
        user_message: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
        max_tokens: int = 200,
        temperature: float = 0.8
    ) -> str:
        """
        Generate response using Groq API
        
        Args:
            emotion: Detected emotion
            user_message: Optional user message
            conversation_history: Optional previous messages
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation
            
        Returns:
            Generated response text
        """
        try:
            if self.client is None:
                self.initialize()
            
            # Create prompts
            system_prompt = create_system_prompt(emotion)
            user_prompt = create_user_prompt(user_message, emotion)
            
            # Build messages array
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": user_prompt})
            
            log.info(f"Generating response for emotion: {emotion}")
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
            )
            
            # Extract response
            response = chat_completion.choices[0].message.content
            
            log.info(f"Generated response ({len(response)} chars)")
            
            return response
            
        except Exception as e:
            log.error(f"Groq API call failed: {str(e)}")
            raise GroqAPIError(f"Failed to generate response: {str(e)}")
    
    async def generate_quick_response(self, emotion: str) -> str:
        """
        Generate a quick response based only on emotion
        
        Args:
            emotion: Detected emotion
            
        Returns:
            Quick response text
        """
        return await self.generate_response(
            emotion=emotion,
            max_tokens=100,
            temperature=0.9
        )


# Global service instance
groq_service = GroqService()
