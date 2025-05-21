import os
import logging
import sys

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TMP_FOLDER = "/tmp/"
EXTRACT_PROMPT_PATH = "extractor/prompt.txt"
TEXTO_CLINICO = "TEXTO_CLINICO"
MEDICAL_INPUT = "MEDICAL_INPUT"
DIAGNOSIS_PROMPT_PATH = "diagnoser/prompt.txt"

def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


