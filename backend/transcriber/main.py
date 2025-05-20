from fastapi import FastAPI, Request
import requests
from whisper_client import transcribe_audio


app = FastAPI()

@app.post("/transcribe")
async def transcribe(req: Request):
    data = await req.json()
    audio_url = data["audio_url"]
    text = transcribe_audio(audio_url)
    return {"transcription": text}
