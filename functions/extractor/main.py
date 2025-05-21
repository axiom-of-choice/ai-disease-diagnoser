from common.openai_client import client
from common.utils import load_prompt
from config import EXTRACT_PROMPT_PATH, TEXTO_CLINICO, setup_logger, GPT_MODEL
from common.schemas import AudioTranscriptionOutput, MedicalInput
import functions_framework
from common.decorators import validate_input, validate_output
import json

logger = setup_logger(__name__)

@functions_framework.http
@validate_input(AudioTranscriptionOutput)
@validate_output(MedicalInput)
def extract(request: AudioTranscriptionOutput) -> MedicalInput:
    """
    Usa el modelo de OpenAI para extraer datos clínicos estructurados desde texto libre.
    """
    text = request.model_dump().get("text")
    logger.info(f"Texto recibido: {text}")
    prompt = load_prompt(EXTRACT_PROMPT_PATH, text, TEXTO_CLINICO)
    logger.info(f"Prompt: {prompt}")
    logger.info("Llamando a OpenAI para la extracción de datos clínicos...")
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=800
        )
    except Exception as e:
        raise Exception(f"Error al llamar a OpenAI: {e}")
    
    logger.debug("response")
    logger.debug(response.choices[0].message.content)
    try:
        response = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar la respuesta JSON: {e}")
        raise ValueError(f"Error al decodificar la respuesta JSON: {e}")

    return response