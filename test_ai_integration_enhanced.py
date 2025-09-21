#!/usr/bin/env python3
"""
Enhanced test script to verify AI service integration with WorkConnect API
This script includes comprehensive testing of edge cases and error scenarios
"""

import requests
import json
import sys
import time
from typing import Dict, List, Any

# Configuration
AI_SERVICE_URL = "http://localhost:8000"
API_SERVICE_URL = "http://localhost:8080"

def test_ai_service_health():
    """Test if AI service is running"""
    try:
        response = requests.get(f"{AI_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ AI Service is running")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   NLTK Data: {data.get('nltk_data', {})}")
            return True
        else:
            print(f"❌ AI Service health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI Service is not accessible: {e}")
        return False

def test_ai_recommendations_basic():
    """Test AI recommendations endpoint with basic data"""
    test_data = {
        "worker_profile": {
            "skills": "Java Spring Boot Python"
        },
        "job_postings": [
            {"id": 1, "required_skills": "Java Spring Boot REST API"},
            {"id": 2, "required_skills": "Python Django Machine Learning"},
            {"id": 3, "required_skills": "JavaScript React Frontend"}
        ]
    }
    
    return _test_ai_recommendations("Basic Recommendations", test_data)

def test_ai_recommendations_edge_cases():
    """Test AI recommendations with edge cases"""
    test_cases = [
        {
            "name": "Empty Skills",
            "data": {
                "worker_profile": {"skills": ""},
                "job_postings": [{"id": 1, "required_skills": "Java"}]
            },
            "expect_empty": True
        },
        {
            "name": "No Job Postings",
            "data": {
                "worker_profile": {"skills": "Java"},
                "job_postings": []
            },
            "expect_empty": True
        },
        {
            "name": "Special Characters in Skills",
            "data": {
                "worker_profile": {"skills": "C++ .NET SQL Server"},
                "job_postings": [
                    {"id": 1, "required_skills": "C++ Visual Studio"},
                    {"id": 2, "required_skills": ".NET Framework SQL"}
                ]
            },
            "expect_empty": False
        },
        {
            "name": "Very Long Skills List",
            "data": {
                "worker_profile": {
                    "skills": " ".join([f"skill{i}" for i in range(100)])
                },
                "job_postings": [
                    {"id": 1, "required_skills": "skill1 skill2 skill3"}
                ]
            },
            "expect_empty": False
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"🔍 Testing {test_case['name']}...")
        result = _test_ai_recommendations(test_case['name'], test_case['data'], test_case.get('expect_empty', False))
        results.append(result)
        print()
    
    return all(results)

def _test_ai_recommendations(test_name: str, test_data: Dict[str, Any], expect_empty: bool = False) -> bool:
    """Helper function to test AI recommendations"""
    try:
        response = requests.post(
            f"{AI_SERVICE_URL}/recommendations/jobs",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            ranked_job_ids = result.get('ranked_job_ids', [])
            
            if expect_empty:
                if not ranked_job_ids:
                    print(f"✅ {test_name}: Correctly returned empty results")
                    return True
                else:
                    print(f"❌ {test_name}: Expected empty results but got {len(ranked_job_ids)} recommendations")
                    return False
            else:
                print(f"✅ {test_name}: Returned {len(ranked_job_ids)} recommendations")
                if ranked_job_ids:
                    print(f"   Top recommendation: Job ID {ranked_job_ids[0]}")
                return True
        else:
            print(f"❌ {test_name} failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {test_name} request failed: {e}")
        return False

def test_data_validation():
    """Test data validation and error handling"""
    invalid_test_cases = [
        {
            "name": "Invalid Job ID Type",
            "data": {
                "worker_profile": {"skills": "Java"},
                "job_postings": [{"id": "invalid", "required_skills": "Java"}]
            }
        },
        {
            "name": "Missing Required Fields",
            "data": {
                "worker_profile": {"skills": "Java"},
                "job_postings": [{"id": 1}]  # Missing required_skills
            }
        },
        {
            "name": "Null Values",
            "data": {
                "worker_profile": {"skills": None},
                "job_postings": [{"id": 1, "required_skills": "Java"}]
            }
        }
    ]
    
    results = []
    for test_case in invalid_test_cases:
        print(f"🔍 Testing {test_case['name']}...")
        try:
            response = requests.post(
                f"{AI_SERVICE_URL}/recommendations/jobs",
                json=test_case['data'],
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code in [200, 422]:  # 422 for validation errors
                print(f"✅ {test_case['name']}: Handled gracefully")
                results.append(True)
            else:
                print(f"❌ {test_case['name']}: Unexpected status {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {test_case['name']}: Exception {e}")
            results.append(False)
        print()
    
    return all(results)

def test_performance():
    """Test performance with large datasets"""
    print("🔍 Testing performance with large dataset...")
    
    # Create large test dataset
    large_test_data = {
        "worker_profile": {
            "skills": "Java Python JavaScript React Angular Node.js Spring Boot Django Flask"
        },
        "job_postings": [
            {"id": i, "required_skills": f"skill{i % 10} technology{i % 5} framework{i % 3}"}
            for i in range(1, 101)  # 100 job postings
        ]
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{AI_SERVICE_URL}/recommendations/jobs",
            json=large_test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            recommendations_count = len(result.get('ranked_job_ids', []))
            print(f"✅ Performance test passed")
            print(f"   Processed 100 jobs in {processing_time:.2f} seconds")
            print(f"   Returned {recommendations_count} recommendations")
            return processing_time < 10  # Should complete within 10 seconds
        else:
            print(f"❌ Performance test failed: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Performance test failed: Request timed out")
        return False
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all enhanced integration tests"""
    print("🚀 Starting Enhanced WorkConnect AI Integration Tests\n")
    
    tests = [
        ("AI Service Health", test_ai_service_health),
        ("Basic AI Recommendations", test_ai_recommendations_basic),
        ("Edge Case Handling", test_ai_recommendations_edge_cases),
        ("Data Validation", test_data_validation),
        ("Performance Test", test_performance)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("=" * 60)
    print("ENHANCED TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All enhanced tests passed! AI integration is robust and working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the AI service implementation and error handling.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
