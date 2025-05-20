from common.openai_client import client
from openai import OpenAI

def extract(text: str):
    """
    Extracts medical information from a given text using OpenAI's GPT-4 model.
    """
    
    # Initialize OpenAI client
    
    # Call the function to extract medical information
    extracted_info = extract_medical_info(text, client)
    
    return extracted_info


def extract_medical_info(text: str, client: OpenAI) -> dict:
    response = client.chat.completions.create(
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