#!/usr/bin/env python3
"""
Test the live deployed application
"""

import requests
import time

def test_live_deployment():
    """Test the live deployed application"""
    
    # The deployed URL
    url = "https://startup-evaluator-lmkuspefxq-uc.a.run.app"
    
    print("Testing Live Deployment")
    print("=" * 40)
    print(f"URL: {url}")
    
    try:
        # Test if the application is accessible
        print("1. Testing application accessibility...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            print("   Status: ACCESSIBLE")
            print(f"   Response time: {response.elapsed.total_seconds():.2f}s")
            print(f"   Content length: {len(response.content)} bytes")
            
            # Check if it's a Streamlit app
            if "streamlit" in response.text.lower() or "startup evaluator" in response.text.lower():
                print("   Type: Streamlit Application")
                print("   Status: RUNNING CORRECTLY")
            else:
                print("   Warning: May not be the expected Streamlit app")
            
            return True
            
        else:
            print(f"   Status: ERROR - HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   Status: TIMEOUT - Application may be starting up")
        return False
    except requests.exceptions.ConnectionError:
        print("   Status: CONNECTION ERROR - Application may be down")
        return False
    except Exception as e:
        print(f"   Status: ERROR - {e}")
        return False

def test_health_check():
    """Test application health"""
    url = "https://startup-evaluator-lmkuspefxq-uc.a.run.app"
    
    print("2. Testing application health...")
    
    try:
        # Test multiple requests to check stability
        response_times = []
        
        for i in range(3):
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time
            response_times.append(response_time)
            
            if response.status_code != 200:
                print(f"   Request {i+1}: FAILED - HTTP {response.status_code}")
                return False
        
        avg_response_time = sum(response_times) / len(response_times)
        print(f"   Average response time: {avg_response_time:.2f}s")
        print(f"   All requests: SUCCESSFUL")
        
        if avg_response_time < 5.0:
            print("   Performance: GOOD")
        else:
            print("   Performance: SLOW")
        
        return True
        
    except Exception as e:
        print(f"   Health check failed: {e}")
        return False

def main():
    """Run live deployment tests"""
    
    # Test accessibility
    accessible = test_live_deployment()
    
    if accessible:
        # Test health
        healthy = test_health_check()
        
        print("\n" + "=" * 40)
        print("LIVE DEPLOYMENT TEST RESULTS")
        print("=" * 40)
        
        if accessible and healthy:
            print("Status: FULLY OPERATIONAL")
            print("The AI Startup Evaluator is live and working!")
            print("\nYou can access it at:")
            print("https://startup-evaluator-lmkuspefxq-uc.a.run.app")
            return 0
        else:
            print("Status: PARTIALLY OPERATIONAL")
            print("Application is accessible but may have performance issues")
            return 1
    else:
        print("\n" + "=" * 40)
        print("LIVE DEPLOYMENT TEST RESULTS")
        print("=" * 40)
        print("Status: NOT ACCESSIBLE")
        print("Application may be starting up or experiencing issues")
        return 1

if __name__ == "__main__":
    exit(main())