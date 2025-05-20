import time
import json
from functools import wraps
from flask import Request, make_response

def with_logging_and_validation(func):
    @wraps(func)
    def wrapper(request: Request):
        start = time.time()
        try:
            data = request.get_json(force=True)
            if not data:
                return make_response({"error": "Invalid JSON"}, 400)
            response = func(data)
            latency = time.time() - start
            return make_response(json.dumps({
                "result": response,
                "latency": latency
            }), 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)
    return wrapper
