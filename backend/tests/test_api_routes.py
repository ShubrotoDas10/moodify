"""
Test API routes
"""
import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_models_status(client: TestClient):
    """Test models status endpoint"""
    response = client.get("/health/models")
    assert response.status_code == 200
    assert "models_loaded" in response.json()


def test_readiness_check(client: TestClient):
    """Test readiness endpoint"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert "ready" in response.json()


# Add more tests for your specific endpoints
@pytest.mark.skip(reason="Requires actual audio file")
def test_audio_emotion_detection(client: TestClient, sample_audio_path):
    """Test audio emotion detection"""
    with open(sample_audio_path, 'rb') as audio:
        files = {'audio': audio}
        response = client.post("/audio/detect-emotion", files=files)
        assert response.status_code == 200
        assert "emotion" in response.json()


@pytest.mark.skip(reason="Requires actual image file")
def test_image_emotion_detection(client: TestClient, sample_image_path):
    """Test face emotion detection"""
    with open(sample_image_path, 'rb') as image:
        files = {'image': image}
        response = client.post("/image/detect-emotion", files=files)
        assert response.status_code == 200
        assert "emotion" in response.json()
