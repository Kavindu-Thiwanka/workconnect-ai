#!/usr/bin/env python3
"""
Test script to verify AI service integration with WorkConnect API
This script tests the communication between the Java backend and Python AI service
"""

import requests
import json
import sys
import time

# Configuration
AI_SERVICE_URL = "http://localhost:8000"
API_SERVICE_URL = "http://localhost:8080"

def test_ai_service_health():
    """Test if AI service is running"""
    try:
        response = requests.get(f"{AI_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI Service is running")
            return True
        else:
            print(f"❌ AI Service health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI Service is not accessible: {e}")
        return False

def test_ai_recommendations():
    """Test AI recommendations endpoint directly"""
    test_data = {
        "worker_profile": {
            "skills": "Java Spring Boot Python"
        },
        "job_postings": [
            {
                "id": 1,
                "required_skills": "Java Spring Boot REST API"
            },
            {
                "id": 2,
                "required_skills": "Python Django Machine Learning"
            },
            {
                "id": 3,
                "required_skills": "JavaScript React Frontend"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{AI_SERVICE_URL}/recommendations/jobs",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI Recommendations endpoint working")
            print(f"   Ranked job IDs: {result.get('ranked_job_ids', [])}")
            return True
        else:
            print(f"❌ AI Recommendations failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI Recommendations request failed: {e}")
        return False

def test_api_service_health():
    """Test if API service is running"""
    try:
        response = requests.get(f"{API_SERVICE_URL}/api/recommendations/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Service recommendations endpoint is accessible")
            return True
        elif response.status_code == 403:
            print("✅ API Service is running (authentication required - expected)")
            return True
        else:
            print(f"❌ API Service health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API Service is not accessible: {e}")
        return False

def test_data_format_compatibility():
    """Test that data formats are compatible between services"""
    print("🔍 Testing data format compatibility...")
    
    # Test the exact format expected by AI service
    expected_format = {
        "worker_profile": {"skills": "Java Spring Boot"},
        "job_postings": [{"id": 1, "required_skills": "Java Spring Boot"}]
    }
    
    try:
        response = requests.post(
            f"{AI_SERVICE_URL}/recommendations/jobs",
            json=expected_format,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if "ranked_job_ids" in result and isinstance(result["ranked_job_ids"], list):
                print("✅ Data format compatibility verified")
                return True
            else:
                print("❌ Response format is incorrect")
                print(f"   Expected 'ranked_job_ids' list, got: {result}")
                return False
        else:
            print(f"❌ Data format test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Data format test error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting WorkConnect AI Integration Tests\n")
    
    tests = [
        ("AI Service Health", test_ai_service_health),
        ("AI Recommendations", test_ai_recommendations),
        ("API Service Health", test_api_service_health),
        ("Data Format Compatibility", test_data_format_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! AI integration is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the services and configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
