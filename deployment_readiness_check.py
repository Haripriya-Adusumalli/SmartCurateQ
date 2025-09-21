#!/usr/bin/env python3
"""
Final deployment readiness check for AI Startup Evaluator
"""

import os
import sys
from datetime import datetime

# Set test environment
os.environ["GEMINI_API_KEY"] = "test_key"

def check_deployment_readiness():
    """Comprehensive deployment readiness check"""
    
    print("AI Startup Evaluator - Deployment Readiness Check")
    print("=" * 55)
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Core Dependencies
    print("1. Checking core dependencies...")
    total_checks += 1
    try:
        import streamlit
        import pandas
        import pydantic
        print("   Core dependencies: AVAILABLE")
        checks_passed += 1
    except ImportError as e:
        print(f"   Core dependencies: MISSING - {e}")
    
    # Check 2: Agent System
    print("2. Checking agent system...")
    total_checks += 1
    try:
        from startup_evaluator import StartupEvaluator
        evaluator = StartupEvaluator()
        print("   Agent system: OPERATIONAL")
        checks_passed += 1
    except Exception as e:
        print(f"   Agent system: FAILED - {e}")
    
    # Check 3: End-to-End Evaluation
    print("3. Testing end-to-end evaluation...")
    total_checks += 1
    try:
        from config import InvestorPreferences
        
        sample_data = {
            "company_name": "DeployTest Corp",
            "problem_statement": "Testing deployment readiness",
            "solution": "Automated testing platform",
            "market_size": 3000000000,
            "revenue": 800000,
            "employees": 12,
            "founders": [{"name": "Test Founder", "background": "Tech expert", "experience_years": 5}]
        }
        
        preferences = InvestorPreferences()
        memo = evaluator.evaluate_startup(form_data=sample_data, investor_preferences=preferences)
        
        # Validate memo
        assert hasattr(memo, 'investment_score')
        assert hasattr(memo, 'recommendation')
        assert hasattr(memo, 'startup_profile')
        assert 0 <= memo.investment_score <= 10
        
        print(f"   End-to-end evaluation: SUCCESS")
        print(f"   Sample score: {memo.investment_score:.1f}/10")
        checks_passed += 1
        
    except Exception as e:
        print(f"   End-to-end evaluation: FAILED - {e}")
    
    # Check 4: Deal Note Generation
    print("4. Testing deal note generation...")
    total_checks += 1
    try:
        deal_note = evaluator.generate_deal_note(memo)
        assert isinstance(deal_note, str)
        assert len(deal_note) > 100
        assert "DeployTest Corp" in deal_note
        
        print("   Deal note generation: SUCCESS")
        checks_passed += 1
        
    except Exception as e:
        print(f"   Deal note generation: FAILED - {e}")
    
    # Check 5: Batch Processing
    print("5. Testing batch processing...")
    total_checks += 1
    try:
        batch_data = [
            {"form_data": sample_data},
            {"form_data": {**sample_data, "company_name": "BatchTest B"}}
        ]
        
        batch_results = evaluator.batch_evaluate(batch_data, preferences)
        assert len(batch_results) == 2
        assert all(hasattr(r, 'investment_score') for r in batch_results)
        
        print(f"   Batch processing: SUCCESS ({len(batch_results)} processed)")
        checks_passed += 1
        
    except Exception as e:
        print(f"   Batch processing: FAILED - {e}")
    
    # Check 6: Configuration Files
    print("6. Checking configuration files...")
    total_checks += 1
    try:
        config_files = [
            "requirements.txt",
            "Dockerfile", 
            "cloudbuild.yaml",
            "agent_deployment/deploy_agents.py",
            "agent_deployment/agent_client.py"
        ]
        
        missing_files = []
        for file in config_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if not missing_files:
            print("   Configuration files: COMPLETE")
            checks_passed += 1
        else:
            print(f"   Configuration files: MISSING - {missing_files}")
            
    except Exception as e:
        print(f"   Configuration files: ERROR - {e}")
    
    # Check 7: Agent Deployment Configs
    print("7. Checking agent deployment configs...")
    total_checks += 1
    try:
        agent_configs = [
            "agent_deployment/data_extraction_agent.yaml",
            "agent_deployment/mapping_agent.yaml",
            "agent_deployment/analysis_agent.yaml",
            "agent_deployment/public_data_agent.yaml",
            "agent_deployment/voice_agent.yaml",
            "agent_deployment/orchestrator_agent.yaml"
        ]
        
        missing_configs = []
        for config in agent_configs:
            if not os.path.exists(config):
                missing_configs.append(config)
        
        if not missing_configs:
            print("   Agent deployment configs: COMPLETE")
            checks_passed += 1
        else:
            print(f"   Agent deployment configs: MISSING - {missing_configs}")
            
    except Exception as e:
        print(f"   Agent deployment configs: ERROR - {e}")
    
    # Final Assessment
    print("\n" + "=" * 55)
    print("DEPLOYMENT READINESS ASSESSMENT")
    print("=" * 55)
    
    success_rate = (checks_passed / total_checks) * 100
    
    print(f"Checks Passed: {checks_passed}/{total_checks} ({success_rate:.1f}%)")
    
    if checks_passed == total_checks:
        print("\n✅ READY FOR DEPLOYMENT!")
        print("All systems operational. Proceed with Google Cloud deployment.")
        
        print("\nDeployment Commands:")
        print("1. Set environment: export GOOGLE_CLOUD_PROJECT=your-project-id")
        print("2. Deploy agents: cd agent_deployment && ./deploy.sh")
        print("3. Deploy app: gcloud builds submit --config cloudbuild.yaml")
        
        return True
    else:
        print(f"\n⚠️ DEPLOYMENT READINESS: {success_rate:.1f}%")
        print("Some components need attention before deployment.")
        return False

def performance_benchmark():
    """Run performance benchmark"""
    print("\n" + "=" * 55)
    print("PERFORMANCE BENCHMARK")
    print("=" * 55)
    
    try:
        from startup_evaluator import StartupEvaluator
        from config import InvestorPreferences
        
        evaluator = StartupEvaluator()
        preferences = InvestorPreferences()
        
        sample_data = {
            "company_name": "PerfTest Corp",
            "problem_statement": "Performance testing",
            "solution": "High-speed evaluation",
            "market_size": 2000000000,
            "revenue": 1000000,
            "employees": 20,
            "founders": [{"name": "Perf Founder", "background": "Speed expert", "experience_years": 7}]
        }
        
        # Single evaluation benchmark
        start_time = datetime.now()
        memo = evaluator.evaluate_startup(form_data=sample_data, investor_preferences=preferences)
        single_duration = (datetime.now() - start_time).total_seconds()
        
        # Batch evaluation benchmark
        batch_data = [{"form_data": sample_data} for _ in range(5)]
        start_time = datetime.now()
        batch_results = evaluator.batch_evaluate(batch_data, preferences)
        batch_duration = (datetime.now() - start_time).total_seconds()
        
        print(f"Single Evaluation: {single_duration:.3f} seconds")
        print(f"Batch Evaluation (5 startups): {batch_duration:.3f} seconds")
        print(f"Average per startup: {batch_duration/5:.3f} seconds")
        
        # Performance assessment
        if single_duration < 1.0:
            print("Performance: EXCELLENT (< 1 second)")
        elif single_duration < 3.0:
            print("Performance: GOOD (< 3 seconds)")
        else:
            print("Performance: ACCEPTABLE (> 3 seconds)")
            
    except Exception as e:
        print(f"Performance benchmark failed: {e}")

def main():
    """Run deployment readiness check"""
    
    ready = check_deployment_readiness()
    performance_benchmark()
    
    print("\n" + "=" * 55)
    if ready:
        print("🚀 SYSTEM READY FOR DEPLOYMENT!")
        print("All agents tested and operational.")
        return 0
    else:
        print("⚠️ SYSTEM NEEDS ATTENTION")
        print("Fix issues before deployment.")
        return 1

if __name__ == "__main__":
    exit(main())