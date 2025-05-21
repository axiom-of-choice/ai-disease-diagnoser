from typing import List, Dict, Any
from requests.models import Response
from common.config import setup_logger
from common.schemas import DiagnosisResponse

# Configuración del logger
logger = setup_logger(__name__)


def handle_diagnostic_response(diagnostic_response: Response) -> str:
    """
    Handle the response from the diagnostic function.
    """
    status_code = diagnostic_response.status_code
    response_modeled = DiagnosisResponse(**diagnostic_response.json())
    logger.info(f"Response status code: {status_code}")
    logger.info(f"Response content: {response_modeled}")
    return_value = None
    match status_code:
        case 200:
            return_value = handle_success_response(response_modeled)
        case 400:
            # Bad request
            logger.error("Bad request: Invalid input data.")
            return_value = handle_bad_request_response(response_modeled)
            
        case 500:
            # Internal server error
            logger.error("Internal server error: Something went wrong.")
            return_value = handle_internal_server_error_response()
        case _:
            # Other errors
            logger.error(f"Unexpected error: {status_code}")
            return_value = handle_unexpected_error_response()
    
    return return_value
    
def handle_success_response(response: DiagnosisResponse) -> str:
    """
    Handle the success response from the transcription function.
    """
    text_combined = f"""
    Diagnostico: {response.diagnosis_report.get("diagnostic")}
    Tratamiento: {response.diagnosis_report.get("treatment")}
    Recomendaciones: {response.diagnosis_report.get("recommendations")}
    """
    return text_combined
    
def handle_bad_request_response(response: DiagnosisResponse) -> str:
    """
    Handle the bad request response from the transcription function.
    """
    return extract_missing_pydantic_fields(response)
    
def extract_missing_pydantic_fields(response: DiagnosisResponse) -> Dict[str, Any]:
    """
    Extract missing fields from the Pydantic model.
    """
    missing_fields = []
    logger.info(f"Missing fields in response: {response}")
    logger.info(f"Model fields in response: {response.model_fields_set}")
    logger.info(f"Model fields in response: {response.model_dump()}")
    for field in response.model_fields_set:
        if field not in response.model_dump():
            missing_fields.append(field)
            
    text_combined = f"""
    La respuesta no pudo ser procesada porque faltan los siguientes campos:
    {missing_fields}
    """
    return text_combined

def handle_internal_server_error_response() -> str:
    """
    Handle the internal server error response from the transcription function.
    """
    return "Error: Something went wrong. See logs for details."

def handle_unexpected_error_response() -> str:
    """
    Handle the unexpected error response from the transcription function.
    """
    return "Error: Unexpected error. See logs for details."