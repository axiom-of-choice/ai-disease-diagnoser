import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_medical_info(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Extrae información médica del texto como JSON."},
            {"role": "user", "content": text}
        ],
        functions=[{
            "name": "extract_info",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "integer"},
                            "id": {"type": "string"}
                        },
                        "required": ["name", "age", "id"]
                    },
                    "symptoms": {"type": "array", "items": {"type": "string"}},
                    "reasonForVisit": {"type": "string"}
                },
                "required": ["patient", "symptoms", "reasonForVisit"]
            }
        }],
        function_call={"name": "extract_info"}
    )
    return response["choices"][0]["message"]["function_call"]["arguments"]

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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "diagnosis": "Posible diagnóstico de ejemplo",
        "treatment": "Tratamiento de ejemplo",
        "recommendations": "Recomendaciones de ejemplo"
    }
