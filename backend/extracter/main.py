from fastapi import FastAPI, Request
from backend.common.openai_client import extract_medical_info

app = FastAPI()

@app.post("/extract")
async def extract(req: Request):
    data = await req.json()
    result = extract_medical_info(data["text"])
    return result
