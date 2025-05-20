import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.extracter.main import app

client = TestClient(app)

@patch("medical_ai_common.openai_client.extract_medical_info")
def test_extract_endpoint_success(mock_extract):
    mock_extract.return_value = {
        "patient": {"name": "Luis", "age": 32, "id": "123"},
        "symptoms": ["fiebre", "dolor"],
        "reasonForVisit": "consulta general"
    }

    response = client.post("/extract", json={"text": "Paciente con fiebre y dolor."})
    
    assert response.status_code == 200
    data = response.json()
    assert "patient" in data
    assert "symptoms" in data
    assert data["patient"]["name"] == "Luis"

def test_extract_missing_text():
    response = client.post("/extract", json={})
    assert response.status_code == 422
