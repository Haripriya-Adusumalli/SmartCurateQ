#!/usr/bin/env python3
"""
Cloud-based Startup Evaluator using deployed Google Cloud Agents
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from agent_deployment.agent_client import AgentClient
from models import InvestmentMemo, StartupProfile, RiskAssessment
from config import InvestorPreferences

class CloudStartupEvaluator:
    """
    Cloud-based startup evaluator using Google Cloud Agent Engine
    """
    
    def __init__(self, registry_file: str = "agent_deployment/agent_registry.json"):
        """Initialize with deployed agents"""
        try:
            self.agent_client = AgentClient(registry_file)
            self.agents_available = True
            print("✅ Connected to deployed agents on Google Cloud")
        except Exception as e:
            print(f"⚠️ Could not connect to deployed agents: {e}")
            self.agents_available = False
    
    async def evaluate_startup(self, 
                              pitch_deck_path: str = None,
                              form_data: Dict = None,
                              investor_preferences: InvestorPreferences = None) -> InvestmentMemo:
        """
        Complete startup evaluation using cloud agents
        """
        
        if not self.agents_available:
            raise Exception("Cloud agents not available. Please deploy agents first.")
        
        if investor_preferences is None:
            investor_preferences = InvestorPreferences()
        
        # Prepare input data
        startup_data = {
            "pitch_deck_path": pitch_deck_path,
            "form_data": form_data,
            "investor_preferences": {
                "founder_weight": investor_preferences.founder_weight,
                "market_weight": investor_preferences.market_weight,
                "differentiation_weight": investor_preferences.differentiation_weight,
                "traction_weight": investor_preferences.traction_weight,
                "risk_tolerance": investor_preferences.risk_tolerance
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Run multi-agent evaluation
        print("🚀 Starting cloud-based startup evaluation...")
        results = await self.agent_client.orchestrate_startup_evaluation(startup_data)
        
        # Parse results into InvestmentMemo
        return self._parse_agent_results(results)
    
    async def batch_evaluate(self, 
                            startup_data_list: list, 
                            investor_preferences: InvestorPreferences = None) -> list[InvestmentMemo]:
        """Evaluate multiple startups using cloud agents"""
        
        results = []
        
        for i, startup_data in enumerate(startup_data_list):
            try:
                print(f"📊 Evaluating startup {i+1}/{len(startup_data_list)}...")
                
                memo = await self.evaluate_startup(
                    pitch_deck_path=startup_data.get('pitch_deck_path'),
                    form_data=startup_data.get('form_data'),
                    investor_preferences=investor_preferences
                )
                results.append(memo)
                
                # Brief pause between evaluations
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Error evaluating startup {i+1}: {e}")
                continue
        
        return results
    
    async def schedule_founder_interview(self, 
                                       startup_data: Dict,
                                       custom_questions: list = None) -> Dict[str, Any]:
        """Schedule and conduct founder interview using Voice Agent"""
        
        if not self.agents_available:
            raise Exception("Cloud agents not available")
        
        print("🎤 Scheduling founder interview...")
        
        return await self.agent_client.schedule_founder_interview(
            startup_data, 
            custom_questions
        )
    
    def _parse_agent_results(self, results: Dict[str, Any]) -> InvestmentMemo:
        """Parse agent results into InvestmentMemo object"""
        
        try:
            # Extract final memo from orchestrator
            final_memo = results.get("final_memo", {}).get("response", {})
            
            if isinstance(final_memo, str):
                final_memo = json.loads(final_memo)
            
            # Create mock objects for now (in production, parse from agent responses)
            startup_profile = StartupProfile(
                company_name=final_memo.get("company_name", "Unknown"),
                founders=[],  # Parse from mapping agent results
                problem_statement=final_memo.get("problem_statement", ""),
                solution=final_memo.get("solution", ""),
                unique_differentiator=final_memo.get("unique_differentiator", ""),
                market_analysis=None,  # Parse from mapping agent results
                business_metrics=None,  # Parse from mapping agent results
                funding_stage=final_memo.get("funding_stage", "Unknown")
            )
            
            risk_assessment = RiskAssessment(
                risk_level=final_memo.get("risk_level", "medium"),
                risk_factors=final_memo.get("risk_factors", []),
                mitigation_strategies=final_memo.get("mitigation_strategies", [])
            )
            
            memo = InvestmentMemo(
                startup_profile=startup_profile,
                investment_score=final_memo.get("investment_score", 5.0),
                risk_assessment=risk_assessment,
                recommendation=final_memo.get("recommendation", "HOLD"),
                key_strengths=final_memo.get("key_strengths", []),
                key_concerns=final_memo.get("key_concerns", []),
                generated_at=datetime.now()
            )
            
            # Add cloud agent metadata
            memo.agent_results = results
            memo.evaluation_method = "cloud_agents"
            
            return memo
            
        except Exception as e:
            print(f"⚠️ Error parsing agent results: {e}")
            # Return default memo
            return self._create_default_memo()
    
    def _create_default_memo(self) -> InvestmentMemo:
        """Create default memo when parsing fails"""
        from models import FounderProfile, MarketAnalysis, BusinessMetrics
        
        default_founder = FounderProfile(
            name="Unknown",
            background="",
            experience_years=0,
            previous_exits=0,
            domain_expertise="",
            founder_market_fit_score=5.0
        )
        
        default_market = MarketAnalysis(
            market_size=1000000000,
            growth_rate=0.1,
            competition_level="medium",
            key_players=[],
            market_maturity="unknown"
        )
        
        default_metrics = BusinessMetrics()
        
        startup_profile = StartupProfile(
            company_name="Unknown Startup",
            founders=[default_founder],
            problem_statement="",
            solution="",
            unique_differentiator="",
            market_analysis=default_market,
            business_metrics=default_metrics,
            funding_stage="Unknown"
        )
        
        risk_assessment = RiskAssessment(
            risk_level="medium",
            risk_factors=["Incomplete evaluation"],
            mitigation_strategies=["Conduct manual review"]
        )
        
        return InvestmentMemo(
            startup_profile=startup_profile,
            investment_score=5.0,
            risk_assessment=risk_assessment,
            recommendation="HOLD - Requires manual review",
            key_strengths=["Evaluation incomplete"],
            key_concerns=["Agent parsing failed"],
            generated_at=datetime.now()
        )
    
    def generate_deal_note(self, investment_memo: InvestmentMemo) -> str:
        """Generate formatted deal note"""
        
        startup = investment_memo.startup_profile
        
        deal_note = f"""
# Investment Deal Note: {startup.company_name}

## Executive Summary
**Investment Score:** {investment_memo.investment_score:.1f}/10
**Recommendation:** {investment_memo.recommendation}
**Risk Level:** {investment_memo.risk_assessment.risk_level.upper()}
**Evaluation Method:** Cloud Agents (Google AI)

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

---
*Generated by AI Startup Evaluator (Cloud Agents) on {investment_memo.generated_at.strftime('%Y-%m-%d %H:%M')}*
*Powered by Google Cloud Agent Engine*
"""
        
        return deal_note
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all deployed agents"""
        if not self.agents_available:
            return {"status": "agents_not_available"}
        
        return self.agent_client.get_agent_status()

# Async wrapper functions for compatibility
def create_cloud_evaluator():
    """Create cloud evaluator instance"""
    return CloudStartupEvaluator()

async def evaluate_startup_async(evaluator: CloudStartupEvaluator, **kwargs):
    """Async wrapper for startup evaluation"""
    return await evaluator.evaluate_startup(**kwargs)

# Example usage
async def main():
    """Example usage of cloud startup evaluator"""
    
    # Sample startup data
    sample_startup = {
        "company_name": "CloudTech AI",
        "problem_statement": "Businesses struggle with cloud cost optimization",
        "solution": "AI-powered cloud cost optimization platform",
        "market_size": 8000000000,
        "revenue": 1500000,
        "employees": 22,
        "founders": [
            {
                "name": "Alex Chen",
                "background": "Former AWS Solutions Architect with 10 years experience",
                "experience_years": 10
            }
        ]
    }
    
    try:
        # Initialize cloud evaluator
        evaluator = CloudStartupEvaluator()
        
        # Check agent status
        print("🔍 Checking agent status...")
        status = evaluator.get_agent_status()
        for agent, state in status.items():
            print(f"   {agent}: {state}")
        
        # Evaluate startup
        memo = await evaluator.evaluate_startup(form_data=sample_startup)
        
        # Generate deal note
        deal_note = evaluator.generate_deal_note(memo)
        print("\n📋 Investment Deal Note:")
        print(deal_note)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())