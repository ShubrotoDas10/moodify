"""
Logging configuration using loguru
"""
from loguru import logger
import sys
from app.config import settings


def setup_logging():
    """Configure loguru logger"""
    
    # Remove default handler
    logger.remove()
    
    # Add custom handler with formatting
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # Add file handler for production
    if settings.ENVIRONMENT == "production":
        logger.add(
            "logs/moodify_{time:YYYY-MM-DD}.log",
            rotation="00:00",
            retention="7 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        )
    
    return logger


# Initialize logger
log = setup_logging()
