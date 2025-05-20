import pytest
from pydantic import ValidationError
from common.schemas import MedicalInput, Patient

def test_medical_input_valid():
    data = {
        "patient": {"name": "Luis", "age": 30, "id": "001"},
        "symptoms": ["tos", "fiebre"],
        "reasonForVisit": "resfriado común"
    }
    model = MedicalInput(**data)
    assert model.patient.name == "Luis"
    assert len(model.symptoms) == 2

def test_medical_input_invalid_age():
    with pytest.raises(ValidationError):
        MedicalInput(
            patient={"name": "Luis", "age": "treinta", "id": "001"},
            symptoms=["tos"],
            reasonForVisit="control"
        )
