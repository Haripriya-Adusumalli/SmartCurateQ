@echo off
echo Deploying SmartCurateQ to Google Cloud Run...

REM Check if gcloud is installed
gcloud version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Google Cloud CLI not found. Please install it first.
    exit /b 1
)

REM Set project (replace with your project ID)
set PROJECT_ID=firstsample-269604
gcloud config set project %PROJECT_ID%

REM Enable required APIs
echo Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com

REM Deploy using Cloud Build
echo Building and deploying application...
gcloud builds submit --config cloudbuild.yaml

REM Get the service URL
echo Getting service URL...
gcloud run services describe startup-evaluator --region=us-central1 --format="value(status.url)"

echo.
echo Deployment completed! Your SmartCurateQ app is now live.
pause