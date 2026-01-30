from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    # API Keys
    GROQ_API_KEY: str
    HF_TOKEN: str = ""
    
    # Model Paths
    CNN_MODEL_PATH: str = "./trained_models/cnn_face_emotion.pth"
    AUDIO_MODEL_NAME: str = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
    
    # App Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Base configuration values
    MAX_AUDIO_SIZE_MB: int = 10
    MAX_IMAGE_SIZE_MB: int = 5
    ALLOWED_AUDIO_FORMATS: str = "wav,mp3,ogg,webm,m4a"
    ALLOWED_IMAGE_FORMATS: str = "jpg,jpeg,png"
    AUDIO_CONFIDENCE_THRESHOLD: float = 0.70
    FACE_CONFIDENCE_THRESHOLD: float = 0.65
    REQUEST_FACE_CONFIRMATION: bool = True
    TEMP_FILE_CLEANUP_HOURS: int = 1
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    TEMP_DIR: str = "./storage/temp"
    
    # Pydantic Configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore", 
        case_sensitive=True
    )

    # --- MISSING PROPERTIES CAUSING THE 500 ERROR ---
    
    @property
    def max_audio_size_bytes(self) -> int:
        """Converts MB to Bytes for backend validation"""
        return self.MAX_AUDIO_SIZE_MB * 1024 * 1024

    @property
    def max_image_size_bytes(self) -> int:
        """Converts MB to Bytes for backend validation"""
        return self.MAX_IMAGE_SIZE_MB * 1024 * 1024

    @property
    def allowed_audio_formats_list(self) -> List[str]:
        return [fmt.strip() for fmt in self.ALLOWED_AUDIO_FORMATS.split(",")]

    @property
    def allowed_image_formats_list(self) -> List[str]:
        return [fmt.strip() for fmt in self.ALLOWED_IMAGE_FORMATS.split(",")]

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    # -----------------------------------------------------------------------

# Settings instance creation
settings = Settings()