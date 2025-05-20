from pydantic import BaseModel
from typing import List

class Patient(BaseModel):
    name: str
    age: int
    id: str

class MedicalInput(BaseModel):
    patient: Patient
    symptoms: List[str]
    reasonForVisit: str
