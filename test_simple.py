#!/usr/bin/env python3

import os
from startup_evaluator import StartupEvaluator
from config import InvestorPreferences

def test_simple_evaluation():
    """Simple test of the evaluation pipeline"""
    
    # Test with form data only (no PDF)
    form_data = {
        "company_name": "Test Company",
        "problem_statement": "Test problem",
        "solution": "Test solution",
        "market_size": 1000000000,
        "revenue": 0,
        "employees": 5
    }
    
    print("Creating evaluator...")
    evaluator = StartupEvaluator()
    
    print("Running evaluation...")
    preferences = InvestorPreferences()
    
    try:
        memo = evaluator.evaluate_startup(
            form_data=form_data,
            investor_preferences=preferences
        )
        
        print(f"SUCCESS: Investment Score: {memo.investment_score:.1f}/10")
        print(f"Recommendation: {memo.recommendation}")
        print(f"Company: {memo.startup_profile.company_name}")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_evaluation()