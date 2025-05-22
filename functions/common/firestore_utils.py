import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

def update_consulta(user_id, consulta_id, data):
    doc_ref = db.collection('users').document(user_id).collection('consults').document(consulta_id)
    doc_ref.set(data, merge=True)
