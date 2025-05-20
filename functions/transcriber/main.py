from .audio_utils import transcribe_audio, get_file_extension, validate_extension
from config import setup_logger, TMP_FOLDER
import functions_framework
from common.schemas import AudioTranscriptionInput
from common.decorators import validate_model
from common.utils import write_file, generate_uuid
import requests



logger = setup_logger(__name__)

@functions_framework.http
@validate_model(AudioTranscriptionInput)
def transcribe(request: AudioTranscriptionInput) -> str:
    audio_url = request.model_dump().get("audio_url")
    response = requests.get(audio_url)
    if response.status_code != 200:
        logger.error(f"Failed to download audio file: {response.status_code}")
        return "Failed to download audio file", 400
    
    logger.info(f"Downloaded audio file from URL: {audio_url}")
    extension = get_file_extension(response.headers.get("Content-Type"))
    logger.info(f"File extension determined: {extension}")
    if not extension:
        logger.error("Could not determine file extension from Content-Type header")
        return "Could not determine file extension", 400
    if not validate_extension(extension):
        return "Invalid file extension", 400
    logger.info(f"Transcribing audio from URL: {audio_url}")
    filename = generate_uuid()
    file_path = f"{TMP_FOLDER}{filename}.{extension}"
    write_file(file_path, response.content)
    logger.info("Transcribing audio...")
    result = transcribe_audio(file_path)
    return result
