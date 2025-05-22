from typing import List, Dict, Any
from requests.models import Response
from common.config import setup_logger
from common.schemas import DiagnosisResponse, ErrorResponse
from common.exceptions import InvalidInputError, InvalidOutputError

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
            return_value = handle_internal_server_error_response(response_modeled)
        case _:
            # Other errors
            logger.error(f"Unexpected error: {status_code}")
            return_value = handle_unexpected_error_response(response_modeled)
    
    return return_value
    
def handle_success_response(response: DiagnosisResponse) -> str:
    """
    Handle the success response from the transcription function.
    """
    text_combined = f"""
    Hello! {response.extracted_info.get("patient").get("name")}, I am the AI medic assistant. \n
    Based on the information you provided, I have generated a report. \n
    Patient information: \n
    Name: {response.extracted_info.get("patient").get("name")} \n
    Age: {response.extracted_info.get("patient").get("age")} \n
    Gender: {response.extracted_info.get("patient").get("gender")} \n
    Symptoms: {response.extracted_info.get("symptoms")} \n
    Diagnosis: {response.extracted_info.get("diagnosis")} \n
    Treatment: {response.extracted_info.get("treatment")} \n
    Recommendations: {response.extracted_info.get("recommendations")} \n
    """
    return text_combined
    
def handle_bad_request_response(response: DiagnosisResponse) -> str:
    """
    Handle the bad request response from the transcription function.
    """
    error_message = response.error.message + "\n in Function: " + response.error.function
    logger.error(f"Error message: {error_message}")
    logger.error(f"Function name: {response.error.function}")
    logger.error(f"Error details: {response.error.details}")
    
    
    match error_message:
        case InvalidInputError.__name__ | InvalidOutputError.__name__:
            error_message = error_message + "\n" + extract_missing_pydantic_fields(response.error)
        case _:
            logger.error("Unexpected error: No missing fields found.")
            error_message = error_message + "\n Details: \n" + str(response.error.details)
    return f"Error: {error_message}"
    
def extract_missing_pydantic_fields(response: ErrorResponse) -> str:
    """
    Extract and format missing/invalid fields from the Pydantic error details.
    Returns a user-friendly string.
    """
    error_details = response.details
    if not error_details or not isinstance(error_details, list):
        return "No missing or invalid fields found."
    missing_fields = []
    for field in error_details:
        if isinstance(field, dict):
            field_path = ".".join(str(part) for part in field.get("loc", []))
            field_message = field.get("msg", "")
            missing_fields.append(f"- {field_path}: {field_message}")
        else:
            missing_fields.append(str(field))
    return "Missing or invalid fields:\n" + "\n".join(missing_fields)    

def handle_internal_server_error_response(response: DiagnosisResponse) -> str:
    """
    Handle the internal server error response from the transcription function.
    """
    error = response.error
    error_message = error.message + "\n in Function: " + error.function + "\n Details: \n" + str(error.details)
    logger.error(f"Error message: {error_message}")
    return error_message

def handle_unexpected_error_response(response: DiagnosisResponse) -> str:
    """
    Handle the unexpected error response from the transcription function.
    """
    error = response.error
    error_message = error.message + "\n in Function: " + error.function + "\n Details: \n" + str(error.details)
    logger.error(f"Error message: {error_message}")
    return error_message