#!/bin/bash

# Deploy AI Startup Evaluator Agents to Google Cloud Agent Engine

set -e

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
LOCATION=${AGENT_LOCATION:-"us-central1"}

echo "🚀 Deploying AI Startup Evaluator Agents"
echo "Project: $PROJECT_ID"
echo "Location: $LOCATION"
echo "=========================================="

# Check if project ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "❌ Error: Please set GOOGLE_CLOUD_PROJECT environment variable"
    echo "   export GOOGLE_CLOUD_PROJECT=your-actual-project-id"
    exit 1
fi

# Enable required APIs
echo "📋 Enabling required Google Cloud APIs..."
gcloud services enable aiplatform.googleapis.com --project=$PROJECT_ID
gcloud services enable dialogflow.googleapis.com --project=$PROJECT_ID
gcloud services enable speech.googleapis.com --project=$PROJECT_ID
gcloud services enable texttospeech.googleapis.com --project=$PROJECT_ID

# Set project
gcloud config set project $PROJECT_ID

# Install required Python packages
echo "📦 Installing required Python packages..."
pip install google-cloud-aiplatform google-cloud-dialogflow google-oauth2-tool pyyaml

# Deploy agents
echo "🤖 Deploying agents to Agent Engine..."
python deploy_agents.py

# Verify deployment
echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Check agent_registry.json for deployed agent IDs"
echo "2. Test agents using: python agent_client.py"
echo "3. Monitor agents in Cloud Console: https://console.cloud.google.com/ai/agents"
echo ""
echo "🔧 Environment variables for your application:"
echo "export GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
echo "export AGENT_LOCATION=$LOCATION"