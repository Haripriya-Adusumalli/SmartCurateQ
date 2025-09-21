import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from config import Config
import json

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
except ImportError:
    vertexai = None
    GenerativeModel = None

class PublicDataAgent:
    def __init__(self):
        if vertexai and GenerativeModel:
            self.model = GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
    
    def enrich_startup_data(self, company_name: str, founders: List[str]) -> Dict:
        """Enrich startup data with public information"""
        
        enriched_data = {
            "news_articles": self._search_news(company_name),
            "founder_profiles": self._research_founders(founders),
            "market_data": self._get_market_insights(company_name),
            "competitor_analysis": self._analyze_competitors(company_name)
        }
        
        return enriched_data
    
    def _search_news(self, company_name: str) -> List[Dict]:
        """Search for recent news about the company"""
        # Simulate news search (in production, use News API or similar)
        mock_articles = [
            {
                "title": f"{company_name} raises Series A funding",
                "source": "TechCrunch",
                "date": "2024-01-15",
                "sentiment": "positive",
                "summary": f"Analysis of {company_name}'s recent funding round"
            },
            {
                "title": f"{company_name} launches new product feature",
                "source": "VentureBeat", 
                "date": "2024-01-10",
                "sentiment": "neutral",
                "summary": f"{company_name} expands product capabilities"
            }
        ]
        
        return mock_articles
    
    def _research_founders(self, founders: List[str]) -> Dict:
        """Research founder backgrounds from public sources"""
        founder_data = {}
        
        for founder in founders:
            # Simulate LinkedIn/public profile research
            founder_data[founder] = {
                "linkedin_profile": f"linkedin.com/in/{founder.lower().replace(' ', '-')}",
                "previous_companies": ["TechCorp", "StartupXYZ"],
                "education": ["Stanford University", "MIT"],
                "publications": 5,
                "patents": 2,
                "social_presence_score": 7.5
            }
        
        return founder_data
    
    def _get_market_insights(self, company_name: str) -> Dict:
        """Get market size and competition data"""
        # Simulate market research (in production, use market research APIs)
        prompt = f"""
        Provide market analysis for a company like {company_name}.
        Include:
        - Estimated market size
        - Growth projections
        - Key market trends
        - Regulatory considerations
        
        Return as structured data.
        """
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                return json.loads(response.text)
        except:
            pass
        
        return {
            "market_size_estimate": 5000000000,  # $5B
            "growth_rate": 0.15,  # 15%
            "key_trends": ["Digital transformation", "AI adoption"],
            "regulatory_risks": "Medium"
        }
    
    def _analyze_competitors(self, company_name: str) -> List[Dict]:
        """Analyze competitive landscape"""
        # Simulate competitor analysis
        competitors = [
            {
                "name": "CompetitorA",
                "funding_raised": 50000000,
                "employees": 200,
                "market_share": 0.15,
                "differentiation": "Enterprise focus"
            },
            {
                "name": "CompetitorB", 
                "funding_raised": 25000000,
                "employees": 100,
                "market_share": 0.08,
                "differentiation": "SMB market"
            }
        ]
        
        return competitors
    
    def verify_claims(self, startup_claims: Dict) -> Dict:
        """Verify startup claims against public data"""
        verification_results = {}
        
        # Verify market size claims
        claimed_market_size = startup_claims.get('market_size', 0)
        if claimed_market_size > 100000000000:  # >$100B
            verification_results['market_size'] = {
                'status': 'inflated',
                'confidence': 0.8,
                'note': 'Market size claim appears inflated compared to industry reports'
            }
        else:
            verification_results['market_size'] = {
                'status': 'reasonable',
                'confidence': 0.7,
                'note': 'Market size claim within reasonable bounds'
            }
        
        # Verify revenue claims
        claimed_revenue = startup_claims.get('revenue', 0)
        if claimed_revenue is not None and claimed_revenue > 0:
            verification_results['revenue'] = {
                'status': 'unverified',
                'confidence': 0.5,
                'note': 'Revenue claims require further verification'
            }
        else:
            verification_results['revenue'] = {
                'status': 'no_revenue',
                'confidence': 0.9,
                'note': 'No revenue reported or pre-revenue stage'
            }
        
        return verification_results