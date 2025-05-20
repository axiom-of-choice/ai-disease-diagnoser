from flask import Request
from common.decorators import with_logging_and_validation
from transcriber.transcribe import transcribe_audio
from extracter.exctraction import extract_info
from diagnoser.generator import generate_diagnosis

@with_logging_and_validation
def transcribe(request: Request):
    return transcribe_audio(request["audio_url"])

@with_logging_and_validation
def extract(request: Request):
    return extract_info(request["text"])

@with_logging_and_validation
def diagnose(request: Request):
    return generate_diagnosis(request)
