from functools import wraps
from flask import request, jsonify
from pydantic import ValidationError, BaseModel
import time

def validate_model(model: BaseModel):
    """
    Decorator to validate JSON input against a Pydantic model.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validated_input = model.model_validate(request.json)
                return func(validated_input)
            except ValidationError as e:
                raise e
        return wrapper
    return decorator

def track_metrics(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        duration = time.time() - start
        print(f"[{func.__name__}] Tiempo: {duration:.2f}s")
        return response
    return wrapper

