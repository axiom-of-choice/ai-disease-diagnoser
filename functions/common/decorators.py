from functools import wraps
from flask import jsonify
from pydantic import ValidationError, BaseModel
import time
from .exceptions import InvalidInputError, InvalidOutputError
from config import setup_logger

logger = setup_logger(__name__)

def validate_input(model: BaseModel):
    """
    Decorator to validate JSON input against a Pydantic model.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(arg, *args, **kwargs):
            try:
                logger.info(f"Validating input with model: {model.__name__}")
                # For Pydantic v2, use model(**request.get_json())
                validated_input: BaseModel = model.model_validate(arg)
            except InvalidInputError as e:
                # Return error response immediately, do NOT call the function
                logger.error(f"Invalid input: {e.errors()}")
                logger.debug(f"Invalid input details: {e}")
                return jsonify({"error": "Invalid input", "details": e.errors()}), 400
            return func(validated_input)
        return wrapper
    return decorator

def validate_output(model: BaseModel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Validating output with model: {model.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Function result: {result}")
            # If the result is a tuple (response, status), just return it directly
            if isinstance(result, tuple):
                return result
            try:
                validated: BaseModel = model(**result)
                return validated.model_dump()
            except InvalidOutputError as e:
                logger.error(f"Invalid output: {e.errors()}")
                logger.debug(f"Invalid output details: {e}")
                return jsonify({"error": "Invalid output", "details": str(e)}), 500
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

