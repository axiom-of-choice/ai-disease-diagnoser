import streamlit as st
import requests

st.title("Procesamiento Médico Inteligente")

option = st.radio("Selecciona una entrada:", ("Link de audio", "Texto libre"))

if option == "Link de audio":
    audio_url = st.text_input("Pega el enlace del audio")
    if st.button("Procesar audio"):
        response = requests.post("https://REGION-PROJECT.cloudfunctions.net/process_audio", json={"audio_url": audio_url})
        st.json(response.json())

else:
    texto_libre = st.text_area("Escribe el texto del paciente")
    if st.button("Procesar texto"):
        response = requests.post("https://REGION-PROJECT.cloudfunctions.net/process_text", json={"text": texto_libre})
        st.json(response.json())