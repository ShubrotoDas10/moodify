"""
Image processing utilities for face emotion detection
"""
import cv2
import numpy as np
import torch
from PIL import Image
from pathlib import Path
from app.core.logging_config import log
from app.core.exceptions import ImageProcessingError
from app.core.constants import IMAGE_SIZE


def load_image(image_path: str) -> np.ndarray:
    """
    Load image from file
    
    Args:
        image_path: Path to image file
        
    Returns:
        Image as numpy array
    """
    try:
        image = cv2.imread(str(image_path))
        if image is None:
            raise ImageProcessingError(f"Failed to load image: {image_path}")
        return image
    except Exception as e:
        log.error(f"Image loading failed: {str(e)}")
        raise ImageProcessingError(f"Failed to load image: {str(e)}")


def detect_face(image: np.ndarray) -> tuple:
    """
    Detect face in image using Haar Cascade
    
    Args:
        image: Input image as numpy array
        
    Returns:
        Tuple of (face_detected, face_region, coordinates)
    """
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            log.warning("No face detected in image")
            return False, None, None
        
        # Get the largest face (closest to camera)
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        
        # Extract face region
        face_region = gray[y:y+h, x:x+w]
        
        log.info(f"Face detected at coordinates: ({x}, {y}, {w}, {h})")
        return True, face_region, (x, y, w, h)
        
    except Exception as e:
        log.error(f"Face detection failed: {str(e)}")
        raise ImageProcessingError(f"Face detection failed: {str(e)}")


def preprocess_face_for_cnn(face_region: np.ndarray, target_size: tuple = IMAGE_SIZE) -> torch.Tensor:
    """
    Preprocess face image for CNN input
    
    Args:
        face_region: Face region as numpy array (grayscale)
        target_size: Target size for resizing (default 48x48)
        
    Returns:
        Preprocessed image tensor (1, 1, 48, 48)
    """
    try:
        # Resize to target size
        face_resized = cv2.resize(face_region, target_size)
        
        # Normalize pixel values to [0, 1]
        face_normalized = face_resized.astype('float32') / 255.0
        
        # Convert to tensor and add batch and channel dimensions
        face_tensor = torch.from_numpy(face_normalized).unsqueeze(0).unsqueeze(0)
        
        log.info(f"Face preprocessed to tensor shape: {face_tensor.shape}")
        return face_tensor
        
    except Exception as e:
        log.error(f"Face preprocessing failed: {str(e)}")
        raise ImageProcessingError(f"Face preprocessing failed: {str(e)}")


def process_image_for_emotion(image_path: str) -> tuple:
    """
    Complete pipeline: load image, detect face, preprocess for CNN
    
    Args:
        image_path: Path to image file
        
    Returns:
        Tuple of (face_tensor, face_detected, coordinates)
    """
    try:
        # Load image
        image = load_image(image_path)
        
        # Detect face
        face_detected, face_region, coordinates = detect_face(image)
        
        if not face_detected:
            return None, False, None
        
        # Preprocess for CNN
        face_tensor = preprocess_face_for_cnn(face_region)
        
        return face_tensor, True, coordinates
        
    except Exception as e:
        log.error(f"Image processing pipeline failed: {str(e)}")
        raise ImageProcessingError(f"Image processing failed: {str(e)}")


def save_processed_face(face_region: np.ndarray, output_path: str):
    """
    Save processed face region (for debugging)
    
    Args:
        face_region: Face region as numpy array
        output_path: Path to save the face
    """
    try:
        cv2.imwrite(str(output_path), face_region)
        log.info(f"Face saved to: {output_path}")
    except Exception as e:
        log.error(f"Failed to save face: {str(e)}")


def get_image_info(image_path: str) -> dict:
    """
    Get image information
    
    Args:
        image_path: Path to image
        
    Returns:
        Dictionary with image info
    """
    try:
        with Image.open(image_path) as img:
            return {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height
            }
    except Exception as e:
        log.error(f"Failed to get image info: {str(e)}")
        return {}
