#!/bin/bash

# Deploy to Google Cloud Run
gcloud run deploy smartcurateq \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --max-instances 10