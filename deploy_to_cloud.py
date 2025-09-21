#!/usr/bin/env python3
"""
Deploy AI Startup Evaluator to Google Cloud
"""

import subprocess
import os
import sys

def run_command(cmd, description):
    """Run command and handle errors"""
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}: SUCCESS")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description}: FAILED")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {e}")
        return False
    
    return True

def deploy_to_cloud():
    """Deploy to Google Cloud"""
    
    print("🚀 Deploying AI Startup Evaluator to Google Cloud")
    print("=" * 60)
    
    # Check if gcloud is installed
    if not run_command("gcloud version", "Checking gcloud CLI"):
        print("Please install Google Cloud CLI first")
        return False
    
    # Get project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable")
        return False
    
    print(f"Project ID: {project_id}")
    
    # Set project
    if not run_command(f"gcloud config set project {project_id}", "Setting project"):
        return False
    
    # Enable APIs
    apis = [
        "cloudbuild.googleapis.com",
        "run.googleapis.com",
        "containerregistry.googleapis.com",
        "aiplatform.googleapis.com"
    ]
    
    for api in apis:
        if not run_command(f"gcloud services enable {api}", f"Enabling {api}"):
            return False
    
    # Build and deploy using Cloud Build
    if not run_command("gcloud builds submit --config cloudbuild.yaml", "Building and deploying app"):
        return False
    
    # Get service URL
    run_command("gcloud run services describe startup-evaluator --region=us-central1 --format='value(status.url)'", "Getting service URL")
    
    print("\n🎉 Deployment completed!")
    print("Your AI Startup Evaluator is now live on Google Cloud Run")
    
    return True

if __name__ == "__main__":
    success = deploy_to_cloud()
    sys.exit(0 if success else 1)