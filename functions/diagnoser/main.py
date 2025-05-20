from fastapi import FastAPI, Request
from common.openai_client import client
from common.schemas import DiagnosisOutput


def diagnose(req: Request):
    """
    Diagnoses a patient based on the provided symptoms, patient information, and reason for visit.
    """
    data = req.json()
    info = {
        "patient": {
            "name": data["paciente"]["nombre"],
            "age": data["paciente"]["edad"],
            "id": data["paciente"]["id"]
        },
        "symptoms": data["sintomas"],
        "reasonForVisit": data["motivo_consulta"]
    }

    diagnosis = generate_diagnosis(info)
    return DiagnosisOutput(**diagnosis)


def generate_diagnosis(info):
    prompt = f"""
Paciente: {info['patient']}
Síntomas: {info['symptoms']}
Motivo de consulta: {info['reasonForVisit']}

Genera:
- Diagnóstico
- Tratamiento
- Recomendaciones
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "diagnosis": "Posible diagnóstico de ejemplo",
        "treatment": "Tratamiento de ejemplo",
        "recommendations": "Recomendaciones de ejemplo"
    }