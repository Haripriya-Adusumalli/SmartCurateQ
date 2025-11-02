#!/bin/bash

# Deploy SmartCurateQ LVX Platform to GCP

echo "🚀 Deploying SmartCurateQ LVX Platform..."

# Set project
gcloud config set project firstsample-269604

# Create BigQuery dataset
echo "📊 Creating BigQuery dataset..."
bq mk --dataset --location=us-central1 firstsample-269604:lvx_curation

# Create BigQuery tables
echo "🗄️ Creating BigQuery tables..."
bq query --use_legacy_sql=false "$(cat bigquery_schema.sql)"

# Create storage bucket
echo "🪣 Creating storage bucket..."
gsutil mb -l us-central1 gs://lvx-startup-assets

# Deploy to App Engine
echo "☁️ Deploying to App Engine..."
gcloud app deploy app.yaml --quiet

# Get the deployed URL
echo "✅ Deployment complete!"
echo "🌐 Application URL: https://firstsample-269604.appspot.com"