from fastapi import FastAPI, Request
from backend.common.openai_client import generate_diagnosis

app = FastAPI()

@app.post("/diagnose")
async def diagnose(req: Request):
    data = await req.json()
    result = generate_diagnosis(data)
    return result
