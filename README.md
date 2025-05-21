# Descripcion del proyecto

Este proyecto permite a un usuario ingresar un enlace de audio o escribir texto libre con información médica. Luego, utiliza funciones serverless en Google Cloud para transcripción, extracción estructurada de datos médicos y generación de diagnóstico, todo con una interfaz web simple en Streamlit.

---

# 🔧 Requisitos

- Python 3.10 o superior
- Cuenta de Google Cloud con `gcloud` CLI instalado y configurado
- API Key de OpenAI
- Opcional: cuenta de Whisper API o Google Speech-to-Text

---

# 📁 Estructura del Proyecto





---

# ⚙️ Configuración y Despliegue

## 1. Autenticarse con Google Cloud

```
gcloud auth login
gcloud config set project TU_ID_DEL_PROYECTO
```

## 2. Configurar API Key de OpenAI

Agrega tu clave en extract_medical_info/main.py y generate_diagnosis/main.py:
openai.api_key = "TU_API_KEY"

## 3. Desplegar las Cloud Functions

### Función 1: Transcripción
```
cd transcribe_audio
gcloud functions deploy transcribe_audio \\
  --runtime python311 \\
  --trigger-http \\
  --allow-unauthenticated \\
  --region us-central1
```

### Función 2: Extracción médica
```
cd extract_medical_info
gcloud functions deploy extract_medical_info \\
  --runtime python311 \\
  --trigger-http \\
  --allow-unauthenticated \\
  --region us-central1
```

### Función 3: Generación de diagnóstico
```
cd generate_diagnosis
gcloud functions deploy generate_diagnosis \\
  --runtime python311 \\
  --trigger-http \\
  --allow-unauthenticated \\
  --region us-central1
```

## 4. Ejecutar la interfaz Streamlit
```
cd medic_app/frontend
pip install streamlit requests
streamlit run streamlit_app.py
```

# 🧪 Ejemplo de uso

## Entrada (en frontend):
* Opción 1: https://mis-audios.com/audio_paciente_1.mp3
* Opción 2: Texto: "Me llamo Juan Pérez, tengo 45 años, siento dolor en el pecho desde hace dos días..."



## Salida
```
{
  "data": {
    "resultado": "Diagnóstico: Angina de pecho... Tratamiento: Reposo, nitroglicerina... Recomendaciones: Evitar esfuerzos..."
}
```



                                      ┌─────────────┐
                                      │  Usuario    │
                                      └────┬────────┘
                                           │
                          ┌────────────────┴───────────────┐
                          │           Web App              │
                          │  (React, Streamlit, etc.)      │
                          └────────────────┬───────────────┘
                                           │
                      ┌────────────────────┼────────────────────────┐
                      ▼                    ▼                        ▼
       [Audio URL o Texto]        [Ver resultados]       [Mostrar errores/logs]
                                           │
                                ┌──────────▼────────────┐
                                │   Firebase Functions  │
                                │       (Python)        │
                                └──────────┬────────────┘
                                           ▼
    ┌─────────────┐ ┌──────────────────────┐ ┌────────────────────────┐
    │ Transcribe  │→│ Extraer Información  │→│ Generar Diagnóstico     │
    └─────────────┘ └──────────────────────┘ └────────────────────────┘
        (Whisper)        (OpenAI / Gemini)         (OpenAI / Gemini)
                               │                          │
                     ┌────────▼────────┐       ┌──────────▼────────────┐
                     │   JSON Schema   │       │ Texto estructurado    │
                     └─────────────────┘       └───────────────────────┘


