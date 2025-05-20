import requests
import whisper

def transcribe_audio(audio_url: str) -> str:
    response = requests.get(audio_url)
    with open("/tmp/audio.mp3", "wb") as f:
        f.write(response.content)

    model = whisper.load_model("base")
    result = model.transcribe("/tmp/audio.mp3")
    return result["text"]
