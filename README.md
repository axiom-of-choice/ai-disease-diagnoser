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
│   ├── sample.env          # Basic configs
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
│   ├── sample.env          # Important file to add your environment variables.
│   ├── config.py           # Basic configurations file 
│   ├── requirements_test.txt  # No description needed
│   └── requirements.txt    # No description needed
│
├── .gitignore              # No description needed
├── firebase.json           # Functions config
└── LICENSE                 # No description needed
```

---

# ⚙️ Configurations of the project to run locally

## 1. Auth Google Cloud asnd Firebase


Install firebase CLI y log in. 

[reference](https://firebase.google.com/docs/hosting/quickstart)


## 2. Config Open AI APi Key

Add you API key into functions/sample.env file and **rename the file to .env**

## 3. Run functions locally

```
firebase emulators:start --only functions,hosting
```

After doing this, the backend should be up and running.
You need to check your terminal to see the links for accesing the functions locally. Something like this:
![image](public/Screenshot%202025-05-22%20at%2010.21.11 a.m..jpg)

**Save up the URL showed (in the image case http://127.0.0.1:5001/ai-diagnoser/us-central1/process_medical_data) because you will need it for the streamlit app**

## 4. Run streamlit app
First, **rename the sample.env to .env** and add the url above showed into the file as the ENDPOINT_URL var.


In another terminal, run the following.

```
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

You should be able to see something like this if everything went good.

![image](public/Screenshot%202025-05-22%20at%2010.25.33 a.m..jpg)

# 🧪 Sample use case.

## Option 1: https://audiourl.something:
## Output
![image](public/Use_case_audio.jpg)
## Option 2
## Output
![image](public/Use_case_text.jpg)


