import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.transcriber.main import app

client = TestClient(app)

@patch("medical_ai_common.whisper_client.transcribe_audio")
def test_transcribe_endpoint_success(mock_transcribe):
    mock_transcribe.return_value = "Texto transcrito de prueba"

    response = client.post("/transcribe", json={"audio_url": "https://example.com/audio.mp3"})
    
    assert response.status_code == 200
    assert response.json()["transcription"] == "Texto transcrito de prueba"

@patch("medical_ai_common.whisper_client.transcribe_audio")
def test_transcribe_missing_audio_url(mock_transcribe):
    response = client.post("/transcribe", json={})
    assert response.status_code == 422
