import os
import librosa
import numpy as np
import json
from groq import Groq
from app.config import settings

class AudioEmotionService:
    def __init__(self):
        # Groq client initializing using settings
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    async def detect_emotion_and_respond(self, audio_path: str):
        # 1. Word Analysis (Transcription)
        with open(audio_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3",
                response_format="text",
            )
        
        # 2. Voice Tone Analysis (Acoustic Analysis)
        # Librosa load karke pitch aur loudness nikalte hain
        y, sr = librosa.load(audio_path)
        energy = np.mean(librosa.feature.rms(y=y))
        
        # Voice energy se tone determine karna
        voice_tone = "energetic/loud" if energy > 0.05 else "calm/soft"
        
        # 3. Hybrid Analysis using LLM (Llama 3.1)
        # Hum words aur voice tone dono Llama ko bhej rahe hain
        prompt = f"""
        User said: '{transcription}'
        User's voice tone: {voice_tone}
        
        Task: Analyze both words and tone to find the emotion. Respond as Goku.
        Format: JSON only with keys 'emotion' and 'reply'.
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        result = json.loads(chat_completion.choices[0].message.content)
        
        return {
            "transcript": transcription,
            "emotion": {"label": result.get("emotion", "neutral")},
            "chat_response": {"message": result.get("reply", "I'm ready to train!")}
        }

# Instance creation for routes to use
audio_emotion_service = AudioEmotionService()