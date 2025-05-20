
from common.schemas import ValidExtensions, AudioTranscriptionOutput
from common.openai_client import client
from config import setup_logger
import functions_framework
from typing import Dict

logger = setup_logger(__name__)


@functions_framework.http
def transcribe_audio(filepath: str) -> Dict[str, str]:
    """
    Transcribe audio file to text using OpenAI's Whisper model.
    """
    logger.info(f"Reading audio file from: {filepath}")
    with open(filepath, "rb") as audio_file:
        logger.info("Transcribing audio...")
        try:
            response = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file
            )
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return {"error": str(e)}
        
    logger.info(f"Transcription response: {response}")
    response = AudioTranscriptionOutput.model_validate(response.model_dump())
    return response.model_dump()

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