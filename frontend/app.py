import streamlit as st
import requests
from common.config import setup_logger
from common.response_adapters import handle_diagnostic_response

# Configuración del logger
logger = setup_logger(__name__)


st.title("AI Medic Assistant")

option = st.radio("Select an option :", ("Audio Link", "Free Text"))

if option == "Audio Link":
    audio_url = st.text_input("Paste the audio link")
    logger.info(f"Audio URL: {audio_url}")
    if st.button("Process audio"):
        try:
            with st.spinner("Processing...", show_time=True):
                response = requests.post("http://127.0.0.1:5001/ai-diagnoser/us-central1/process_medical_data", json={"audio_url": audio_url})
                logger.info(f"Response: {response.json()}")
                result = handle_diagnostic_response(response)
            if response.status_code != 200:
                st.error(f"Error processing audio: {response.status_code}")
                st.error(result)
                with st.expander("View full JSON response for advanced users"):
                    st.json(response.json())
                st.stop()
            st.success("Audio processed successfully")
            st.text(result)
            with st.expander("View full JSON response for advanced users"):
                st.json(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Error processing the audio: {e}")
            st.text(result)
            logger.error(f"Error processing the audio: {e}")
            with st.expander("View full JSON response for advanced users"):
                    st.json(response.json())
            st.stop()
else:
    texto_libre = st.text_area("Write the free text")
    if st.button("Process text"):
        logger.info(f"Free Text: {texto_libre}")
        try:
            with st.spinner("Processing...", show_time=True):
                response = requests.post("http://127.0.0.1:5001/ai-diagnoser/us-central1/process_medical_data", json={"text_input": texto_libre})
                logger.info(f"Response: {response.json()}")
                result = handle_diagnostic_response(response)
            if response.status_code != 200:
                st.error(f"Error processing text: {response.status_code}")
                st.error(result)
                with st.expander("View full JSON response for advanced users"):
                    st.json(response.json())
                st.stop()
            st.success("Text processed successfully")
            st.text(result)
            with st.expander("View full JSON response for advanced users"):
                    st.json(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Error processing text: {e}")
            st.error(result)
            with st.expander("View full JSON response for advanced users"):
                    st.json(response.json())
            st.stop()
