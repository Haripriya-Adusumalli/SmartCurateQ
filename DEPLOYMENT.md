# SmartCurateQ Cloud Deployment Guide

## Quick Deploy to Google Cloud Run

### Prerequisites
1. **Google Cloud CLI**: Install from https://cloud.google.com/sdk/docs/install
2. **Google Cloud Project**: Create or select a project
3. **Authentication**: Run `gcloud auth login`

### Environment Setup
```bash
# Set your project ID
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Set API key (optional - for enhanced features)
export GEMINI_API_KEY="your_gemini_api_key"
```

### Deploy Options

#### Option 1: One-Click Deploy (Windows)
```cmd
deploy_simple.bat
```

#### Option 2: Manual Deploy (Cross-platform)
```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com aiplatform.googleapis.com

# Deploy using Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Get service URL
gcloud run services describe startup-evaluator --region=us-central1 --format="value(status.url)"
```

#### Option 3: Direct Deploy
```bash
gcloud run deploy smartcurateq \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --max-instances 10
```

### Configuration
- **Memory**: 2GB (handles PDF processing)
- **CPU**: 2 cores (for AI processing)
- **Timeout**: 1 hour (for complex analyses)
- **Region**: us-central1 (change as needed)

### Post-Deployment
1. Access your app at the provided URL
2. Test with sample pitch decks
3. Configure investor preferences
4. Monitor usage in Cloud Console

### Troubleshooting
- **Build fails**: Check Dockerfile and requirements.txt
- **Memory issues**: Increase memory allocation
- **Timeout**: Increase timeout for large files
- **API errors**: Verify GEMINI_API_KEY is set

### Cost Optimization
- Set max instances to control costs
- Use Cloud Scheduler for auto-scaling
- Monitor usage in Cloud Console