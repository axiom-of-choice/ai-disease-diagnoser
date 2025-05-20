import streamlit as st
import requests

TRANSCRIBE_URL = "https://<transcribe-url>/transcribe"
EXTRACT_URL = "https://<extract-url>/extract"
DIAGNOSE_URL = "https://<diagnose-url>/diagnose"

st.title("Asistente Médico AI")

text_input = st.text_area("Texto clínico o motivo de consulta")
audio_url = st.text_input("URL de audio (opcional)")

if st.button("Procesar"):
    if audio_url:
        with st.spinner("Transcribiendo audio..."):
            response = requests.post(TRANSCRIBE_URL, json={"audio_url": audio_url})
            text_input = response.json()["transcription"]

    with st.spinner("Extrayendo información médica..."):
        r2 = requests.post(EXTRACT_URL, json={"text": text_input})
        structured = r2.json()

    with st.spinner("Generando diagnóstico..."):
        r3 = requests.post(DIAGNOSE_URL, json=structured)
        result = r3.json()

    st.subheader("Datos del Paciente")
    st.json(structured)

    st.subheader("Diagnóstico")
    st.write(result.get("diagnosis", "No disponible"))

    st.subheader("Tratamiento")
    st.write(result.get("treatment", "No disponible"))

    st.subheader("Recomendaciones")
    st.write(result.get("recommendations", "No disponible"))
