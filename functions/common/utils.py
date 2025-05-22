import uuid
from common.schemas import ValidExtensions, ErrorResponse, Response
import traceback
import json
from firebase_functions import https_fn

from config import setup_logger

logger = setup_logger(__name__)

def normalize_text(text: str) -> str:
    return text.strip().lower()

def write_file(file_path: str, content: bytes) -> None:
    with open(file_path, "wb") as file:
        try:
            file.write(content)
        except Exception as e:
            raise IOError(f"Error writing to file {file_path}: {e}")

def read_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        try:
            return file.read()
        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {e}")
        
def generate_uuid() -> str:
    return str(uuid.uuid4())

def load_prompt(path: str, texto_clinico: str, replace_text: str) -> str:
    """
    Carga el prompt desde un archivo de texto y reemplaza el marcador con el texto clínico.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            prompt_base = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return prompt_base.replace(replace_text, texto_clinico)


def validate_extension(extension: str) -> bool:
    """
    Validate the audio file extension.
    """
    logger.info(f"Validating file extension: {extension}")
    if extension not in [ext.value for ext in ValidExtensions]:
        logger.error(f"Invalid file extension: {extension}")
        return False
    return True

def get_file_extension(filepath: str) -> str:
    """
    Get the file extension from the file path.
    """
    logger.info(f"Getting file extension from: {filepath}")
    try:
        ext = filepath.split("/")[-1]
    except Exception as e:
        logger.error(f"Error getting file extension: {e}")
        return None
    return ext

def get_truncated_traceback(exc, max_lines=100, max_chars=1000):
    tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    # Flatten to a single string, then split into lines
    tb_str = ''.join(tb_lines)
    tb_split = tb_str.strip().splitlines()
    # Keep only the last max_lines lines
    truncated_lines = tb_split[-max_lines:]
    truncated_tb = '\n'.join(truncated_lines)
    # If still too long, truncate characters but keep the end
    if len(truncated_tb) > max_chars:
        truncated_tb = '...\n' + truncated_tb[-max_chars:]
    return truncated_tb

def check_and_return_error(result) -> https_fn.Response:
    """
    Checks if the result is an error dict and returns an HTTP response if so.
    Returns None if no error is found.
    """
    if isinstance(result, dict) and "error" in result:
        message = result.get("error", "Unknown error")
        function = result.get("function", "Unknown function")
        details = result.get("details", "No details provided")
        error_response = ErrorResponse(
            message = message,
            function= function,
            details = details
        )
        response = Response(
            status="error",
            error=error_response
        )
        logger.error(f"Error response: {response}")
        return https_fn.Response(response.model_dump_json(), status=400, mimetype="application/json")
    return None