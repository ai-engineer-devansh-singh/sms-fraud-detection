#!/usr/bin/env python3
"""
Test script for the Flask SMS Spam Detection API
"""

import requests
import json
import sys

def test_api():
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test prediction endpoint with ham message
    print("\n🔍 Testing prediction with HAM message...")
    ham_message = "Hey, are we still meeting for lunch today?"
    try:
        response = requests.post(
            f"{base_url}/predict",
            json={"text": ham_message},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Prediction: {result.get('prediction', 'N/A')}")
        print(f"Confidence: {result.get('confidence_percentage', 'N/A')}")
    except Exception as e:
        print(f"❌ HAM prediction failed: {e}")
        return False
    
    # Test prediction endpoint with spam message
    print("\n🔍 Testing prediction with SPAM message...")
    spam_message = "URGENT! You have won $1000! Click here to claim your prize now!"
    try:
        response = requests.post(
            f"{base_url}/predict",
            json={"text": spam_message},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Prediction: {result.get('prediction', 'N/A')}")
        print(f"Confidence: {result.get('confidence_percentage', 'N/A')}")
    except Exception as e:
        print(f"❌ SPAM prediction failed: {e}")
        return False
    
    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    if not test_api():
        sys.exit(1)