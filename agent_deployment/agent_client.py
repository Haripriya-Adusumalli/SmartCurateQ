#!/usr/bin/env python3
"""
Client for interacting with deployed agents on Google Cloud Agent Engine
"""

import json
import os
from typing import Dict, Any, List
from google.cloud import aiplatform
import asyncio

class AgentClient:
    def __init__(self, registry_file: str = "agent_registry.json"):
        """Initialize client with deployed agent registry"""
        self.agents = self._load_agent_registry(registry_file)
        
        # Initialize AI Platform
        aiplatform.init(
            project=self.agents["project_id"],
            location=self.agents["location"]
        )
    
    def _load_agent_registry(self, registry_file: str) -> dict:
        """Load deployed agent registry"""
        try:
            with open(registry_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Agent registry file {registry_file} not found. Please deploy agents first.")
    
    async def call_agent(self, agent_name: str, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Call a specific agent with a prompt"""
        if agent_name not in self.agents["agents"]:
            raise ValueError(f"Agent {agent_name} not found in registry")
        
        agent_id = self.agents["agents"][agent_name]
        
        try:
            # Get agent instance
            agent = aiplatform.Agent(agent_id)
            
            # Prepare context
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {json.dumps(context)}\n\nTask: {prompt}"
            
            # Call agent
            response = await agent.predict(
                instances=[{"prompt": full_prompt}]
            )
            
            return {
                "agent": agent_name,
                "response": response.predictions[0],
                "status": "success"
            }
            
        except Exception as e:
            return {
                "agent": agent_name,
                "error": str(e),
                "status": "error"
            }
    
    async def orchestrate_startup_evaluation(self, startup_data: Dict) -> Dict[str, Any]:
        """Orchestrate complete startup evaluation using all agents"""
        
        print("🚀 Starting multi-agent startup evaluation...")
        results = {}
        
        # Step 1: Data Extraction
        print("📊 Step 1: Data Extraction...")
        extraction_result = await self.call_agent(
            "data-extraction-agent",
            "Extract and structure the startup data provided in the context",
            startup_data
        )
        results["extraction"] = extraction_result
        
        if extraction_result["status"] == "error":
            return {"error": "Data extraction failed", "details": extraction_result}
        
        # Step 2: Data Mapping
        print("🗺️ Step 2: Data Mapping and Scoring...")
        mapping_result = await self.call_agent(
            "mapping-agent",
            "Map the extracted data to standardized startup profile and calculate founder-market fit scores",
            extraction_result["response"]
        )
        results["mapping"] = mapping_result
        
        # Step 3: Public Data Enrichment
        print("🌐 Step 3: Public Data Enrichment...")
        public_data_result = await self.call_agent(
            "public-data-agent",
            "Enrich the startup profile with public data and verify claims",
            mapping_result["response"]
        )
        results["public_data"] = public_data_result
        
        # Step 4: Analysis and Scoring
        print("📈 Step 4: Investment Analysis...")
        analysis_result = await self.call_agent(
            "analysis-agent",
            "Generate investment score, risk assessment, and recommendation based on all available data",
            {
                "startup_profile": mapping_result["response"],
                "public_data": public_data_result["response"],
                "investor_preferences": startup_data.get("investor_preferences", {})
            }
        )
        results["analysis"] = analysis_result
        
        # Step 5: Final Orchestration
        print("🎯 Step 5: Final Memo Generation...")
        final_result = await self.call_agent(
            "orchestrator-agent",
            "Synthesize all agent outputs into a comprehensive investment memo",
            results
        )
        results["final_memo"] = final_result
        
        print("✅ Multi-agent evaluation completed!")
        return results
    
    async def schedule_founder_interview(self, startup_data: Dict, questions: List[str] = None) -> Dict[str, Any]:
        """Schedule and conduct founder interview using Voice Agent"""
        
        default_questions = [
            "Can you walk me through the specific problem you're solving?",
            "How did you validate that this problem exists in the market?",
            "What makes your solution unique compared to existing alternatives?",
            "What are the key assumptions in your business model?",
            "What would be the biggest risk that could cause this business to fail?",
            "How do you plan to scale your team and operations?"
        ]
        
        interview_context = {
            "startup_data": startup_data,
            "questions": questions or default_questions,
            "interview_type": "investment_evaluation"
        }
        
        return await self.call_agent(
            "voice-agent",
            "Conduct a structured interview with the startup founder to gather deeper insights",
            interview_context
        )
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all deployed agents"""
        status = {}
        
        for agent_name, agent_id in self.agents["agents"].items():
            try:
                agent = aiplatform.Agent(agent_id)
                status[agent_name] = agent.state
            except Exception as e:
                status[agent_name] = f"Error: {str(e)}"
        
        return status
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents["agents"].keys())

# Example usage
async def main():
    """Example usage of the agent client"""
    
    # Sample startup data
    sample_startup = {
        "company_name": "EcoTech Solutions",
        "problem_statement": "Traditional manufacturing processes waste 30% of raw materials",
        "solution": "AI-powered optimization platform that reduces material waste by 40%",
        "founders": [
            {
                "name": "Dr. Maria Rodriguez",
                "background": "Former Tesla manufacturing engineer with PhD in Industrial Engineering",
                "experience_years": 12
            }
        ],
        "market_size": 12000000000,
        "revenue": 2500000,
        "employees": 28,
        "investor_preferences": {
            "founder_weight": 0.3,
            "market_weight": 0.25,
            "differentiation_weight": 0.25,
            "traction_weight": 0.2
        }
    }
    
    try:
        # Initialize client
        client = AgentClient()
        
        # Check agent status
        print("🔍 Checking agent status...")
        status = client.get_agent_status()
        for agent, state in status.items():
            print(f"   {agent}: {state}")
        
        # Run complete evaluation
        results = await client.orchestrate_startup_evaluation(sample_startup)
        
        # Print final memo
        if "final_memo" in results and results["final_memo"]["status"] == "success":
            print("\n📋 Investment Memo Generated:")
            print(results["final_memo"]["response"])
        else:
            print("❌ Evaluation failed")
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())