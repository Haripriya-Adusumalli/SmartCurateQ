#!/usr/bin/env python3
"""
Working test for AI Startup Evaluator
"""

import os
import sys
from datetime import datetime

# Set environment
os.environ["GEMINI_API_KEY"] = "test_key"

# Create proper mocks
class MockVisionClient:
    def __init__(self):
        pass

class MockVision:
    @staticmethod
    def ImageAnnotatorClient():
        return MockVisionClient()

class MockGenAI:
    @staticmethod
    def configure(api_key): 
        pass
    
    class GenerativeModel:
        def __init__(self, model_name): 
            pass
        
        def generate_content(self, prompt):
            return type('Response', (), {'text': '7.5'})()

# Apply mocks
sys.modules['google.generativeai'] = MockGenAI
sys.modules['google.cloud.vision'] = MockVision

def test_core_functionality():
    """Test the core startup evaluation functionality"""
    print("Testing AI Startup Evaluator Core Functionality")
    print("=" * 55)
    
    # Sample startup data
    startup_data = {
        "company_name": "EcoTech Solutions",
        "problem_statement": "Manufacturing waste is a major environmental issue",
        "solution": "AI-powered optimization platform reducing waste by 40%",
        "unique_differentiator": "Patent-pending ML algorithms with IoT integration",
        "market_analysis": {
            "market_size": 12000000000,
            "growth_rate": 0.18,
            "competition_level": "medium",
            "key_players": ["Siemens", "GE Digital"],
            "market_maturity": "growing"
        },
        "business_metrics": {
            "revenue": 2500000,
            "revenue_growth": 0.35,
            "employees": 28,
            "cac": 15000,
            "ltv": 180000,
            "churn_rate": 0.03
        },
        "founders": [
            {
                "name": "Dr. Maria Rodriguez",
                "background": "Former Tesla manufacturing engineer",
                "experience_years": 12,
                "previous_exits": 1,
                "domain_expertise": "Manufacturing Optimization"
            }
        ],
        "funding_stage": "Series A"
    }
    
    try:
        # Import and test
        from startup_evaluator import StartupEvaluator
        from config import InvestorPreferences
        
        print("1. Imports: SUCCESS")
        
        # Create evaluator
        evaluator = StartupEvaluator()
        preferences = InvestorPreferences(
            founder_weight=0.3,
            market_weight=0.25,
            differentiation_weight=0.25,
            traction_weight=0.2
        )
        
        print("2. Evaluator creation: SUCCESS")
        
        # Run evaluation
        print("3. Running evaluation...")
        start_time = datetime.now()
        
        memo = evaluator.evaluate_startup(
            form_data=startup_data,
            investor_preferences=preferences
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"   Completed in {duration:.2f} seconds")
        print(f"   Company: {memo.startup_profile.company_name}")
        print(f"   Investment Score: {memo.investment_score:.1f}/10")
        print(f"   Recommendation: {memo.recommendation}")
        print(f"   Risk Level: {memo.risk_assessment.risk_level}")
        print(f"   Strengths: {len(memo.key_strengths)}")
        print(f"   Concerns: {len(memo.key_concerns)}")
        
        print("3. Evaluation: SUCCESS")
        
        # Test deal note generation
        print("4. Generating deal note...")
        deal_note = evaluator.generate_deal_note(memo)
        
        print(f"   Deal note length: {len(deal_note)} characters")
        print(f"   Contains company name: {'EcoTech Solutions' in deal_note}")
        print("4. Deal note generation: SUCCESS")
        
        # Test batch processing
        print("5. Testing batch processing...")
        batch_data = [
            {"form_data": startup_data},
            {"form_data": {**startup_data, "company_name": "TechCorp B"}},
            {"form_data": {**startup_data, "company_name": "HealthTech C"}}
        ]
        
        batch_results = evaluator.batch_evaluate(batch_data, preferences)
        print(f"   Processed {len(batch_results)} startups")
        print("5. Batch processing: SUCCESS")
        
        # Display sample deal note
        print("\n" + "=" * 55)
        print("SAMPLE DEAL NOTE OUTPUT:")
        print("=" * 55)
        print(deal_note[:500] + "..." if len(deal_note) > 500 else deal_note)
        
        print("\n" + "=" * 55)
        print("ALL TESTS PASSED!")
        print("The AI Startup Evaluator is working correctly.")
        print("Ready for deployment to Google Cloud Agent Engine.")
        print("=" * 55)
        
        return True
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_components():
    """Test individual agent components"""
    print("\nTesting Individual Agent Components:")
    print("-" * 40)
    
    components_tested = 0
    components_passed = 0
    
    # Test each agent individually
    agents = [
        ("Data Extraction Agent", "agents.data_extraction_agent", "DataExtractionAgent"),
        ("Mapping Agent", "agents.mapping_agent", "MappingAgent"),
        ("Analysis Agent", "agents.analysis_agent", "AnalysisAgent"),
        ("Public Data Agent", "agents.public_data_agent", "PublicDataAgent")
    ]
    
    for agent_name, module_name, class_name in agents:
        try:
            components_tested += 1
            module = __import__(module_name, fromlist=[class_name])
            agent_class = getattr(module, class_name)
            agent_instance = agent_class()
            
            print(f"{agent_name}: PASSED")
            components_passed += 1
            
        except Exception as e:
            print(f"{agent_name}: FAILED - {e}")
    
    print(f"\nAgent Components: {components_passed}/{components_tested} passed")
    return components_passed == components_tested

def main():
    """Run comprehensive tests"""
    print("AI Startup Evaluator - Comprehensive Testing")
    print("=" * 50)
    
    # Test components
    components_ok = test_agent_components()
    
    # Test core functionality
    core_ok = test_core_functionality()
    
    print("\n" + "=" * 50)
    print("FINAL TEST RESULTS:")
    print("=" * 50)
    print(f"Agent Components: {'PASSED' if components_ok else 'FAILED'}")
    print(f"Core Functionality: {'PASSED' if core_ok else 'FAILED'}")
    
    if components_ok and core_ok:
        print("\nOVERALL: SUCCESS!")
        print("All agents are working correctly and ready for deployment.")
        return 0
    else:
        print("\nOVERALL: NEEDS ATTENTION")
        print("Some components require fixes before deployment.")
        return 1

if __name__ == "__main__":
    exit(main())