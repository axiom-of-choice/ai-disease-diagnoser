from typing import Optional, Dict, Any
from pydantic import BaseModel

class DiagnosisResponse(BaseModel):
    status: str
    transcribed_text: Optional[str] = None
    extracted_info: Optional[Dict[str, Any]] = None
    diagnosis_report: Optional[Dict[str, Any]] = None
    error: Optional[str] = None