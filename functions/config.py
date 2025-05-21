import os
import logging
import sys
from dotenv import load_dotenv


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Fallback para desarrollo local si usas .env
    from dotenv import load_dotenv
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Please set it as an environment variable or via Firebase functions:config:set")

TMP_FOLDER = "/tmp/"
EXTRACT_PROMPT_PATH = "extractor/prompt.txt"
TEXTO_CLINICO = "TEXTO_CLINICO"
MEDICAL_INPUT = "MEDICAL_INPUT"
DIAGNOSIS_PROMPT_PATH = "diagnoser/prompt.txt"
GPT_MODEL = "gpt-3.5-turbo-1106"
TRANSCRIBE_MODEL = "gpt-4o-transcribe"

def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(name)s:%(filename)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


