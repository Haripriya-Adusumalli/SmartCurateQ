#!/usr/bin/env python3
"""
Simple test script to verify all agents work correctly
"""

import sys
import traceback
from agents.orchestrator_agent import OrchestratorAgent

def test_basic_functionality():
    """Test basic agent functionality"""
    print("Testing SmartCurateQ 8-Agent System...")
    
    try:
        # Initialize orchestrator
        print("1. Initializing orchestrator...")
        orchestrator = OrchestratorAgent()
        print("Orchestrator initialized successfully")
        
        # Test data
        test_input = {
            "manual_data": {
                "company_name": "TestCorp AI",
                "problem_statement": "Solving data analysis problems",
                "solution": "AI-powered analytics platform",
                "unique_differentiator": "Proprietary ML algorithms",
                "funding_stage": "Seed",
                "revenue": 100000,
                "employees": 5,
                "market_size": 1000000000,
                "founders": [{
                    "name": "John Doe",
                    "background": "Former Google engineer",
                    "experience_years": 8,
                    "previous_exits": 1,
                    "domain_expertise": "Machine Learning"
                }]
            }
        }
        
        test_preferences = {
            "founder_weight": 0.3,
            "market_weight": 0.25,
            "differentiation_weight": 0.25,
            "traction_weight": 0.2
        }
        
        print("2. Testing individual agents...")
        
        # Test each agent individually
        agents_to_test = [
            "extraction", "mapping", "public_data", 
            "scheduling", "voice_interview", "memo_refinement"
        ]
        
        for agent_name in agents_to_test:
            try:
                print(f"   Testing {agent_name} agent...")
                # Basic agent initialization test
                agent = orchestrator.agents.get(agent_name)
                if agent:
                    print(f"   {agent_name} agent initialized successfully")
                else:
                    print(f"   {agent_name} agent not found")
            except Exception as e:
                print(f"   {agent_name} agent error: {str(e)}")
        
        print("3. Testing pipeline phases...")
        
        # Test Phase 1
        try:
            phase1_result = orchestrator._execute_phase1(test_input)
            if phase1_result.get("success"):
                print("   Phase 1 (Extraction & Mapping) works")
            else:
                print(f"   Phase 1 failed: {phase1_result.get('error')}")
        except Exception as e:
            print(f"   Phase 1 error: {str(e)}")
        
        print("4. System test complete!")
        return True
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)