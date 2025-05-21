# generate_diagnosis.py
import functions_framework
from common.openai_client import client
from common.decorators import validate_input, validate_output
from common.utils import load_prompt
from common.schemas import MedicalInput, DiagnosisOutput
from config import DIAGNOSIS_PROMPT_PATH, setup_logger, MEDICAL_INPUT, GPT_MODEL
import json
from common.exceptions import OpenAIError, JsonDecodeError


logger = setup_logger(__name__)


@functions_framework.http
@validate_output(DiagnosisOutput)
@validate_input(MedicalInput)
def diagnose(request: MedicalInput) -> str:
    logger.info("Diagnosing...")
    logger.debug(request)
    # Convertir el input a un string
    medical_info = info_parser(request)
    logger.info(f"Información médica: {medical_info}")
    
    if not isinstance(medical_info, str):
        return {"error": "Invalid input format"}
    
    prompt = load_prompt(DIAGNOSIS_PROMPT_PATH, medical_info, MEDICAL_INPUT)

    logger.info("Llamando a OpenAI para el diagnóstico...")
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
    except Exception as e:
        logger.error(f"Error al llamar a OpenAI: {e}")
        return {
            "error": OpenAIError.__name__,
            "function": diagnose.__name__,
            "details": str(e)
        }
    logger.debug("response")
    logger.debug(response.choices[0].message.content)
    logger.info("Diagnóstico generado")
    try:
        response = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar la respuesta JSON: {e}")
        return {
            "error": JsonDecodeError.__name__,
            "function": diagnose.__name__,
            "details": str(e)
        }
    return response
    

def info_parser(info: MedicalInput) -> str:
    """
    Parse the medical information from the input.
    """
    logger.info("Parsing medical information...")
    logger.debug(info)
    patient_details = info.patient
    symptoms = info.symptoms
    reason_for_visit = info.reason_for_visit
    # Convertir el input a un string
    info_str = f"""
    Paciente de {patient_details.age} años, de genero {patient_details.gender}, presenta los siguientes síntomas: {', '.join(symptoms)}.
    Motivo de la visita: {reason_for_visit}.
    """
    return info_str