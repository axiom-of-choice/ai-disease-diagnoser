from transcriber import transcribe
from extractor import extract
from diagnoser import diagnose
from common.schemas import AudioTranscriptionInput, Response, AudioTranscriptionOutput, MedicalInput, DiagnosisOutput
from common.utils import get_truncated_traceback


import json
from flask import Request
from flask_cors import CORS, cross_origin
from flask import jsonify
from firebase_functions import https_fn
from firebase_admin import initialize_app

from config import setup_logger

logger = setup_logger(__name__)

# app = Flask(__name__)
# logger = setup_logger(__name__)
# 
# @app.errorhandler(ValidationError)
# def handle_validation_error(e):
#     return jsonify({"error": e.errors()}), 400
# 
# @app.route("/transcribe", methods=["POST"])
# @track_metrics
# @validate_model(AudioTranscriptionInput)
# def transcribe_endpoint(validated_input: AudioTranscriptionInput, error: dict):
#     if error:
#         return jsonify({"error": error}), 400
#     logger.info(f"Transcribing audio from URL: {validated_input.audio_url}")
#     text = transcribe(validated_input.audio_url)
#     return jsonify({"transcription": text})
# 
# @app.route("/extract", methods=["POST"])
# @track_metrics
# @validate_model(AudioTranscriptionOutput)
# def extract_endpoint(validated_input: AudioTranscriptionOutput, error: dict):
#     if error:
#         return jsonify({"error": error}), 400
#     info = extract(validated_input.text)
#     return jsonify(info.dict())
# 
# @app.route("/diagnose", methods=["POST"])
# @track_metrics
# @validate_model(MedicalInput)
# def diagnose_endpoint(validated_input: MedicalInput, error: dict):
#     if error:
#         return jsonify({"error": error}), 400
#     diagnosis = diagnose(validated_input)
#     return jsonify({"diagnosis": diagnosis})
# 
# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({"status": "healthy"}), 200
# 
# @app.route("/", methods=["GET"])
# def index():
#     return jsonify({"message": "Welcome to the doctor API!"}), 200
# 
# # Cloud Function entrypoint
# 
# def api(request):
#     with app.request_context(request.environ):
#         return app.full_dispatch_request()



# Inicializa Firebase Admin SDK si es necesario (para interactuar con otros servicios de Firebase)
initialize_app()


# Obtiene la clave de API de OpenAI desde las variables de entorno de Firebase Functions
# Asegúrate de haberla configurado con: firebase functions:config:set openai.key="TU_API_KEY"
# Y luego, durante el despliegue, Firebase la expondrá como una variable de entorno.
# Es mejor usar un nombre de variable de entorno más estándar como OPENAI_API_KEY
# en lugar de firebase_functions.config().openai.key, lo que puede ser más complicado de acceder.

# --- Cloud Function Principal ---


## Handling errors on Json

@https_fn.on_request()
def not_found(request: Request) -> https_fn.Response:
    return https_fn.Response(
        json.dumps({"error": "Not found", "message": request.path}),
        status=404,
        mimetype="application/json"
    )

@https_fn.on_request()
@cross_origin()  # Permite solicitudes CORS desde cualquier origen (ajustar en producción)
def health(request: Request) -> https_fn.Response:
    """
    Endpoint de salud para verificar el estado de la función.
    """
    if request.method != 'GET':
        return https_fn.Response("Método no permitido", status=405)

    return https_fn.Response(json.dumps({"status": "healthy"}), status=200, mimetype="application/json")

@https_fn.on_request()
@cross_origin()  # Permite solicitudes CORS desde cualquier origen (ajustar en producción)
def transcribe_audio(request: Request) -> https_fn.Response:
    """
    Endpoint para transcribir audio a texto.
    """
    if request.method != 'POST':
        return https_fn.Response("Método no permitido", status=405)
    
    try:
        data = request.get_json(silent=True)
        if not data:
            return https_fn.Response(json.dumps({"error": "No se recibió JSON válido."}), status=400, mimetype="application/json")
        transcribed_text = transcribe(AudioTranscriptionInput(**data))
        response = AudioTranscriptionOutput(**transcribed_text).model_dump_json()
    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        return https_fn.Response(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status=500,
            mimetype="application/json"
        )
    return https_fn.Response(response, status=200, mimetype="application/json")

@https_fn.on_request()
@cross_origin()  # Permite solicitudes CORS desde cualquier origen (ajustar en producción)
def extract_medical_info(request: Request) -> https_fn.Response:
    """
    Endpoint para extraer información médica desde texto.
    """
    if request.method != 'POST':
        return https_fn.Response("Método no permitido", status=405)
    
    try:
        data = request.get_json(silent=True)
        if not data:
            return https_fn.Response(json.dumps({"error": "No se recibió JSON válido."}), status=400, mimetype="application/json")
        extracted_info = extract(AudioTranscriptionOutput(**data))
        response = json.dumps(extracted_info)
    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        return https_fn.Response(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status=500,
            mimetype="application/json"
        )
    return https_fn.Response(response, status=200, mimetype="application/json")

@https_fn.on_request()
@cross_origin()  # Permite solicitudes CORS desde cualquier origen (ajustar en producción)
def generate_diagnose(request: Request) -> https_fn.Response:
    """
    Endpoint para generar un diagnóstico médico.
    """
    if request.method != 'POST':    
        return https_fn.Response("Método no permitido", status=405)
    
    try:
        data = request.get_json(silent=True)
        if not data:
            return https_fn.Response(json.dumps({"error": "No se recibió JSON válido."}), status=400, mimetype="application/json")
        diagnosis_report = diagnose(MedicalInput(**data))
        logger.info(diagnosis_report)
        response = DiagnosisOutput(**diagnosis_report).model_dump_json()
    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        return https_fn.Response(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status=500,
            mimetype="application/json"
        )
    return https_fn.Response(response, status=200, mimetype="application/json")

@https_fn.on_request()
@cross_origin() # Permite solicitudes CORS desde cualquier origen (ajustar en producción)
def process_medical_data(request: Request) -> https_fn.Response:
    """
    Cloud Function que orquesta la transcripción, extracción y generación médica.
    """
    if request.method != 'POST':
        return https_fn.Response("Método no permitido", status=405)

    data = request.get_json(silent=True)
    if not data:
        return https_fn.Response(json.dumps({"error": "No se recibió JSON válido."}), status=400, mimetype="application/json")

    audio_url = data.get("audio_url")
    text_input = data.get("text_input")

    transcribed_text = {"text": text_input}
    status = "failed"
    try:
        if audio_url:
            transcribed_text = transcribe(AudioTranscriptionInput(audio_url=audio_url))
            text_to_process = AudioTranscriptionOutput(**transcribed_text)
        elif text_input:
            text_to_process = AudioTranscriptionOutput(text=text_input)
        else:
            return https_fn.Response(json.dumps({"error": "Debe proporcionar un 'audio_url' o 'text_input'."}), status=400, mimetype="application/json")

        # Paso 2: Extracción de información médica
        logger.info("Extrayendo información médica...")
        logger.info(f"Texto a procesar: {text_to_process}")
        extracted_info = extract(text_to_process)
        logger.info(f"Información extraída: {extracted_info}")

        # Paso 3: Generación de diagnóstico
        diagnosis_report = diagnose(MedicalInput(**extracted_info))
        status = "success"

        response_data = {
            "status": status,
            "transcribed_text": transcribed_text.get("text", ""),
            "extracted_info": extracted_info,
            "diagnosis_report": diagnosis_report
        }
        # Response model
        response = Response(**response_data).model_dump_json()
        return https_fn.Response(response, status=200, mimetype="application/json")

    except ValueError as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        error = str(e)
        response_data = {
            "status": status,
            "error": error, 
            "transcribed_text": transcribed_text.get("text", ""),
        }
        response = Response(**response_data).model_dump_json()
        return https_fn.Response(response, status=400, mimetype="application/json")
    except Exception as e:
        tb = get_truncated_traceback(e)
        logger.error(f"Error: {e}\nTraceback: {tb}")
        # Manejo de errores genérico
        error = str(e)
        response_data = {
            "status": status,
            "error": error, 
            "transcribed_text": transcribed_text.get("text", ""),
        }
        response = Response(**response_data).model_dump_json()
        return https_fn.Response(response, status=500, mimetype="application/json")
