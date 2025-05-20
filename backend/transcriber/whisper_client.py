import requests
import tempfile
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_url: str, model: str = "whisper-1", language: str = "es") -> str:
    """
    Descarga un archivo de audio desde una URL y lo transcribe usando OpenAI Whisper API.
    """
    # Descarga el archivo temporalmente
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp_file:
        response = requests.get(audio_url)
        if response.status_code != 200:
            raise Exception("No se pudo descargar el archivo de audio")

        tmp_file.write(response.content)
        tmp_file.flush()

        # Envía a OpenAI Whisper
        with open(tmp_file.name, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                file=audio_file,
                model=model,
                language=language
            )
            return transcript["text"]
