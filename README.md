# Proyect description

This project enables a user to insert an audio file url or write plain text with personal information and syntomps. 
Then use Google Cloud serverless functions to perform a transcript (if needed), extract structured and relevant data about the patient and its symptoms, and perform a diagnose.

---

# 🔧 Requirements

- Python 3.11.9
- Google Cloud account with `gcloud` CLI installed and configured. Also firebase.
- Open AI API Key 
---

# 📁 Project structure

This project is basically divided into two main components that could be decoupled into microservices (primarili the frontend).
* Frontend:
It is a streamlit app that bascially offers to the user to put an audio url or plain text (audio url preferred) and serves the endpoint so when the user submits, sends the requests and shows the response, either a successsful or unsuccessful in a friendly way.
* Backend:
It is a set of modules containing all the logic and endpoints to transcribe, extract and diagnose served in a API way.

## Details about the structure:

General view of the project structure

```
/ai-disease-diagnoser
├── README.md
├── frontend
│   ├── .streamlit
│      └── config.toml       # Config of streamlit
│
│   ├── common              # Package of common modules. Can be decoupled as external library.
│     ├── __init__.py       # No description needed
│     ├── exceptions.py     # Exceptions module
│     ├── response_adapters.py # Adapters for displaying the API response in a friendly way
│     └── schemas.py        # Schemas modules for validation
│
│   ├── tests               # Tests folder
│      ├── # Left some generic ones.
│
│   ├── .dockerignore       # # No description needed
│   ├── Dockerfile          # File to build the docker image (if needed)   
│   ├── app.py              # Simple app definition
│   ├── config.py           # Basic configs
│   └── requirements.txt    # No description needed
│
├── functions               # Backend package. The name functions is needed due to firebase functions constraints.
│
│   ├── common              # Package of common modules. Can be decoupled as external library.
│     ├── __init__.py       # No description needed
│     ├── decorators.py     # Basic configs
│     ├── exceptions.py     # Exceptions module
│     ├── utils.py          # Utils
│     ├── openai_client.py  # Singleton client
│     ├── firestore_utils.py # Utils to write to firestore
│     └── schemas.py        # Schemas modules for validation
│
│   ├── diagnoser           # Module of diagnoser logic
│     ├── __init__.py       # No description needed
│     ├── main.py           # Core logic
│     └── prompt.txt        # Customizable prompt. Can be decoupled to avoid touching code when changing
│
│   ├── extractor           # Module of extractor logic
│     ├── __init__.py       # No description needed
│     ├── main.py           # Core logic
│     └── prompt.txt        # Customizable prompt. Can be decoupled to avoid touching code when changing
│
│   ├── transcriber         # Module of transciber logic
│     ├── __init__.py       # No description needed
│     └── main.py           # Core logic
│
│   ├── tests               # Tests folder
│      ├── # Left some generic ones.
│
│   ├── main.py             # Main file containing endpoint definitions and orchestrator function (explained later)  
│   ├── __init__.py         # No description needed
│   ├── .gitignore          # No description needed
│   ├── .env                # Important file to add your environment variables.
│   ├── config.py           # Basic configurations file 
│   ├── requirements_test.txt  # No description needed
│   └── requirements.txt    # No description needed
│
├── .gitignore              # No description needed
├── firebase.json           # Functions config
└── LICENSE                 # No description needed
```

---

# ⚙️ Configurations and deploy

## 1. Auth Google Cloud

```
Install firebase CLI y log in 
gcloud config set project TU_ID_DEL_PROYECTO
```

## 2. Config Open AI APi Key

Add you API key into .env file

## 3. Run functions locally

```
firebase emulators:start --only functions,hosting
```

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

## 4. Run streamlit app
```
pip install -r frontend/requirements.txt
streamlit run forntend/app.py
```

# 🧪 Ejemplo de uso

## Entrada (en frontend):
* Opción 1: https://audiourl.something
* Opción 2: Texto: "My name is NAME i am GENDER i have YY years and i feel..."



## Salida
```
{
  "data": {
    "resultado": "Diagnóstico: Angina de pecho... Tratamiento: Reposo, nitroglicerina... Recomendaciones: Evitar esfuerzos..."
}
```
# High level functionality


                                      ┌─────────────┐
                                      │     User    │
                                      └────┬────────┘
                                           │
                          ┌────────────────┴───────────────┐
                          │           Web App              │
                          │  (React, Streamlit, etc.)      │
                          └────────────────┬───────────────┘
                                           │
                      ┌────────────────────┼────────────────────────┐
                      ▼                    ▼                        ▼
       [Audio URL or Text]        [See results ]       [Show errors/logs]
                                           │
                                ┌──────────▼────────────┐
                                │   Firebase Functions  │
                                │       (Python)        │
                                └──────────┬────────────┘
                                           ▼
    ┌─────────────┐ ┌──────────────────────┐ ┌────────────────────────┐
    │ Transcribe  │→│ Exttract data        │→│ Generate diagnostic    │
    └─────────────┘ └──────────────────────┘ └────────────────────────┘
      (Open AI)        (OpenAI / Gemini)         (OpenAI / Gemini)
                               │                          │
                     ┌────────▼────────┐       ┌──────────▼────────────┐
                     │   JSON Schema   │       │ Structured Text       │
                     └─────────────────┘       └───────────────────────┘


