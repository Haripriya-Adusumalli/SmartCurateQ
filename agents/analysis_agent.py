from typing import List
from models import StartupProfile, InvestmentMemo, RiskAssessment
from config import Config, InvestorPreferences
from datetime import datetime
import json

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    vertexai = None
    GenerativeModel = None

class AnalysisAgent:
    def __init__(self):
        if VERTEX_AI_AVAILABLE and Config.USE_VERTEX_AI:
            vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
            self.model = GenerativeModel('gemini-pro')
            self.use_vertex = True
        else:
            self.model = None
            self.use_vertex = False
    
    def generate_investment_memo(self, startup: StartupProfile, preferences: InvestorPreferences) -> InvestmentMemo:
        """Generate comprehensive investment memo"""
        
        # Calculate weighted investment score
        investment_score = self._calculate_investment_score(startup, preferences)
        
        # Assess risks
        risk_assessment = self._assess_risks(startup)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(startup, investment_score, risk_assessment)
        
        # Extract key insights
        strengths, concerns = self._extract_key_insights(startup)
        
        return InvestmentMemo(
            startup_profile=startup,
            investment_score=investment_score,
            risk_assessment=risk_assessment,
            recommendation=recommendation,
            key_strengths=strengths,
            key_concerns=concerns,
            generated_at=datetime.now()
        )
    
    def _calculate_investment_score(self, startup: StartupProfile, preferences: InvestorPreferences) -> float:
        """Calculate weighted investment score based on investor preferences"""
        
        # Founder score (0-10)
        founder_score = sum(f.founder_market_fit_score for f in startup.founders) / len(startup.founders)
        
        # Market score (0-10)
        market_score = self._score_market_opportunity(startup.market_analysis)
        
        # Differentiation score (0-10)
        diff_score = self._score_differentiation(startup.unique_differentiator)
        
        # Traction score (0-10)
        traction_score = self._score_traction(startup.business_metrics)
        
        # Apply investor weights
        weighted_score = (
            founder_score * preferences.founder_weight +
            market_score * preferences.market_weight +
            diff_score * preferences.differentiation_weight +
            traction_score * preferences.traction_weight
        )
        
        return min(10.0, max(0.0, weighted_score))
    
    def _score_market_opportunity(self, market: any) -> float:
        """Score market opportunity (0-10)"""
        score = 5.0  # Base score
        
        if market.market_size > Config.MIN_MARKET_SIZE:
            score += 2.0
        
        if market.growth_rate > 0.15:  # 15% growth
            score += 1.5
        
        if market.competition_level == "low":
            score += 1.5
        elif market.competition_level == "high":
            score -= 1.0
        
        return min(10.0, max(0.0, score))
    
    def _score_differentiation(self, differentiator: str) -> float:
        """Score unique differentiation using AI"""
        if not self.use_vertex or not self.model:
            # Basic scoring without AI
            if "patent" in differentiator.lower() or "proprietary" in differentiator.lower():
                return 8.0
            elif "unique" in differentiator.lower() or "first" in differentiator.lower():
                return 7.0
            else:
                return 5.0
        
        prompt = f"""
        Rate the uniqueness and defensibility of this differentiator on a scale of 0-10:
        
        "{differentiator}"
        
        Consider:
        - Uniqueness in market
        - Defensibility (patents, network effects, etc.)
        - Scalability potential
        - Competitive moat strength
        
        Return only a numeric score.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return float(response.text.strip())
        except:
            return 5.0
    
    def _score_traction(self, metrics: any) -> float:
        """Score business traction based on metrics"""
        score = 0.0
        
        if metrics.revenue and metrics.revenue > 0:
            score += 3.0
            if metrics.revenue_growth and metrics.revenue_growth > Config.MIN_REVENUE_GROWTH:
                score += 2.0
        
        if metrics.employees and metrics.employees > 5:
            score += 1.0
        
        if metrics.cac and metrics.ltv and metrics.cac > 0 and metrics.ltv > metrics.cac * 3:
            score += 2.0
        
        if metrics.churn_rate is not None and metrics.churn_rate < 0.05:  # <5% monthly churn
            score += 2.0
        
        return min(10.0, score)
    
    def _assess_risks(self, startup: StartupProfile) -> RiskAssessment:
        """Assess investment risks"""
        risk_factors = []
        risk_level = "low"
        
        # Check for risk indicators
        if startup.market_analysis.competition_level == "high":
            risk_factors.append("High competition in market")
        
        if startup.business_metrics.churn_rate is not None and startup.business_metrics.churn_rate > 0.1:
            risk_factors.append("High customer churn rate")
        
        if not startup.business_metrics.revenue or startup.business_metrics.revenue == 0:
            risk_factors.append("No revenue traction")
        
        # Determine overall risk level
        if len(risk_factors) > 3:
            risk_level = "high"
        elif len(risk_factors) > 1:
            risk_level = "medium"
        
        return RiskAssessment(
            risk_level=risk_level,
            risk_factors=risk_factors,
            mitigation_strategies=self._generate_mitigation_strategies(risk_factors)
        )
    
    def _generate_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """Generate risk mitigation strategies"""
        strategies = []
        for risk in risk_factors:
            if "competition" in risk.lower():
                strategies.append("Focus on unique value proposition and customer retention")
            elif "churn" in risk.lower():
                strategies.append("Implement customer success programs and product improvements")
            elif "revenue" in risk.lower():
                strategies.append("Develop clear monetization strategy and sales pipeline")
        
        return strategies
    
    def _generate_recommendation(self, startup: StartupProfile, score: float, risk: RiskAssessment) -> str:
        """Generate investment recommendation"""
        if score >= 8.0 and risk.risk_level == "low":
            return "STRONG BUY - High potential with manageable risks"
        elif score >= 6.5 and risk.risk_level in ["low", "medium"]:
            return "BUY - Good opportunity with acceptable risk profile"
        elif score >= 5.0:
            return "HOLD - Monitor progress, consider follow-on rounds"
        else:
            return "PASS - Significant concerns outweigh potential"
    
    def _extract_key_insights(self, startup: StartupProfile) -> tuple[List[str], List[str]]:
        """Extract key strengths and concerns"""
        strengths = []
        concerns = []
        
        # Analyze strengths
        avg_founder_score = sum(f.founder_market_fit_score for f in startup.founders) / len(startup.founders)
        if avg_founder_score > 7.0:
            strengths.append("Strong founder-market fit")
        
        if startup.market_analysis.market_size > Config.MIN_MARKET_SIZE:
            strengths.append("Large addressable market")
        
        if startup.business_metrics.revenue and startup.business_metrics.revenue > 0:
            strengths.append("Revenue generating")
        
        # Analyze concerns
        if startup.market_analysis.competition_level == "high":
            concerns.append("Highly competitive market")
        
        if not startup.business_metrics.revenue:
            concerns.append("Pre-revenue stage")
        
        return strengths, concerns