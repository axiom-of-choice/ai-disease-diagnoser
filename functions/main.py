from transcriber import transcribe
from extractor import extract
from diagnoser import diagnose
from common.schemas import AudioTranscriptionInput, Response, AudioTranscriptionOutput, MedicalInput, DiagnosisOutput
from common.utils import get_truncated_traceback, check_and_return_error
import json
from flask import Request
from flask_cors import CORS, cross_origin
from flask import jsonify
from firebase_functions import https_fn
from firebase_admin import initialize_app

from config import setup_logger

logger = setup_logger(__name__)


# Init Firebase Admin SDK
initialize_app()

## Handling errors on Json response

@https_fn.on_request()
def not_found(request: Request) -> https_fn.Response:
    return https_fn.Response(
        json.dumps({"error": "Not found", "message": request.path}),
        status=404,
        mimetype="application/json"
    )

@https_fn.on_request()
@cross_origin()
def health(request: Request) -> https_fn.Response:
    if request.method != 'GET':
        return https_fn.Response("Method not allowed", status=405)

    return https_fn.Response(json.dumps({"status": "healthy"}), status=200, mimetype="application/json")

# Singleton endpoint for transcribe
@https_fn.on_request()
@cross_origin()
def transcribe_audio(request: Request) -> https_fn.Response:
    if request.method != 'POST':
        # Wrap error in a Response object
        return https_fn.Response("Method not allowed", status=405)
    
    try:
        data = request.get_json(silent=True)
        if not data:
            # Wrap error in a Response object
            return https_fn.Response(json.dumps({"error": "No valid JSON was received."}), status=400, mimetype="application/json")
        transcribed_text = transcribe(AudioTranscriptionInput(**data))
        response = AudioTranscriptionOutput(**transcribed_text).model_dump_json()
    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        # Wrap error in a Response object
        return https_fn.Response(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status=500,
            mimetype="application/json"
        )
    # Wrap in a Response object
    return https_fn.Response(response, status=200, mimetype="application/json")

# Singleton endpoint for extract
@https_fn.on_request()
@cross_origin()
def extract_medical_info(request: Request) -> https_fn.Response:
    if request.method != 'POST':
        # Wrap error in a Response object
        return https_fn.Response("Method not allowed", status=405)
    
    try:
        data = request.get_json(silent=True)
        if not data:
            # Wrap error in a Response object
            return https_fn.Response(json.dumps({"error": "No valid JSON was received."}), status=400, mimetype="application/json")
        extracted_info = extract(AudioTranscriptionOutput(**data))
        response = json.dumps(extracted_info)
    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        # Wrap error in a Response object
        return https_fn.Response(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status=500,
            mimetype="application/json"
        )
    # Wrap in a Response object
    return https_fn.Response(response, status=200, mimetype="application/json")

# Singleton endpoint for diagnose
@https_fn.on_request()
@cross_origin()
def generate_diagnose(request: Request) -> https_fn.Response:
    if request.method != 'POST':
        # Wrap error in a Response object
        return https_fn.Response("Method not allowed", status=405)
    
    try:
        data = request.get_json(silent=True)
        if not data:
            # Wrap error in a Response object
            return https_fn.Response(json.dumps({"error": "No valid JSON was received."}), status=400, mimetype="application/json")
        diagnosis_report = diagnose(MedicalInput(**data))
        logger.info(diagnosis_report)
        response = DiagnosisOutput(**diagnosis_report).model_dump_json()
    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        # Wrap error in a Response object
        return https_fn.Response(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status=500,
            mimetype="application/json"
        )
    # Wrap in a Response object
    return https_fn.Response(response, status=200, mimetype="application/json")

# Orchestrator endpoint
@https_fn.on_request()
@cross_origin()
def process_medical_data(request: Request) -> https_fn.Response:
    if request.method != 'POST':
        # Wrap error in a Response object
        response = Response(
            status="error",
            error={"message": "Method not allowed"}
            ).model_dump_json()
        return https_fn.Response(response, status=405)

    data = request.get_json(silent=True)
    if not data:
        # Wrap error in a Response object
        response = Response(
            status="error",
            error={"message": "No valid JSON was received."}
            ).model_dump_json()
        return https_fn.Response(response, status=400, mimetype="application/json")

    audio_url = data.get("audio_url")
    text_input = data.get("text_input")

    transcribed_text = {"text": text_input}
    status = "failed"
    try:
        if audio_url:
            logger.info("Transcribing audio...")
            transcribed_text = transcribe(AudioTranscriptionInput(audio_url=audio_url))
            error_response = check_and_return_error(transcribed_text)
            if error_response:
                return error_response
            text_to_process = AudioTranscriptionOutput(**transcribed_text)
        elif text_input:
            text_to_process = AudioTranscriptionOutput(text=text_input)
        else:
            # Wrap error in a Response object
            response = Response(
                status="error",
                error={"message": "You must send an 'audio_url' or 'text_input' field"}
            ).model_dump_json()
            return https_fn.Response(response, status=400, mimetype="application/json")

        logger.info("Extracting medical data...")
        logger.info(f"Text to be processed: {text_to_process}")
        extracted_info = extract(text_to_process)
        logger.info(f"Info extracted: {extracted_info}")
        error_response = check_and_return_error(extracted_info)
        if error_response:
            return error_response

        # Paso 3: Generación de diagnóstico
        diagnosis_report = diagnose(MedicalInput(**extracted_info))
        error_response = check_and_return_error(diagnosis_report)
        if error_response:
            return error_response

        status = "success"

        response_data = {
            "status": status,
            "transcribed_text": transcribed_text.get("text", ""),
            "extracted_info": extracted_info,
            "diagnosis_report": diagnosis_report
        }
        response = Response(**response_data).model_dump_json()
        return https_fn.Response(response, status=200, mimetype="application/json")

    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        error = str(e)
        response_data = {
            "status": status,
            "error": {"message": error}, 
            "transcribed_text": transcribed_text.get("text", ""),
        }
        response = Response(**response_data).model_dump_json()
        return https_fn.Response(response, status=400, mimetype="application/json")
    except Exception as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        error = str(e)
        response_data = {
            "status": status,
            "error": {"message": error}, 
            "transcribed_text": transcribed_text.get("text", ""),
        }
        response = Response(**response_data).model_dump_json()
        return https_fn.Response(response, status=500, mimetype="application/json")
