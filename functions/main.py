from flask import Flask, request, jsonify
from transcriber import transcribe
from extractor import extract
from diagnoser import diagnose
from common.decorators import validate_json, track_metrics
from common.schemas import *

app = Flask(__name__)

@app.route("/transcribe", methods=["POST"])
@validate_json(AudioTranscriptionInput)
@track_metrics
def transcribe(validated_input: AudioTranscriptionInput):
    text = transcribe(validated_input.audio_url)
    return jsonify({"transcription": text})

@app.route("/extract", methods=["POST"])
@validate_json(["text"])
@track_metrics
def extract():
    data = request.get_json()
    info = extract(data["text"])
    return jsonify(info.dict())

@app.route("/diagnose", methods=["POST"])
@validate_json(["sintomas", "paciente", "motivo_consulta"])
@track_metrics
def diagnose():
    data = request.get_json()
    diagnosis = diagnose(data)
    return jsonify({"diagnosis": diagnosis})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the doctor API!"}), 200

# Cloud Function entrypoint

def api(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()