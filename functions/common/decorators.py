from functools import wraps
from flask import request, jsonify
from pydantic import ValidationError, BaseModel
import time

def validate_input(model: BaseModel):
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
                return jsonify({"error": "Invalid input", "details": e.errors()}), 400
        return wrapper
    return decorator

def validate_output(model: BaseModel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                # Validate the response using a Pydantic model
                validated: BaseModel = model(**result)
                return validated.model_dump()
            except Exception as e:
                # Handle invalid response
                return jsonify({"error": "Invalid output", "details": str(e)}), 500
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

