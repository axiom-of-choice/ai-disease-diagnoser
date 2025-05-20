from pydantic import BaseModel
from typing import List

class Patient(BaseModel):
    name: str
    age: int
    id: str

class MedicalInput(BaseModel):
    patient: Patient
    symptoms: List[str]
    reason_for_visit: str

class AudioTranscriptionInput(BaseModel):
    audio_url: str
    
class AudioTranscriptionOutput(BaseModel):
    text: str

class DiagnosisOutput(BaseModel):
    diagnostico: str
    tratamiento: str
    recomendaciones: str