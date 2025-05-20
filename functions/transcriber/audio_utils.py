
from common.schemas import AudioTranscriptionOutput
from common.openai_client import client

def transcribe_audio(filepath: str) -> AudioTranscriptionOutput:
    """
    Transcribe audio file to text using OpenAI's Whisper model.
    """
    with open(filepath, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file
        )
        
    text_response = AudioTranscriptionOutput(**response).text
    return text_response