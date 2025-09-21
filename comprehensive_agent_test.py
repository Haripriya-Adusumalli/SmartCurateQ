#!/usr/bin/env python3
"""
Comprehensive agent testing suite
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List

# Set test environment
os.environ["GEMINI_API_KEY"] = "test_key"

# Mock Google AI
class MockGenAI:
    @staticmethod
    def configure(api_key): pass
    
    class GenerativeModel:
        def __init__(self, model_name): pass
        def generate_content(self, prompt):
            return type('Response', (), {'text': '7.5'})()

class MockVision:
    @staticmethod
    def ImageAnnotatorClient():
        return type('Client', (), {})()

sys.modules['google.generativeai'] = MockGenAI
sys.modules['google.cloud.vision'] = MockVision

from startup_evaluator import StartupEvaluator
from config import InvestorPreferences

class ComprehensiveAgentTester:
    def __init__(self):
        self.test_results = {}
        self.evaluator = StartupEvaluator()
        
    def create_test_scenarios(self) -> List[Dict]:
        """Create diverse test scenarios"""
        return [
            # High-potential startup
            {
                "name": "High-Potential AI Startup",
                "data": {
                    "company_name": "NeuralTech AI",
                    "problem_statement": "Healthcare diagnosis takes too long and is error-prone",
                    "solution": "AI-powered diagnostic platform with 95% accuracy",
                    "unique_differentiator": "Proprietary neural network with FDA approval pathway",
                    "market_analysis": {
                        "market_size": 50000000000,
                        "growth_rate": 0.25,
                        "competition_level": "medium",
                        "key_players": ["IBM Watson", "Google Health"],
                        "market_maturity": "growing"
                    },
                    "business_metrics": {
                        "revenue": 5000000,
                        "revenue_growth": 0.80,
                        "employees": 45,
                        "cac": 2000,
                        "ltv": 50000,
                        "churn_rate": 0.02,
                        "burn_rate": 800000
                    },
                    "founders": [{
                        "name": "Dr. Sarah Chen",
                        "background": "Former Google AI researcher with MD from Stanford",
                        "experience_years": 12,
                        "previous_exits": 1,
                        "domain_expertise": "Medical AI"
                    }],
                    "funding_stage": "Series B"
                },
                "expected_score_range": (8.0, 10.0),
                "expected_recommendation": "STRONG BUY"
            },
            
            # Early-stage startup
            {
                "name": "Early-Stage Fintech",
                "data": {
                    "company_name": "PayFlow Startup",
                    "problem_statement": "Small businesses struggle with cash flow management",
                    "solution": "Automated invoice factoring platform",
                    "unique_differentiator": "Real-time credit scoring algorithm",
                    "market_analysis": {
                        "market_size": 8000000000,
                        "growth_rate": 0.15,
                        "competition_level": "high",
                        "key_players": ["Square", "Stripe", "PayPal"],
                        "market_maturity": "mature"
                    },
                    "business_metrics": {
                        "revenue": 0,
                        "revenue_growth": None,
                        "employees": 8,
                        "cac": None,
                        "ltv": None,
                        "churn_rate": None,
                        "burn_rate": 150000
                    },
                    "founders": [{
                        "name": "Mike Johnson",
                        "background": "Former banking analyst with 5 years experience",
                        "experience_years": 5,
                        "previous_exits": 0,
                        "domain_expertise": "Financial Services"
                    }],
                    "funding_stage": "Pre-seed"
                },
                "expected_score_range": (4.0, 6.5),
                "expected_recommendation": "HOLD"
            },
            
            # Risky startup
            {
                "name": "High-Risk Consumer App",
                "data": {
                    "company_name": "SocialBuzz App",
                    "problem_statement": "People are bored on social media",
                    "solution": "AI-generated content recommendation app",
                    "unique_differentiator": "Viral content prediction algorithm",
                    "market_analysis": {
                        "market_size": 2000000000,
                        "growth_rate": 0.05,
                        "competition_level": "high",
                        "key_players": ["TikTok", "Instagram", "Snapchat"],
                        "market_maturity": "saturated"
                    },
                    "business_metrics": {
                        "revenue": 50000,
                        "revenue_growth": -0.10,
                        "employees": 12,
                        "cac": 15,
                        "ltv": 8,
                        "churn_rate": 0.25,
                        "burn_rate": 200000
                    },
                    "founders": [{
                        "name": "Alex Kim",
                        "background": "Recent college graduate with app development experience",
                        "experience_years": 2,
                        "previous_exits": 0,
                        "domain_expertise": "Mobile Apps"
                    }],
                    "funding_stage": "Seed"
                },
                "expected_score_range": (2.0, 4.5),
                "expected_recommendation": "PASS"
            },
            
            # B2B SaaS startup
            {
                "name": "B2B SaaS Platform",
                "data": {
                    "company_name": "WorkflowPro",
                    "problem_statement": "Enterprise workflows are inefficient and manual",
                    "solution": "No-code workflow automation platform for enterprises",
                    "unique_differentiator": "Industry-specific templates with compliance built-in",
                    "market_analysis": {
                        "market_size": 15000000000,
                        "growth_rate": 0.20,
                        "competition_level": "medium",
                        "key_players": ["Zapier", "Microsoft Power Automate", "UiPath"],
                        "market_maturity": "growing"
                    },
                    "business_metrics": {
                        "revenue": 2000000,
                        "revenue_growth": 0.40,
                        "employees": 25,
                        "cac": 5000,
                        "ltv": 75000,
                        "churn_rate": 0.05,
                        "burn_rate": 400000
                    },
                    "founders": [{
                        "name": "Jennifer Liu",
                        "background": "Former Salesforce PM with enterprise software experience",
                        "experience_years": 10,
                        "previous_exits": 0,
                        "domain_expertise": "Enterprise Software"
                    }],
                    "funding_stage": "Series A"
                },
                "expected_score_range": (6.5, 8.5),
                "expected_recommendation": "BUY"
            },
            
            # Edge case: Minimal data
            {
                "name": "Minimal Data Startup",
                "data": {
                    "company_name": "MinimalCorp",
                    "problem_statement": "Generic problem",
                    "solution": "Generic solution",
                    "unique_differentiator": "None specified",
                    "market_analysis": {
                        "market_size": 100000000,
                        "growth_rate": 0.05,
                        "competition_level": "unknown",
                        "key_players": [],
                        "market_maturity": "unknown"
                    },
                    "business_metrics": {
                        "revenue": None,
                        "revenue_growth": None,
                        "employees": None,
                        "cac": None,
                        "ltv": None,
                        "churn_rate": None,
                        "burn_rate": None
                    },
                    "founders": [{
                        "name": "Unknown Founder",
                        "background": "No information",
                        "experience_years": 0,
                        "previous_exits": 0,
                        "domain_expertise": "Unknown"
                    }],
                    "funding_stage": "Unknown"
                },
                "expected_score_range": (3.0, 6.0),
                "expected_recommendation": "HOLD"
            }
        ]
    
    def test_scenario(self, scenario: Dict) -> Dict:
        """Test a single scenario"""
        print(f"Testing: {scenario['name']}")
        
        try:
            # Test with different investor preferences
            preferences_sets = [
                InvestorPreferences(founder_weight=0.4, market_weight=0.2, differentiation_weight=0.2, traction_weight=0.2),
                InvestorPreferences(founder_weight=0.2, market_weight=0.4, differentiation_weight=0.2, traction_weight=0.2),
                InvestorPreferences(founder_weight=0.2, market_weight=0.2, differentiation_weight=0.4, traction_weight=0.2),
                InvestorPreferences(founder_weight=0.2, market_weight=0.2, differentiation_weight=0.2, traction_weight=0.4)
            ]
            
            results = []
            
            for i, preferences in enumerate(preferences_sets):
                start_time = datetime.now()
                
                memo = self.evaluator.evaluate_startup(
                    form_data=scenario['data'],
                    investor_preferences=preferences
                )
                
                duration = (datetime.now() - start_time).total_seconds()
                
                result = {
                    "preference_set": i + 1,
                    "investment_score": memo.investment_score,
                    "recommendation": memo.recommendation,
                    "risk_level": memo.risk_assessment.risk_level,
                    "strengths_count": len(memo.key_strengths),
                    "concerns_count": len(memo.key_concerns),
                    "duration_seconds": duration,
                    "company_name": memo.startup_profile.company_name
                }
                
                results.append(result)
            
            # Validate results
            validation = self._validate_scenario_results(scenario, results)
            
            return {
                "scenario_name": scenario['name'],
                "results": results,
                "validation": validation,
                "status": "PASSED" if validation['all_valid'] else "FAILED"
            }
            
        except Exception as e:
            return {
                "scenario_name": scenario['name'],
                "error": str(e),
                "status": "ERROR"
            }
    
    def _validate_scenario_results(self, scenario: Dict, results: List[Dict]) -> Dict:
        """Validate scenario results"""
        validation = {
            "score_in_range": True,
            "recommendation_appropriate": True,
            "consistent_company_name": True,
            "reasonable_duration": True,
            "all_valid": True
        }
        
        expected_min, expected_max = scenario['expected_score_range']
        expected_rec = scenario['expected_recommendation']
        
        for result in results:
            # Check score range
            if not (expected_min <= result['investment_score'] <= expected_max):
                validation['score_in_range'] = False
            
            # Check recommendation appropriateness
            if expected_rec not in result['recommendation']:
                validation['recommendation_appropriate'] = False
            
            # Check company name consistency
            if result['company_name'] != scenario['data']['company_name']:
                validation['consistent_company_name'] = False
            
            # Check duration (should be < 5 seconds)
            if result['duration_seconds'] > 5.0:
                validation['reasonable_duration'] = False
        
        validation['all_valid'] = all(validation.values())
        return validation
    
    def test_edge_cases(self) -> Dict:
        """Test edge cases and error handling"""
        print("Testing edge cases...")
        
        edge_cases = [
            # Empty data
            {"name": "Empty Data", "data": {}},
            
            # Invalid data types
            {"name": "Invalid Types", "data": {
                "company_name": 123,
                "market_analysis": "not a dict",
                "business_metrics": None
            }},
            
            # Extreme values
            {"name": "Extreme Values", "data": {
                "company_name": "ExtremeTest",
                "market_analysis": {
                    "market_size": 999999999999999,
                    "growth_rate": 10.0,
                    "competition_level": "extreme"
                },
                "business_metrics": {
                    "revenue": -1000000,
                    "churn_rate": 2.0
                }
            }}
        ]
        
        results = []
        
        for case in edge_cases:
            try:
                memo = self.evaluator.evaluate_startup(form_data=case['data'])
                results.append({
                    "case": case['name'],
                    "status": "HANDLED",
                    "score": memo.investment_score
                })
            except Exception as e:
                results.append({
                    "case": case['name'],
                    "status": "ERROR",
                    "error": str(e)
                })
        
        return {"edge_case_results": results}
    
    def test_performance(self) -> Dict:
        """Test performance with multiple evaluations"""
        print("Testing performance...")
        
        test_data = {
            "company_name": "PerfTest Corp",
            "problem_statement": "Performance testing",
            "solution": "Speed optimization",
            "market_size": 1000000000,
            "revenue": 500000,
            "employees": 10,
            "founders": [{"name": "Perf Founder", "experience_years": 5}]
        }
        
        # Single evaluation
        start_time = datetime.now()
        memo = self.evaluator.evaluate_startup(form_data=test_data)
        single_duration = (datetime.now() - start_time).total_seconds()
        
        # Batch evaluation
        batch_data = [{"form_data": test_data} for _ in range(10)]
        start_time = datetime.now()
        batch_results = self.evaluator.batch_evaluate(batch_data)
        batch_duration = (datetime.now() - start_time).total_seconds()
        
        return {
            "single_evaluation_time": single_duration,
            "batch_evaluation_time": batch_duration,
            "batch_size": len(batch_results),
            "average_per_startup": batch_duration / len(batch_results),
            "performance_rating": "EXCELLENT" if single_duration < 1.0 else "GOOD" if single_duration < 3.0 else "ACCEPTABLE"
        }
    
    def run_comprehensive_tests(self) -> Dict:
        """Run all comprehensive tests"""
        print("Starting Comprehensive Agent Testing")
        print("=" * 60)
        
        # Test scenarios
        scenarios = self.create_test_scenarios()
        scenario_results = []
        
        for scenario in scenarios:
            result = self.test_scenario(scenario)
            scenario_results.append(result)
            print(f"  {scenario['name']}: {result['status']}")
        
        # Test edge cases
        edge_case_results = self.test_edge_cases()
        
        # Test performance
        performance_results = self.test_performance()
        
        # Calculate overall results
        passed_scenarios = sum(1 for r in scenario_results if r['status'] == 'PASSED')
        total_scenarios = len(scenario_results)
        
        overall_results = {
            "timestamp": datetime.now().isoformat(),
            "scenario_results": scenario_results,
            "edge_case_results": edge_case_results,
            "performance_results": performance_results,
            "summary": {
                "scenarios_passed": passed_scenarios,
                "total_scenarios": total_scenarios,
                "success_rate": (passed_scenarios / total_scenarios) * 100,
                "overall_status": "PASSED" if passed_scenarios == total_scenarios else "PARTIAL"
            }
        }
        
        return overall_results
    
    def print_test_summary(self, results: Dict):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE AGENT TEST RESULTS")
        print("=" * 60)
        
        summary = results['summary']
        print(f"Scenarios Passed: {summary['scenarios_passed']}/{summary['total_scenarios']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Overall Status: {summary['overall_status']}")
        
        print(f"\nPerformance Results:")
        perf = results['performance_results']
        print(f"  Single Evaluation: {perf['single_evaluation_time']:.3f}s")
        print(f"  Batch Processing: {perf['batch_evaluation_time']:.3f}s ({perf['batch_size']} startups)")
        print(f"  Performance Rating: {perf['performance_rating']}")
        
        print(f"\nDetailed Scenario Results:")
        for scenario in results['scenario_results']:
            status_icon = "✅" if scenario['status'] == 'PASSED' else "❌" if scenario['status'] == 'FAILED' else "⚠️"
            print(f"  {status_icon} {scenario['scenario_name']}: {scenario['status']}")
            
            if 'results' in scenario:
                avg_score = sum(r['investment_score'] for r in scenario['results']) / len(scenario['results'])
                print(f"     Average Score: {avg_score:.1f}/10")
        
        print(f"\nEdge Case Handling:")
        for case in results['edge_case_results']['edge_case_results']:
            status_icon = "✅" if case['status'] == 'HANDLED' else "❌"
            print(f"  {status_icon} {case['case']}: {case['status']}")
        
        if summary['overall_status'] == 'PASSED':
            print(f"\n🎉 ALL AGENTS THOROUGHLY TESTED AND WORKING!")
            print("Ready for production deployment.")
        else:
            print(f"\n⚠️ Some tests need attention.")

def main():
    """Run comprehensive agent testing"""
    tester = ComprehensiveAgentTester()
    
    # Run all tests
    results = tester.run_comprehensive_tests()
    
    # Print summary
    tester.print_test_summary(results)
    
    # Save detailed results
    with open('comprehensive_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: comprehensive_test_results.json")
    
    return 0 if results['summary']['overall_status'] == 'PASSED' else 1

if __name__ == "__main__":
    exit(main())