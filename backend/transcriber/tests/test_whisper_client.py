import pytest
import requests
from unittest.mock import patch, mock_open
from whisper_client import transcribe_audio

# Simular contenido de archivo de audio
DUMMY_AUDIO_CONTENT = b"fake audio content"

# Simular respuesta de OpenAI Whisper
FAKE_TRANSCRIPTION = {"text": "Paciente con dolor abdominal y fiebre."}

@patch("medical_ai_common.whisper_client.openai.Audio.transcribe")
@patch("medical_ai_common.whisper_client.requests.get")
def test_transcribe_audio_success(mock_requests_get, mock_transcribe):
    # Simular la descarga del archivo
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.content = DUMMY_AUDIO_CONTENT

    # Simular la transcripción de OpenAI
    mock_transcribe.return_value = FAKE_TRANSCRIPTION

    # Ejecutar la función
    audio_url = "https://example.com/audio.mp3"
    result = transcribe_audio(audio_url)

    # Verificar resultados
    assert result == FAKE_TRANSCRIPTION["text"]
    mock_requests_get.assert_called_once_with(audio_url)
    mock_transcribe.assert_called_once()

@patch("medical_ai_common.whisper_client.requests.get")
def test_transcribe_audio_download_fail(mock_requests_get):
    mock_requests_get.return_value.status_code = 404

    with pytest.raises(Exception) as exc_info:
        transcribe_audio("https://invalid-url.com/audio.mp3")

    assert "No se pudo descargar" in str(exc_info.value)
