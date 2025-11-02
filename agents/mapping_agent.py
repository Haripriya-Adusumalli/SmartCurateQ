from typing import Dict, Any
from models import StartupProfile, FounderProfile, MarketAnalysis, BusinessMetrics
from config import Config
import json

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    vertexai = None
    GenerativeModel = None

class MappingAgent:
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
    
    def map_to_startup_profile(self, extracted_data: Dict[str, Any]) -> StartupProfile:
        """Map extracted data to structured startup profile"""
        
        # Map founder profiles
        founders = self._extract_founders(extracted_data)
        if not founders:  # Ensure at least one founder
            founders = [FounderProfile(
                name="Founder",
                background="Industry expert",
                experience_years=5,
                previous_exits=0,
                domain_expertise="Business",
                founder_market_fit_score=6.0
            )]
        
        # Map market analysis
        market_analysis = self._extract_market_analysis(extracted_data)
        
        # Map business metrics
        business_metrics = self._extract_business_metrics(extracted_data)
        
        # Generate unique differentiator if not provided
        differentiator = extracted_data.get('differentiator', '') or extracted_data.get('unique_differentiator', '')
        if not differentiator:
            solution = extracted_data.get('solution', '')
            if solution:
                differentiator = f"Innovative approach: {solution[:100]}"
            else:
                differentiator = "Unique market positioning"
        
        # Debug: Print extracted data to see what we're getting
        print(f"MAPPING AGENT - Extracted data keys: {list(extracted_data.keys())}")
        print(f"MAPPING AGENT - Company: {extracted_data.get('company_name')}")
        print(f"MAPPING AGENT - Problem: {extracted_data.get('problem_statement')}")
        print(f"MAPPING AGENT - Solution: {extracted_data.get('solution')}")
        
        return StartupProfile(
            company_name=extracted_data.get('company_name') or 'Unknown Company',
            founders=founders,
            problem_statement=extracted_data.get('problem_statement') or 'Problem not identified',
            solution=extracted_data.get('solution') or 'Solution not identified',
            unique_differentiator=differentiator,
            market_analysis=market_analysis,
            business_metrics=business_metrics,
            funding_stage=extracted_data.get('funding_stage') or 'Seed',
            funding_amount=extracted_data.get('funding_amount')
        )
    
    def _extract_founders(self, data: Dict) -> list[FounderProfile]:
        """Extract and score founder profiles"""
        founders_data = data.get('founders', [])
        founders = []
        
        if not founders_data:
            return founders
        
        for founder_info in founders_data:
            # Calculate founder-market fit score using AI
            fit_score = self._calculate_founder_market_fit(
                founder_info, 
                data.get('problem_statement', ''),
                data.get('market_analysis', {})
            )
            
            founder = FounderProfile(
                name=founder_info.get('name') or 'Unknown Founder',
                background=founder_info.get('background') or 'Background not specified',
                experience_years=founder_info.get('experience_years') or 5,
                previous_exits=founder_info.get('previous_exits') or 0,
                domain_expertise=founder_info.get('domain_expertise') or 'Business',
                founder_market_fit_score=fit_score or 6.0
            )
            founders.append(founder)
        
        return founders
    
    def _extract_market_analysis(self, data: Dict) -> MarketAnalysis:
        """Extract market analysis data"""
        market_data = data.get('market_analysis', {})
        
        # Get market size from direct form input or nested data
        market_size = data.get('market_size', 0) or market_data.get('market_size', 0)
        
        return MarketAnalysis(
            market_size=market_size,
            growth_rate=market_data.get('growth_rate', 0.15),  # Default 15% growth
            competition_level=market_data.get('competition_level', 'medium'),
            key_players=market_data.get('key_players', ['Competitor A', 'Competitor B']),
            market_maturity=market_data.get('market_maturity', 'Growing')
        )
    
    def _extract_business_metrics(self, data: Dict) -> BusinessMetrics:
        """Extract business KPIs"""
        metrics_data = data.get('business_metrics', {})
        
        # Get values from direct form input or nested data
        revenue = data.get('revenue') or metrics_data.get('revenue')
        employees = data.get('employees') or metrics_data.get('employees')
        
        return BusinessMetrics(
            revenue=revenue,
            revenue_growth=metrics_data.get('revenue_growth', 0.2 if revenue and revenue > 0 else None),
            employees=employees,
            cac=metrics_data.get('cac'),
            ltv=metrics_data.get('ltv'),
            churn_rate=metrics_data.get('churn_rate'),
            burn_rate=metrics_data.get('burn_rate')
        )
    
    def _calculate_founder_market_fit(self, founder_info: Dict, problem: str, market: Dict) -> float:
        """Calculate founder-market fit score using AI"""
        prompt = f"""
        Evaluate founder-market fit on a scale of 0-10:
        
        Founder: {json.dumps(founder_info)}
        Problem: {problem}
        Market: {json.dumps(market)}
        
        Consider:
        - Domain expertise relevance
        - Previous experience in similar markets
        - Technical background alignment
        - Network and connections
        
        Return only a numeric score between 0-10.
        """
        
        if not self.use_vertex or not self.model:
            # Calculate basic score based on experience without AI
            experience_years = founder_info.get('experience_years', 0)
            domain_match = 1.0 if founder_info.get('domain_expertise', '').lower() in problem.lower() else 0.0
            return min(10.0, 5.0 + (experience_years * 0.3) + (domain_match * 2.0))
        
        try:
            response = self.model.generate_content(prompt)
            score = float(response.text.strip())
            return max(0.0, min(10.0, score))
        except:
            # Calculate basic score based on experience
            experience_years = founder_info.get('experience_years', 0)
            return min(10.0, 5.0 + (experience_years * 0.3))