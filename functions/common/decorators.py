from functools import wraps
from flask import jsonify
from pydantic import ValidationError, BaseModel
import time
from .exceptions import InvalidInputError, InvalidOutputError
from config import setup_logger

logger = setup_logger(__name__)

def validate_input(model: BaseModel):
    """
    Decorator to validate input against a Pydantic model.
    Returns a dict with error details on validation failure.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(arg, *args, **kwargs):
            try:
                logger.info(f"Validating input with model: {model.__name__}")
                validated_input: BaseModel = model.model_validate(arg)
            except (InvalidInputError, ValidationError) as e:
                logger.error(f"Invalid input: {e.errors() if hasattr(e, 'errors') else str(e)}")
                return {
                    "error": "Invalid input",
                    "function": func.__name__,
                    "details": e.errors() if hasattr(e, 'errors') else str(e)
                }
            return func(validated_input, *args, **kwargs)
        return wrapper
    return decorator

def validate_output(model: BaseModel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Validating output with model: {model.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Function result: {result}")
            if isinstance(result, tuple):
                return result
            try:
                validated: BaseModel = model(**result)
                return validated.model_dump()
            except (InvalidOutputError, ValidationError) as e:
                logger.error(f"Invalid output: {e.errors() if hasattr(e, 'errors') else str(e)}")
                return {
                    "error": "Invalid output",
                    "function": func.__name__,
                    "details": e.errors() if hasattr(e, 'errors') else str(e)
                }
        return wrapper
    return decorator

def track_metrics(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = setup_logger(func.__module__)
        start = time.time()
        logger.info(f"Started {func.__name__}")
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"Finished {func.__name__} in {duration:.3f}s")
        return result
    return wrapper

