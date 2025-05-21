from flask import Flask, request, jsonify
from transcriber import transcribe
from extractor import extract
from diagnoser import diagnose
from common.decorators import validate_input, track_metrics
from common.schemas import AudioTranscriptionInput, MedicalInput
from pydantic import ValidationError
from config import setup_logger

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