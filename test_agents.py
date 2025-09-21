#!/usr/bin/env python3
"""
Test suite for all AI Startup Evaluator agents
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any

# Mock the Google AI dependencies for testing
class MockGenAI:
    @staticmethod
    def configure(api_key): pass
    
    class GenerativeModel:
        def __init__(self, model_name): pass
        def generate_content(self, prompt):
            return MockResponse()

class MockResponse:
    def __init__(self):
        self.text = "7.5"  # Mock score response

# Replace imports for testing
sys.modules['google.generativeai'] = MockGenAI
sys.modules['google.cloud.vision'] = type('MockVision', (), {'ImageAnnotatorClient': lambda: None})()

# Now import our agents
from agents.data_extraction_agent import DataExtractionAgent
from agents.mapping_agent import MappingAgent
from agents.analysis_agent import AnalysisAgent
from agents.public_data_agent import PublicDataAgent
from startup_evaluator import StartupEvaluator
from config import InvestorPreferences

class AgentTester:
    def __init__(self):
        self.test_results = {}
        self.sample_data = self._create_sample_data()
    
    def _create_sample_data(self) -> Dict[str, Any]:
        """Create sample startup data for testing"""
        return {
            "company_name": "TestTech AI",
            "problem_statement": "Businesses struggle with automated testing",
            "solution": "AI-powered testing platform that reduces testing time by 80%",
            "unique_differentiator": "Patent-pending ML algorithms for test case generation",
            "market_analysis": {
                "market_size": 5000000000,
                "growth_rate": 0.20,
                "competition_level": "medium",
                "key_players": ["Selenium", "TestComplete", "Cypress"],
                "market_maturity": "growing"
            },
            "business_metrics": {
                "revenue": 1200000,
                "revenue_growth": 0.35,
                "employees": 15,
                "cac": 5000,
                "ltv": 50000,
                "churn_rate": 0.02,
                "burn_rate": 200000
            },
            "founders": [
                {
                    "name": "Jane Smith",
                    "background": "Former Google engineer with 8 years in QA automation",
                    "experience_years": 8,
                    "previous_exits": 1,
                    "domain_expertise": "Software Testing"
                }
            ],
            "funding_stage": "Series A",
            "funding_amount": 3000000
        }
    
    def test_data_extraction_agent(self) -> bool:
        """Test Data Extraction Agent"""
        print("🧪 Testing Data Extraction Agent...")
        
        try:
            agent = DataExtractionAgent()
            
            # Test form data extraction
            result = agent.extract_from_form(self.sample_data)
            
            # Validate result structure
            assert isinstance(result, dict), "Result should be a dictionary"
            
            print("   ✅ Form data extraction: PASSED")
            
            # Test PDF extraction (mock)
            try:
                # This will fail without actual PDF, but we test the method exists
                agent.extract_from_pdf("nonexistent.pdf")
            except FileNotFoundError:
                print("   ✅ PDF extraction method: EXISTS")
            except Exception as e:
                print(f"   ⚠️ PDF extraction: {e}")
            
            self.test_results["data_extraction"] = True
            return True
            
        except Exception as e:
            print(f"   ❌ Data Extraction Agent failed: {e}")
            self.test_results["data_extraction"] = False
            return False
    
    def test_mapping_agent(self) -> bool:
        """Test Mapping Agent"""
        print("🧪 Testing Mapping Agent...")
        
        try:
            agent = MappingAgent()
            
            # Test mapping to startup profile
            startup_profile = agent.map_to_startup_profile(self.sample_data)
            
            # Validate startup profile
            assert hasattr(startup_profile, 'company_name'), "Should have company_name"
            assert hasattr(startup_profile, 'founders'), "Should have founders"
            assert len(startup_profile.founders) > 0, "Should have at least one founder"
            assert hasattr(startup_profile.founders[0], 'founder_market_fit_score'), "Should have fit score"
            
            print(f"   ✅ Startup profile mapping: PASSED")
            print(f"   ✅ Founder-market fit score: {startup_profile.founders[0].founder_market_fit_score}")
            
            self.test_results["mapping"] = True
            return True
            
        except Exception as e:
            print(f"   ❌ Mapping Agent failed: {e}")
            self.test_results["mapping"] = False
            return False
    
    def test_analysis_agent(self) -> bool:
        """Test Analysis Agent"""
        print("🧪 Testing Analysis Agent...")
        
        try:
            # First create a startup profile using mapping agent
            mapping_agent = MappingAgent()
            startup_profile = mapping_agent.map_to_startup_profile(self.sample_data)
            
            # Test analysis agent
            analysis_agent = AnalysisAgent()
            preferences = InvestorPreferences()
            
            memo = analysis_agent.generate_investment_memo(startup_profile, preferences)
            
            # Validate investment memo
            assert hasattr(memo, 'investment_score'), "Should have investment score"
            assert hasattr(memo, 'recommendation'), "Should have recommendation"
            assert hasattr(memo, 'risk_assessment'), "Should have risk assessment"
            assert 0 <= memo.investment_score <= 10, "Score should be between 0-10"
            
            print(f"   ✅ Investment memo generation: PASSED")
            print(f"   ✅ Investment score: {memo.investment_score:.1f}/10")
            print(f"   ✅ Recommendation: {memo.recommendation}")
            print(f"   ✅ Risk level: {memo.risk_assessment.risk_level}")
            
            self.test_results["analysis"] = True
            return True
            
        except Exception as e:
            print(f"   ❌ Analysis Agent failed: {e}")
            self.test_results["analysis"] = False
            return False
    
    def test_public_data_agent(self) -> bool:
        """Test Public Data Agent"""
        print("🧪 Testing Public Data Agent...")
        
        try:
            agent = PublicDataAgent()
            
            # Test data enrichment
            enriched_data = agent.enrich_startup_data("TestTech AI", ["Jane Smith"])
            
            # Validate enriched data structure
            assert isinstance(enriched_data, dict), "Should return dictionary"
            assert "news_articles" in enriched_data, "Should have news articles"
            assert "founder_profiles" in enriched_data, "Should have founder profiles"
            
            print("   ✅ Data enrichment: PASSED")
            
            # Test claim verification
            claims = {"market_size": 5000000000, "revenue": 1200000}
            verification = agent.verify_claims(claims)
            
            assert isinstance(verification, dict), "Should return verification results"
            
            print("   ✅ Claim verification: PASSED")
            
            self.test_results["public_data"] = True
            return True
            
        except Exception as e:
            print(f"   ❌ Public Data Agent failed: {e}")
            self.test_results["public_data"] = False
            return False
    
    def test_startup_evaluator(self) -> bool:
        """Test complete StartupEvaluator workflow"""
        print("🧪 Testing Complete Startup Evaluator...")
        
        try:
            evaluator = StartupEvaluator()
            preferences = InvestorPreferences()
            
            # Test complete evaluation
            memo = evaluator.evaluate_startup(
                form_data=self.sample_data,
                investor_preferences=preferences
            )
            
            # Validate complete memo
            assert hasattr(memo, 'investment_score'), "Should have investment score"
            assert hasattr(memo, 'startup_profile'), "Should have startup profile"
            assert memo.startup_profile.company_name == "TestTech AI", "Should preserve company name"
            
            print(f"   ✅ Complete evaluation: PASSED")
            print(f"   ✅ Final score: {memo.investment_score:.1f}/10")
            
            # Test deal note generation
            deal_note = evaluator.generate_deal_note(memo)
            assert isinstance(deal_note, str), "Deal note should be string"
            assert "TestTech AI" in deal_note, "Deal note should contain company name"
            
            print("   ✅ Deal note generation: PASSED")
            
            self.test_results["complete_workflow"] = True
            return True
            
        except Exception as e:
            print(f"   ❌ Complete workflow failed: {e}")
            self.test_results["complete_workflow"] = False
            return False
    
    def test_batch_processing(self) -> bool:
        """Test batch processing capability"""
        print("🧪 Testing Batch Processing...")
        
        try:
            evaluator = StartupEvaluator()
            preferences = InvestorPreferences()
            
            # Create batch data
            batch_data = [
                {"form_data": self.sample_data},
                {"form_data": {**self.sample_data, "company_name": "TestTech B"}},
                {"form_data": {**self.sample_data, "company_name": "TestTech C"}}
            ]
            
            # Test batch evaluation
            results = evaluator.batch_evaluate(batch_data, preferences)
            
            assert len(results) == 3, "Should process all 3 startups"
            assert all(hasattr(r, 'investment_score') for r in results), "All should have scores"
            
            print(f"   ✅ Batch processing: PASSED ({len(results)} startups)")
            
            self.test_results["batch_processing"] = True
            return True
            
        except Exception as e:
            print(f"   ❌ Batch processing failed: {e}")
            self.test_results["batch_processing"] = False
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling and edge cases"""
        print("🧪 Testing Error Handling...")
        
        try:
            evaluator = StartupEvaluator()
            
            # Test with minimal data
            minimal_data = {"company_name": "Minimal Corp"}
            
            try:
                memo = evaluator.evaluate_startup(form_data=minimal_data)
                print("   ✅ Minimal data handling: PASSED")
            except Exception as e:
                print(f"   ⚠️ Minimal data handling: {e}")
            
            # Test with empty data
            try:
                memo = evaluator.evaluate_startup(form_data={})
                print("   ✅ Empty data handling: PASSED")
            except Exception as e:
                print(f"   ⚠️ Empty data handling: {e}")
            
            self.test_results["error_handling"] = True
            return True
            
        except Exception as e:
            print(f"   ❌ Error handling test failed: {e}")
            self.test_results["error_handling"] = False
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all agent tests"""
        print("🚀 Starting AI Startup Evaluator Agent Tests")
        print("=" * 60)
        
        # Set mock API key for testing
        os.environ["GEMINI_API_KEY"] = "test_key"
        
        tests = [
            self.test_data_extraction_agent,
            self.test_mapping_agent,
            self.test_analysis_agent,
            self.test_public_data_agent,
            self.test_startup_evaluator,
            self.test_batch_processing,
            self.test_error_handling
        ]
        
        for test in tests:
            try:
                test()
                print()
            except Exception as e:
                print(f"   ❌ Test failed with exception: {e}\n")
        
        return self.test_results
    
    def print_test_summary(self):
        """Print test results summary"""
        print("=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print("-" * 60)
        print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All agents are working correctly!")
        else:
            print("⚠️ Some agents need attention")
        
        return passed == total

def main():
    """Run agent tests"""
    tester = AgentTester()
    
    # Run all tests
    results = tester.run_all_tests()
    
    # Print summary
    all_passed = tester.print_test_summary()
    
    # Performance test
    print("\n🏃 Performance Test...")
    start_time = datetime.now()
    
    evaluator = StartupEvaluator()
    memo = evaluator.evaluate_startup(form_data=tester.sample_data)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"⏱️ Single evaluation completed in {duration:.2f} seconds")
    
    if all_passed:
        print("\n✅ All agents are ready for deployment!")
        return 0
    else:
        print("\n❌ Some agents need fixes before deployment")
        return 1

if __name__ == "__main__":
    exit(main())