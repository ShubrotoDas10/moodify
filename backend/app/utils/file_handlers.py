"""
File upload and validation utilities
"""
import os
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from fastapi import UploadFile
from app.config import settings
from app.core.logging_config import log
from app.core.exceptions import FileValidationError


def validate_audio_file(file: UploadFile) -> bool:
    """
    Validate audio file upload
    
    Args:
        file: Uploaded file
        
    Returns:
        True if valid
        
    Raises:
        FileValidationError if invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower().lstrip('.')
    
    if file_ext not in settings.allowed_audio_formats_list:
        raise FileValidationError(
            f"Invalid audio format. Allowed: {', '.join(settings.allowed_audio_formats_list)}"
        )
    
    # Check file size (if content_length is available)
    if hasattr(file, 'size') and file.size:
        if file.size > settings.max_audio_size_bytes:
            raise FileValidationError(
                f"Audio file too large. Max size: {settings.MAX_AUDIO_SIZE_MB}MB"
            )
    
    return True


def validate_image_file(file: UploadFile) -> bool:
    """
    Validate image file upload
    
    Args:
        file: Uploaded file
        
    Returns:
        True if valid
        
    Raises:
        FileValidationError if invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower().lstrip('.')
    
    if file_ext not in settings.allowed_image_formats_list:
        raise FileValidationError(
            f"Invalid image format. Allowed: {', '.join(settings.allowed_image_formats_list)}"
        )
    
    # Check file size
    if hasattr(file, 'size') and file.size:
        if file.size > settings.max_image_size_bytes:
            raise FileValidationError(
                f"Image file too large. Max size: {settings.MAX_IMAGE_SIZE_MB}MB"
            )
    
    return True


async def save_upload_file(file: UploadFile, file_type: str = "audio") -> str:
    """
    Save uploaded file to temporary storage
    
    Args:
        file: Uploaded file
        file_type: Type of file ("audio" or "image")
        
    Returns:
        Path to saved file
    """
    try:
        # Create unique filename
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Determine save directory
        if file_type == "audio":
            save_dir = Path(settings.TEMP_DIR) / "audio"
        else:
            save_dir = Path(settings.TEMP_DIR) / "images"
        
        # Create directory if it doesn't exist
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = save_dir / unique_filename
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        log.info(f"File saved: {file_path}")
        return str(file_path)
        
    except Exception as e:
        log.error(f"Failed to save file: {str(e)}")
        raise FileValidationError(f"Failed to save file: {str(e)}")


def cleanup_old_files():
    """
    Clean up old temporary files
    """
    try:
        temp_dir = Path(settings.TEMP_DIR)
        if not temp_dir.exists():
            return
        
        # Calculate cutoff time
        cutoff_time = datetime.now() - timedelta(hours=settings.TEMP_FILE_CLEANUP_HOURS)
        
        # Clean up audio files
        audio_dir = temp_dir / "audio"
        if audio_dir.exists():
            for file_path in audio_dir.iterdir():
                if file_path.is_file():
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_mtime < cutoff_time:
                        file_path.unlink()
                        log.info(f"Deleted old file: {file_path}")
        
        # Clean up image files
        image_dir = temp_dir / "images"
        if image_dir.exists():
            for file_path in image_dir.iterdir():
                if file_path.is_file():
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_mtime < cutoff_time:
                        file_path.unlink()
                        log.info(f"Deleted old file: {file_path}")
        
        log.info("Temporary file cleanup completed")
        
    except Exception as e:
        log.error(f"File cleanup failed: {str(e)}")


def delete_file(file_path: str):
    """
    Delete a specific file
    
    Args:
        file_path: Path to file to delete
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            log.info(f"Deleted file: {file_path}")
    except Exception as e:
        log.error(f"Failed to delete file {file_path}: {str(e)}")


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
    """
    try:
        return Path(file_path).stat().st_size
    except Exception as e:
        log.error(f"Failed to get file size: {str(e)}")
        return 0
