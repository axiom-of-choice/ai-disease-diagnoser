#!/bin/bash

gcloud run deploy transcribe-service \
  --source ../backend/transcribe \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy extract-service \
  --source ../backend/extract \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy diagnose-service \
  --source ../backend/diagnose \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
