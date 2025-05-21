from .audio_utils import transcribe_audio, get_file_extension, validate_extension
from config import setup_logger, TMP_FOLDER
import functions_framework
from common.schemas import AudioTranscriptionInput, AudioTranscriptionOutput
from common.decorators import validate_input, validate_output
from common.utils import write_file, generate_uuid
import requests
from typing import Dict



logger = setup_logger(__name__)

@functions_framework.http
@validate_output(AudioTranscriptionOutput)
@validate_input(AudioTranscriptionInput)
def transcribe(request: AudioTranscriptionInput) -> Dict[str, str]:
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
