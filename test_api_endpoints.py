#!/usr/bin/env python3
"""
Test script for SMS Spam Detection API endpoints
Tests both /predict and /api/predict routes
"""

import requests
import json
import time

# Base URL for local Flask app
BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(endpoint, message):
    """Test a specific endpoint with a message"""
    url = f"{BASE_URL}{endpoint}"
    data = {"message": message}
    
    try:
        print(f"\n🔍 Testing {endpoint}")
        print(f"📧 Message: {message}")
        
        response = requests.post(url, json=data)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Could not connect to {url}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing SMS Spam Detection API Endpoints")
    print("=" * 50)
    
    # Wait a moment for Flask to fully start
    time.sleep(2)
    
    # Test messages
    test_messages = [
        "Hey! How are you doing today?",  # Ham
        "CONGRATULATIONS! You've won $1000! Click here to claim your prize NOW!",  # Spam
        "Meeting at 3pm in conference room B",  # Ham
        "FREE VIAGRA! Call now! Limited time offer!"  # Spam
    ]
    
    endpoints = ["/predict", "/api/predict"]
    
    success_count = 0
    total_tests = len(endpoints) * len(test_messages)
    
    for endpoint in endpoints:
        print(f"\n{'='*20} {endpoint} {'='*20}")
        
        for message in test_messages:
            if test_endpoint(endpoint, message):
                success_count += 1
            time.sleep(0.5)  # Small delay between requests
    
    print(f"\n{'='*50}")
    print(f"🎯 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! Both endpoints are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()