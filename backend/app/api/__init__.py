"""
API module initialization
"""
from app.api.routes import health, audio, image, chat
from app.api.middleware import setup_middleware

__all__ = ['health', 'audio', 'image', 'chat', 'setup_middleware']
