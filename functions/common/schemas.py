from pydantic import BaseModel
from typing import List, Optional
import enum

class Patient(BaseModel):
    name: str
    age: Optional[int]
    id: Optional[str]
    gender: Optional[str]

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
    
class ValidExtensions(enum.Enum):
    mp3 = "mp3"
    mp4 = "mp4"
    mpeg = "mpeg"
    mpga = "mpga"
    wav = "wav"
    webm = "webm"