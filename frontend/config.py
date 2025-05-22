import logging
import dotenv
import os

# Load environment variables from .env file
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
if not ENDPOINT_URL:
    # Fallback para desarrollo local si usas .env
    dotenv.load_dotenv()
    ENDPOINT_URL = os.getenv("ENDPOINT_URL")
if not ENDPOINT_URL:
    raise ValueError("ENDPOINT_URL not found. Please set it as an environment variable or via Firebase functions:config:set")


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