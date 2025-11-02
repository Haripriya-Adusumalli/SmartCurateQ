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
        if VERTEX_AI_AVAILABLE:
            try:
                vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
                self.model = GenerativeModel('gemini-2.5-pro')
                self.use_vertex = True
            except Exception:
                self.model = None
                self.use_vertex = False
        else:
            self.model = None
            self.use_vertex = False
    
    def analyze_startup(self, startup: StartupProfile, preferences: InvestorPreferences) -> InvestmentMemo:
        """Analyze startup and generate investment memo"""
        return self.generate_investment_memo(startup, preferences)
    
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
        
        # Founder score (0-10) with null check
        if startup.founders and len(startup.founders) > 0:
            founder_scores = [f.founder_market_fit_score or 5.0 for f in startup.founders]
            founder_score = sum(founder_scores) / len(founder_scores)
        else:
            founder_score = 5.0
        
        # Market score (0-10)
        market_score = self._score_market_opportunity(startup.market_analysis) or 5.0
        
        # Differentiation score (0-10)
        diff_score = self._score_differentiation(startup.unique_differentiator or "") or 5.0
        
        # Traction score (0-10)
        traction_score = self._score_traction(startup.business_metrics) or 0.0
        
        # Apply investor weights with null checks
        founder_weight = preferences.founder_weight or 0.25
        market_weight = preferences.market_weight or 0.25
        diff_weight = preferences.differentiation_weight or 0.25
        traction_weight = preferences.traction_weight or 0.25
        
        weighted_score = (
            founder_score * founder_weight +
            market_score * market_weight +
            diff_score * diff_weight +
            traction_score * traction_weight
        )
        
        return min(10.0, max(0.0, weighted_score))
    
    def _score_market_opportunity(self, market: any) -> float:
        """Score market opportunity (0-10)"""
        if not market:
            return 5.0
            
        score = 5.0  # Base score
        
        market_size = getattr(market, 'market_size', 0) or 0
        if market_size > Config.MIN_MARKET_SIZE:
            score += 2.0
        
        growth_rate = getattr(market, 'growth_rate', 0) or 0
        if growth_rate > 0.15:  # 15% growth
            score += 1.5
        
        competition_level = getattr(market, 'competition_level', 'medium') or 'medium'
        if competition_level == "low":
            score += 1.5
        elif competition_level == "high":
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
        if not metrics:
            return 0.0
            
        score = 0.0
        
        revenue = getattr(metrics, 'revenue', 0) or 0
        if revenue > 0:
            score += 3.0
            revenue_growth = getattr(metrics, 'revenue_growth', 0) or 0
            if revenue_growth > Config.MIN_REVENUE_GROWTH:
                score += 2.0
        
        employees = getattr(metrics, 'employees', 0) or 0
        if employees > 5:
            score += 1.0
        
        cac = getattr(metrics, 'cac', 0) or 0
        ltv = getattr(metrics, 'ltv', 0) or 0
        if cac > 0 and ltv > 0 and ltv > cac * 3:
            score += 2.0
        
        churn_rate = getattr(metrics, 'churn_rate', None)
        if churn_rate is not None and churn_rate < 0.05:  # <5% monthly churn
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