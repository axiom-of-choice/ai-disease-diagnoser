from common.openai_client import client
from common.utils import load_prompt
from config import EXTRACT_PROMPT_PATH, TEXTO_CLINICO, setup_logger
from common.schemas import AudioTranscriptionOutput, MedicalInput
import functions_framework
from common.decorators import validate_input

logger = setup_logger(__name__)

@functions_framework.http
@validate_input(AudioTranscriptionOutput)
def extract(request: AudioTranscriptionOutput) -> MedicalInput:
    """
    Usa el modelo de OpenAI para extraer datos clínicos estructurados desde texto libre.
    """
    text = request.model_dump().get("text")
    logger.info(f"Texto recibido: {text}")
    prompt = load_prompt(EXTRACT_PROMPT_PATH, text, TEXTO_CLINICO)
    logger.info(f"Prompt: {prompt}")
    logger.info("Llamando a OpenAI para la extracción de datos clínicos...")
    response = client.chat.completions.create(
        model="gpt-4",  # Cambiar a "gpt-3.5-turbo" si se desea
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800
    )
    logger.debug(f"Response")
    logger.info(response.choices[0].message.content)
    

    return 

# Ejemplo de uso
if __name__ == "__main__":
    texto = """
    Paciente femenina de 34 años, identificada como Laura Medina, se presenta con dolor de cabeza constante, 
    visión borrosa y náuseas. DNI: 11223344. El motivo de la consulta es que los síntomas han empeorado en los últimos días.
    """
    resultado = extract(texto)
    print(resultado)
