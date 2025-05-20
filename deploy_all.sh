gcloud functions deploy api \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point api \
  --source=backend


gcloud builds submit --tag gcr.io/<TU_PROJECT_ID>/streamlit-frontend


gcloud run deploy streamlit-frontend \
  --image gcr.io/<TU_PROJECT_ID>/streamlit-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
