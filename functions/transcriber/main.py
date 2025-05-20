import requests
from .audio_utils import transcribe_audio

def transcribe(audio_url: str) -> str:
    response = requests.get(audio_url)
    with open("/tmp/audio.mp3", "wb") as f:
        f.write(response.content)

    result = transcribe_audio("/tmp/audio.mp3")
    return result
