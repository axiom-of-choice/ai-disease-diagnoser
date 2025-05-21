from typing import Optional, Dict, Any
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    function: Optional[str] = None
    details: Optional[Any] = None

class DiagnosisResponse(BaseModel):
    status: str
    transcribed_text: Optional[str] = None
    extracted_info: Optional[Dict[str, Any]] = None
    diagnosis_report: Optional[Dict[str, Any]] = None
    error: Optional[ErrorResponse] = None