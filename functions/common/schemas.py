from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import enum

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    id: Optional[str]

class MedicalInput(BaseModel):
    patient: Patient
    symptoms: List[str]
    reason_for_visit: str

class AudioTranscriptionInput(BaseModel):
    audio_url: str
    
class AudioTranscriptionOutput(BaseModel):
    text: str

class DiagnosisOutput(BaseModel):
    diagnostic: str
    treatment: str
    recommendations: str
    
class Response(BaseModel):
    status: str
    transcribed_text: Optional[str] = None
    extracted_info: Optional[Dict[str, Any]] = None
    diagnosis_report: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
class ValidExtensions(enum.Enum):
    mp3 = "mp3"
    mp4 = "mp4"
    mpeg = "mpeg"
    mpga = "mpga"
    wav = "wav"
    webm = "webm"