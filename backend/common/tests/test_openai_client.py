import pytest
from unittest.mock import patch
from common.openai_client import extract_medical_info, generate_diagnosis

@patch("medical_ai_common.openai_client.openai.ChatCompletion.create")
def test_extract_medical_info(mock_create):
    mock_create.return_value = {
        "choices": [
            {
                "message": {
                    "function_call": {
                        "arguments": '{"patient": {"name": "Ana", "age": 25, "id": "123"}, "symptoms": ["fiebre", "dolor"], "reasonForVisit": "consulta general"}'
                    }
                }
            }
        ]
    }

    result = extract_medical_info("Paciente con fiebre y dolor abdominal")
    assert "patient" in result
    assert "symptoms" in result
    assert "reasonForVisit" in result

@patch("medical_ai_common.openai_client.openai.ChatCompletion.create")
def test_generate_diagnosis(mock_create):
    mock_create.return_value = {
        "choices": [
            {"message": {"content": "Diagnóstico simulado"}}
        ]
    }

    structured_data = {
        "patient": {"name": "Ana", "age": 25, "id": "123"},
        "symptoms": ["fiebre", "dolor"],
        "reasonForVisit": "consulta general"
    }

    result = generate_diagnosis(structured_data)
    assert isinstance(result, dict)
    assert "diagnosis" in result
    assert "treatment" in result
    assert "recommendations" in result
