from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class FounderProfile(BaseModel):
    name: str
    background: str
    experience_years: Optional[int] = 5
    previous_exits: Optional[int] = 0
    domain_expertise: Optional[str] = "Business"
    founder_market_fit_score: Optional[float] = 6.0

class MarketAnalysis(BaseModel):
    market_size: float
    growth_rate: float
    competition_level: str
    key_players: List[str]
    market_maturity: str

class BusinessMetrics(BaseModel):
    revenue: Optional[float] = None
    revenue_growth: Optional[float] = None
    employees: Optional[int] = None
    cac: Optional[float] = None
    ltv: Optional[float] = None
    churn_rate: Optional[float] = None
    burn_rate: Optional[float] = None

class StartupProfile(BaseModel):
    company_name: str
    founders: List[FounderProfile]
    problem_statement: str
    solution: str
    unique_differentiator: str
    market_analysis: MarketAnalysis
    business_metrics: BusinessMetrics
    funding_stage: str
    funding_amount: Optional[float] = None

class RiskAssessment(BaseModel):
    risk_level: str  # low, medium, high
    risk_factors: List[str]
    mitigation_strategies: List[str]

class InvestmentMemo(BaseModel):
    startup_profile: StartupProfile
    investment_score: float
    risk_assessment: RiskAssessment
    recommendation: str
    key_strengths: List[str]
    key_concerns: List[str]
    generated_at: datetime