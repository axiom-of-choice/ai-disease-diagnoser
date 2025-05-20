import streamlit as st
import requests

API_BASE = "https://<TUSERVICIO>.cloudfunctions.net/api"

st.set_page_config(page_title="Procesador Médico", layout="centered")

st.title("🩺 Procesamiento Médico con LLMs")

with st.form("input_form"):
    st.subheader("1. Ingresa datos")
    audio_url = st.text_input("🔗 URL del audio")
    texto_manual = st.text_area("📝 O escribe texto manualmente")

    submitted = st.form_submit_button("Procesar")

if submitted:
    if audio_url:
        with st.spinner("🔄 Transcribiendo audio..."):
            response = requests.post(f"{API_BASE}/transcribe", json={"audio_url": audio_url})
            if response.ok:
                transcripcion = response.json()["transcription"]
                st.success("✅ Transcripción completada")
                st.text_area("🗒 Transcripción", transcripcion, height=150)
            else:
                st.error("❌ Error al transcribir audio")
                st.stop()
    else:
        transcripcion = texto_manual

    with st.spinner("📋 Extrayendo información médica..."):
        response = requests.post(f"{API_BASE}/extract", json={"text": transcripcion})
        if response.ok:
            data = response.json()
            st.success("✅ Información médica extraída")

            st.json(data)
        else:
            st.error("❌ Error al extraer información médica")
            st.stop()

    with st.spinner("💡 Generando diagnóstico..."):
        response = requests.post(f"{API_BASE}/diagnose", json=data)
        if response.ok:
            diagnostico = response.json()["diagnosis"]
            st.success("✅ Diagnóstico generado")
            st.markdown("### 🧾 Diagnóstico y Recomendaciones")
            st.write(diagnostico)
        else:
            st.error("❌ Error al generar diagnóstico")
