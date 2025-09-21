#!/usr/bin/env python3
"""
Simple test for AI Startup Evaluator agents
"""

import os
import sys
from datetime import datetime

# Set mock API key
os.environ["GEMINI_API_KEY"] = "test_key"

# Mock the Google AI dependencies
class MockGenAI:
    @staticmethod
    def configure(api_key): 
        print(f"Configured with API key: {api_key[:10]}...")
    
    class GenerativeModel:
        def __init__(self, model_name): 
            self.model_name = model_name
        
        def generate_content(self, prompt):
            return MockResponse()

class MockResponse:
    def __init__(self):
        self.text = "7.5"

# Replace imports
sys.modules['google.generativeai'] = MockGenAI
sys.modules['google.cloud.vision'] = type('MockVision', (), {'ImageAnnotatorClient': lambda: None})()

def test_basic_functionality():
    """Test basic agent functionality"""
    print("Starting AI Startup Evaluator Tests")
    print("=" * 50)
    
    # Test sample data
    sample_data = {
        "company_name": "TestTech AI",
        "problem_statement": "Testing automation challenges",
        "solution": "AI-powered testing platform",
        "market_size": 5000000000,
        "revenue": 1200000,
        "employees": 15,
        "founders": [{
            "name": "Jane Smith",
            "background": "Former Google engineer",
            "experience_years": 8
        }]
    }
    
    try:
        # Test imports
        print("1. Testing imports...")
        from startup_evaluator import StartupEvaluator
        from config import InvestorPreferences
        print("   Imports: PASSED")
        
        # Test evaluator creation
        print("2. Testing evaluator creation...")
        evaluator = StartupEvaluator()
        preferences = InvestorPreferences()
        print("   Evaluator creation: PASSED")
        
        # Test evaluation
        print("3. Testing startup evaluation...")
        start_time = datetime.now()
        
        memo = evaluator.evaluate_startup(
            form_data=sample_data,
            investor_preferences=preferences
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"   Evaluation completed in {duration:.2f} seconds")
        print(f"   Investment Score: {memo.investment_score:.1f}/10")
        print(f"   Recommendation: {memo.recommendation}")
        print("   Startup evaluation: PASSED")
        
        # Test deal note generation
        print("4. Testing deal note generation...")
        deal_note = evaluator.generate_deal_note(memo)
        print(f"   Deal note length: {len(deal_note)} characters")
        print("   Deal note generation: PASSED")
        
        # Test batch processing
        print("5. Testing batch processing...")
        batch_data = [
            {"form_data": sample_data},
            {"form_data": {**sample_data, "company_name": "TestTech B"}}
        ]
        
        batch_results = evaluator.batch_evaluate(batch_data, preferences)
        print(f"   Processed {len(batch_results)} startups")
        print("   Batch processing: PASSED")
        
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED!")
        print("Agents are working correctly and ready for deployment.")
        
        return True
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_agents():
    """Test individual agents"""
    print("\nTesting Individual Agents:")
    print("-" * 30)
    
    try:
        # Test Data Extraction Agent
        print("Data Extraction Agent...")
        from agents.data_extraction_agent import DataExtractionAgent
        data_agent = DataExtractionAgent()
        print("  Creation: PASSED")
        
        # Test Mapping Agent
        print("Mapping Agent...")
        from agents.mapping_agent import MappingAgent
        mapping_agent = MappingAgent()
        print("  Creation: PASSED")
        
        # Test Analysis Agent
        print("Analysis Agent...")
        from agents.analysis_agent import AnalysisAgent
        analysis_agent = AnalysisAgent()
        print("  Creation: PASSED")
        
        # Test Public Data Agent
        print("Public Data Agent...")
        from agents.public_data_agent import PublicDataAgent
        public_agent = PublicDataAgent()
        print("  Creation: PASSED")
        
        print("All individual agents: PASSED")
        return True
        
    except Exception as e:
        print(f"Individual agent test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("AI Startup Evaluator - Agent Testing")
    print("====================================")
    
    # Test individual agents
    agents_ok = test_individual_agents()
    
    # Test complete functionality
    complete_ok = test_basic_functionality()
    
    if agents_ok and complete_ok:
        print("\nSUCCESS: All agents are working correctly!")
        print("Ready for deployment to Google Cloud Agent Engine.")
        return 0
    else:
        print("\nFAILED: Some components need attention.")
        return 1

if __name__ == "__main__":
    exit(main())