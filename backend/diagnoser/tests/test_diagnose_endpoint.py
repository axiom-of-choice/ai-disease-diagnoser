import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.diagnoser.main import app

client = TestClient(app)

@patch("medical_ai_common.openai_client.generate_diagnosis")
def test_diagnose_endpoint_success(mock_diagnose):
    mock_diagnose.return_value = {
        "diagnosis": "Gripe común",
        "treatment": "Reposo e hidratación",
        "recommendations": "Consultar si los síntomas empeoran"
    }

    payload = {
        "patient": {"name": "Ana", "age": 25, "id": "001"},
        "symptoms": ["tos", "fiebre"],
        "reasonForVisit": "resfriado"
    }

    response = client.post("/diagnose", json=payload)
    
    assert response.status
