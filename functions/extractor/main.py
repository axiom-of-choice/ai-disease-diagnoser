from common.openai_client import client
from common.utils import load_prompt
from config import EXTRACT_PROMPT_PATH
from common.schemas import AudioTranscriptionOutput
import functions_framework
from common.decorators import validate_model

# Configura tu clave de API desde una variable de entorno

@functions_framework.http
@validate_model(AudioTranscriptionOutput)
def extract(request: AudioTranscriptionOutput) -> str:
    """
    Usa el modelo de OpenAI para extraer datos clínicos estructurados desde texto libre.
    """
    text = request.model_dump().get("text")
    prompt = load_prompt(EXTRACT_PROMPT_PATH, text)

    response = client.chat.completions.create(
        model="gpt-4",  # Cambiar a "gpt-3.5-turbo" si se desea
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800
    )

    return response["choices"][0]["message"]["content"]

# Ejemplo de uso
if __name__ == "__main__":
    texto = """
    Paciente femenina de 34 años, identificada como Laura Medina, se presenta con dolor de cabeza constante, 
    visión borrosa y náuseas. DNI: 11223344. El motivo de la consulta es que los síntomas han empeorado en los últimos días.
    """
    resultado = extract(texto)
    print(resultado)
