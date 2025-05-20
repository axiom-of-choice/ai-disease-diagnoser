from functools import wraps
from flask import request, jsonify
from pydantic import ValidationError
import time

def validate_json(model):
    """
    Decorator to validate incoming JSON against a Pydantic model.
    Pass the Pydantic model class as the argument.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400
            try:
                validated = model(**data)
            except ValidationError as e:
                return jsonify({"error": e.errors()}), 400
            # Pass the validated model instance to the route handler
            return func(validated, *args, **kwargs)
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

