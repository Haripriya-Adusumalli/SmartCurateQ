#!/usr/bin/env python3

from startup_evaluator import StartupEvaluator
from config import InvestorPreferences

def test_evaluation():
    try:
        evaluator = StartupEvaluator()
        
        form_data = {
            "company_name": "Test Company",
            "problem_statement": "Test problem",
            "solution": "Test solution",
            "market_size": 1000000000,
            "revenue": 100000,
            "employees": 5,
            "funding_stage": "Seed",
            "founders": [{
                "name": "Test Founder",
                "background": "Test background",
                "experience_years": 5,
                "previous_exits": 0,
                "domain_expertise": "Business"
            }]
        }
        
        preferences = InvestorPreferences()
        
        print("Starting evaluation...")
        memo = evaluator.evaluate_startup(form_data=form_data, investor_preferences=preferences)
        
        print(f"Success! Company: {memo.startup_profile.company_name}")
        print(f"Score: {memo.investment_score}")
        print(f"Problem: {memo.startup_profile.problem_statement}")
        print(f"Solution: {memo.startup_profile.solution}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_evaluation()