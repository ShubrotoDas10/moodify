"""
Model loader and manager for ML models
"""
import torch
from pathlib import Path
from app.models.ml_models.cnn_architecture import EmotionCNN, SimpleCNN
from app.models.ml_models.audio_model_wrapper import audio_model
from app.config import settings
from app.core.logging_config import log
from app.core.exceptions import ModelLoadError
from app.core.constants import EMOTION_LABELS


class CNNModelLoader:
    """Loader for CNN face emotion model"""
    
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        log.info(f"CNN Model will use device: {self.device}")
    
    def load(self, model_path: str = None, model_type: str = "EmotionCNN"):
        """
        Load the trained CNN model (optional - graceful failure)
        
        Args:
            model_path: Path to model weights (.pth file)
            model_type: Type of model architecture ("EmotionCNN" or "SimpleCNN")
        """
        try:
            if model_path is None:
                model_path = settings.CNN_MODEL_PATH
            
            model_path = Path(model_path)
            
            if not model_path.exists():
                log.warning(f"CNN model file not found: {model_path}")
                log.warning("CNN face emotion detection will be unavailable")
                log.warning("Audio emotion detection will still work normally")
                return  # Graceful failure - don't raise exception
            
            log.info(f"Loading CNN model from: {model_path}")
            
            # Initialize model architecture
            if model_type == "EmotionCNN":
                self.model = EmotionCNN(num_classes=len(EMOTION_LABELS))
            elif model_type == "SimpleCNN":
                self.model = SimpleCNN(num_classes=len(EMOTION_LABELS))
            else:
                log.warning(f"Unknown model type: {model_type}, CNN will be unavailable")
                return
            
            # Load weights
            state_dict = torch.load(model_path, map_location=self.device)
            
            # Handle different state dict formats
            if 'model_state_dict' in state_dict:
                self.model.load_state_dict(state_dict['model_state_dict'])
            else:
                self.model.load_state_dict(state_dict)
            
            # Move to device and set to evaluation mode
            self.model.to(self.device)
            self.model.eval()
            
            log.info("CNN model loaded successfully")
            
        except Exception as e:
            log.warning(f"Failed to load CNN model: {str(e)}")
            log.warning("CNN face emotion detection will be unavailable")
            log.warning("Audio emotion detection will still work normally")
            self.model = None  # Ensure model is None on failure
    
    def predict(self, image_tensor: torch.Tensor):
        """
        Predict emotion from image tensor
        
        Args:
            image_tensor: Preprocessed image tensor (1, 1, 48, 48)
            
        Returns:
            Predictions tensor
        """
        if self.model is None:
            raise ModelLoadError("Model not loaded. Call load() first.")
        
        try:
            with torch.no_grad():
                image_tensor = image_tensor.to(self.device)
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                return probabilities
        except Exception as e:
            log.error(f"CNN prediction failed: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None


class ModelManager:
    """Manager for all ML models"""
    
    def __init__(self):
        self.cnn_loader = CNNModelLoader()
        self.audio_loader = audio_model
        self._models_loaded = False
    
    def load_all_models(self):
        """Load all models on startup (CNN is optional)"""
        log.info("Loading ML models...")
        
        try:
            # Load audio model (required)
            log.info("Loading audio emotion model...")
            self.audio_loader.load()
            log.info("✓ Audio emotion model loaded successfully")
            
        except Exception as e:
            log.error(f"Failed to load audio model: {str(e)}")
            raise ModelLoadError(f"Audio model initialization failed: {str(e)}")
        
        # Load CNN model (optional)
        try:
            log.info("Loading CNN face emotion model...")
            self.cnn_loader.load()
            if self.cnn_loader.is_loaded():
                log.info("✓ CNN face emotion model loaded successfully")
            else:
                log.warning("⚠ CNN model not available - face emotion detection disabled")
        except Exception as e:
            log.warning(f"⚠ CNN model loading failed: {str(e)}")
            log.warning("⚠ Face emotion detection will be unavailable")
        
        # Mark as loaded if at least audio model works
        self._models_loaded = True
        log.info("Model loading complete - Audio emotion detection ready!")
        if self.cnn_loader.is_loaded():
            log.info("Face emotion detection is also available")
        else:
            log.info("Face emotion detection is disabled (CNN model not found)")
    
    def are_models_loaded(self) -> bool:
        """Check if required models (audio) are loaded"""
        return self._models_loaded and self.audio_loader.is_loaded()
    
    def is_cnn_available(self) -> bool:
        """Check if CNN model is available"""
        return self.cnn_loader.is_loaded()
    
    def get_cnn_model(self):
        """Get CNN model loader (returns None if unavailable)"""
        if not self.cnn_loader.is_loaded():
            log.warning("CNN model requested but not available")
            return None
        return self.cnn_loader
    
    def get_audio_model(self):
        """Get audio model loader"""
        if not self.audio_loader.is_loaded():
            raise ModelLoadError("Audio model not loaded")
        return self.audio_loader


# Global model manager instance
model_manager = ModelManager()
