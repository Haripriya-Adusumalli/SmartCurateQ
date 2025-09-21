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

class Config:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "firstsample-269604")
    LOCATION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    USE_VERTEX_AI = False  # Disable for now to use working extraction
    
    # Analysis thresholds
    MIN_MARKET_SIZE = 1000000000  # $1B
    MIN_REVENUE_GROWTH = 0.2  # 20%
    MAX_CAC_PAYBACK = 12  # months
    
    # Risk flags
    RISK_INDICATORS = [
        "inconsistent_metrics",
        "inflated_market_size", 
        "high_churn",
        "weak_founder_fit",
        "intense_competition"
    ]