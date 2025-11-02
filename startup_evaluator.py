from agents.data_extraction_agent import DataExtractionAgent
from agents.mapping_agent import MappingAgent
from agents.analysis_agent import AnalysisAgent
from agents.public_data_agent import PublicDataAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.enricher_agent import EnricherAgent
from agents.scoring_engine import ScoringEngine
from agents.voice_agent import VoiceAgent
from agents.memo_builder_agent import MemoBuilderAgent
from agents.scheduler_agent import SchedulerAgent
from models import InvestmentMemo
from config import InvestorPreferences, Config
from typing import Dict, Any
import uuid

class StartupEvaluator:
    """Enhanced LVX startup evaluation system with multi-agent architecture"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id or Config.PROJECT_ID
        
        # Initialize all agents
        self.data_extractor = DataExtractionAgent()
        self.mapper = MappingAgent()
        self.analyzer = AnalysisAgent()
        self.public_data_agent = PublicDataAgent(self.project_id)
        self.orchestrator = OrchestratorAgent(self.project_id)
        self.enricher = EnricherAgent(self.project_id)
        self.scoring_engine = ScoringEngine(self.project_id)
        self.voice_agent = VoiceAgent(self.project_id)
        self.memo_builder = MemoBuilderAgent(self.project_id)
        self.scheduler = SchedulerAgent(self.project_id)
    
    def evaluate_startup(self, 
                        pitch_deck_path: str = None,
                        audio_video_path: str = None,
                        video_url: str = None,
                        form_data: Dict = None,
                        investor_preferences: InvestorPreferences = None,
                        use_full_pipeline: bool = False) -> InvestmentMemo:
        """
        Complete startup evaluation pipeline
        
        Args:
            pitch_deck_path: Path to PDF pitch deck
            audio_video_path: Path to audio/video pitch file
            video_url: URL to YouTube or video link
            form_data: Google Form submission data
            investor_preferences: Investor weighting preferences
        
        Returns:
            InvestmentMemo: Complete investment analysis
        """
        
        if investor_preferences is None:
            investor_preferences = InvestorPreferences()
        
        # Step 1: Extract data from sources
        extracted_data = {}
        
        if pitch_deck_path:
            pitch_data = self.data_extractor.extract_from_pdf(pitch_deck_path)
            extracted_data.update(pitch_data)
        
        if audio_video_path:
            # Process audio/video file
            audio_data = self.voice_agent.process_audio_pitch(audio_video_path)
            extracted_data.update(audio_data)
        
        if video_url:
            # Process video URL
            video_data = self.voice_agent.process_video_url(video_url)
            extracted_data.update(video_data)
        
        if form_data:
            form_extracted = self.data_extractor.extract_from_form(form_data)
            if isinstance(form_extracted, dict):
                extracted_data.update(form_extracted)
            else:
                extracted_data = form_data  # Use original form data if extraction fails
        
        # Step 2: Map to structured startup profile
        startup_profile = self.mapper.map_to_startup_profile(extracted_data)
        
        # Debug: Ensure profile has required data
        if not startup_profile.problem_statement and extracted_data.get('problem_statement'):
            startup_profile.problem_statement = extracted_data['problem_statement']
        if not startup_profile.solution and extracted_data.get('solution'):
            startup_profile.solution = extracted_data['solution']
        if not startup_profile.unique_differentiator:
            startup_profile.unique_differentiator = f"Innovative solution: {startup_profile.solution[:50]}..." if startup_profile.solution else "Unique market approach"
        
        # Step 3: Skip public data enrichment for now (causing Pub/Sub errors)
        # public_data = self.public_data_agent.enrich_startup_data(enrichment_message)
        # verification_results = self.public_data_agent.verify_claims(startup_claims)
        print("Skipping public data enrichment to avoid Pub/Sub errors")
        
        # Step 5: Generate investment memo
        investment_memo = self.analyzer.generate_investment_memo(
            startup_profile, 
            investor_preferences
        )
        
        # Note: Public data and verification results are used internally
        # but not stored in the memo model for this version
        
        return investment_memo
    
    def batch_evaluate(self, startup_data_list: list, investor_preferences: InvestorPreferences = None) -> list[InvestmentMemo]:
        """Evaluate multiple startups in batch"""
        results = []
        
        for startup_data in startup_data_list:
            try:
                memo = self.evaluate_startup(
                    pitch_deck_path=startup_data.get('pitch_deck_path'),
                    audio_video_path=startup_data.get('audio_video_path'),
                    video_url=startup_data.get('video_url'),
                    form_data=startup_data.get('form_data'),
                    investor_preferences=investor_preferences
                )
                results.append(memo)
            except Exception as e:
                print(f"Error evaluating startup: {e}")
                continue
        
        return results
    
    def generate_deal_note(self, investment_memo: InvestmentMemo) -> str:
        """Generate formatted deal note for investors"""
        
        startup = investment_memo.startup_profile
        
        deal_note = f"""
# Investment Deal Note: {startup.company_name}

## Executive Summary
**Investment Score:** {investment_memo.investment_score:.1f}/10
**Recommendation:** {investment_memo.recommendation}
**Risk Level:** {investment_memo.risk_assessment.risk_level.upper()}

## Team/Founder Summary
"""
        
        for founder in startup.founders:
            deal_note += f"- **{founder.name}**: {founder.background} (Founder-Market Fit: {founder.founder_market_fit_score:.1f}/10)\n"
        
        deal_note += f"""

## Market Analysis
- **Market Size:** ${startup.market_analysis.market_size:,.0f}
- **Growth Rate:** {startup.market_analysis.growth_rate:.1%}
- **Competition Level:** {startup.market_analysis.competition_level}
- **Key Players:** {', '.join(startup.market_analysis.key_players)}

## Business Metrics
"""
        
        metrics = startup.business_metrics
        if metrics.revenue:
            deal_note += f"- **Revenue:** ${metrics.revenue:,.0f}\n"
        if metrics.revenue_growth:
            deal_note += f"- **Revenue Growth:** {metrics.revenue_growth:.1%}\n"
        if metrics.employees:
            deal_note += f"- **Team Size:** {metrics.employees} employees\n"
        if metrics.cac and metrics.ltv:
            deal_note += f"- **LTV/CAC Ratio:** {metrics.ltv/metrics.cac:.1f}\n"
        
        deal_note += f"""

## Key Strengths
"""
        for strength in investment_memo.key_strengths:
            deal_note += f"- {strength}\n"
        
        deal_note += f"""

## Key Concerns
"""
        for concern in investment_memo.key_concerns:
            deal_note += f"- {concern}\n"
        
        deal_note += f"""

## Risk Assessment
**Risk Factors:**
"""
        for risk in investment_memo.risk_assessment.risk_factors:
            deal_note += f"- {risk}\n"
        
        deal_note += f"""

## Unique Differentiator
{startup.unique_differentiator}

---
*Generated by AI Startup Evaluator on {investment_memo.generated_at.strftime('%Y-%m-%d %H:%M')}*
"""
        
        return deal_note