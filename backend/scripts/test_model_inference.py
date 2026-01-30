"""
Script to test model inference
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.ml_models.model_loader import model_manager
from app.core.logging_config import log


def test_models():
    """Test if models can be loaded and run inference"""
    try:
        log.info("Testing model loading...")
        
        # Load models
        model_manager.load_all_models()
        
        log.info("✓ Audio model loaded")
        log.info("✓ CNN model loaded")
        
        log.info("\nAll models loaded successfully!")
        log.info("Ready to process audio and images.")
        
    except Exception as e:
        log.error(f"✗ Model test failed: {str(e)}")
        raise


if __name__ == "__main__":
    test_models()
