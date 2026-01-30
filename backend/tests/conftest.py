"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def sample_audio_path():
    """Sample audio file path"""
    return "tests/data/sample_audio.wav"


@pytest.fixture
def sample_image_path():
    """Sample image file path"""
    return "tests/data/sample_face.jpg"
