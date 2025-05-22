import streamlit as st
import requests
from common.config import setup_logger
from common.response_adapters import handle_diagnostic_response

# Configuración del logger
logger = setup_logger(__name__)


st.title("Procesamiento Médico Inteligente")

option = st.radio("Selecciona una entrada:", ("Link de audio", "Texto libre"))

if option == "Link de audio":
    audio_url = st.text_input("Pega el enlace del audio")
    logger.info(f"Audio URL: {audio_url}")
    if st.button("Procesar audio"):
        try:
            with st.spinner("Procesando...", show_time=True):
                response = requests.post("http://127.0.0.1:5001/ai-diagnoser/us-central1/process_medical_data", json={"audio_url": audio_url})
                logger.info(f"Response: {response.json()}")
                result = handle_diagnostic_response(response)
            if response.status_code != 200:
                st.error(f"Error al procesar el audio: {response.status_code}")
                st.error(result)
                st.stop()
            st.success("Audio procesado con éxito")
            st.text(result)
        except requests.exceptions.RequestException as e:
            st.error(f"Error al procesar el audio: {e}")
            st.text(result)
            logger.error(f"Error al procesar el audio: {e}")
            st.stop()
else:
    texto_libre = st.text_area("Escribe el texto del paciente")
    if st.button("Procesar texto"):
        logger.info(f"Texto libre: {texto_libre}")
        try:
            with st.spinner("Procesando..."):
                response = requests.post("http://127.0.0.1:5001/ai-diagnoser/us-central1/process_medical_data", json={"text_input": texto_libre})
                logger.info(f"Response: {response.json()}")
                result = handle_diagnostic_response(response)
            if response.status_code != 200:
                st.error(f"Error al procesar el texto: {response.status_code}")
                st.text(result)
                st.stop()
            st.success("Texto procesado con éxito")
            st.text(result)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al procesar el texto: {e}")
            st.text(result)
            st.stop()
