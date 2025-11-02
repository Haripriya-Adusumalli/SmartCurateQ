import os
from dataclasses import dataclass
from typing import Dict

@dataclass
class InvestorPreferences:
    founder_weight: float = 0.25
    market_weight: float = 0.25
    differentiation_weight: float = 0.25
    traction_weight: float = 0.25
    risk_tolerance: str = "medium"  # low, medium, high
    custom_weights: Dict[str, float] = None  # For 350 metric weights

class Config:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "firstsample-269604")
    LOCATION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    # Vertex AI uses service account authentication in Cloud Run
    
    # LVX Platform Configuration
    BUCKET_NAME = os.getenv("LVX_STORAGE_BUCKET", "lvx-startup-assets")
    BIGQUERY_DATASET = os.getenv("LVX_BIGQUERY_DATASET", "lvx_curation")
    PUBSUB_TOPICS = {
        "ingestion": "ingestion-events",
        "extraction": "extraction-events", 
        "enrichment": "enrichment-events",
        "mapping": "mapping-events",
        "scoring": "scoring-events",
        "memo": "memo-events",
        "voice": "voice-events"
    }
    
    # 350 Curation Metrics Framework
    CURATION_METRICS_COUNT = 350
    SCORING_SEGMENTS = {
        "founder_profile": 0.25,
        "problem_market_size": 0.25, 
        "unique_differentiator": 0.25,
        "team_traction": 0.25
    }
    
    # Analysis thresholds
    MIN_MARKET_SIZE = 1000000000  # $1B
    MIN_REVENUE_GROWTH = 0.2  # 20%
    MAX_CAC_PAYBACK = 12  # months
    
    # Voice Agent Configuration
    VOICE_INTERVIEW_DURATION = 30  # minutes
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    
    # External Data Sources
    EXTERNAL_APIS = {
        "vcch": os.getenv("VCCH_API_KEY"),
        "probe42": os.getenv("PROBE42_API_KEY"),
        "traction": os.getenv("TRACTION_API_KEY")
    }
    
    # Risk flags
    RISK_INDICATORS = [
        "inconsistent_metrics",
        "inflated_market_size", 
        "high_churn",
        "weak_founder_fit",
        "intense_competition",
        "reputation_risks",
        "regulatory_concerns"
    ]