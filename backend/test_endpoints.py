#!/usr/bin/env python3
"""
Test script for the Pattern Learning Platform API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return False

def test_patterns_endpoint():
    """Test the patterns endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/patterns")
        print(f"Patterns endpoint: {response.status_code}")
        if response.status_code == 200:
            patterns = response.json()
            print(f"Found {len(patterns)} patterns")
            if patterns:
                print(f"First pattern: {patterns[0]['name']}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing patterns endpoint: {e}")
        return False

def test_generate_detailed_code():
    """Test the generate-detailed-code endpoint"""
    try:
        payload = {
            "pattern_name": "Right Triangle Pattern",
            "language": "python"
        }
        response = requests.post(f"{BASE_URL}/ai/generate-detailed-code", json=payload)
        print(f"Generate detailed code endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Generated code for: {result.get('pattern', 'Unknown')}")
            print(f"Language: {result.get('language', 'Unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing generate-detailed-code endpoint: {e}")
        return False

def test_execute_code():
    """Test the execute-code endpoint"""
    try:
        payload = {
            "code": "print('Hello, World!')",
            "language": "python"
        }
        response = requests.post(f"{BASE_URL}/execute-code", json=payload)
        print(f"Execute code endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Execution status: {result.get('status', 'Unknown')}")
            print(f"Output: {result.get('output', 'No output')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing execute-code endpoint: {e}")
        return False

if __name__ == "__main__":
    print("Testing Pattern Learning Platform API endpoints...")
    print("=" * 50)

    tests = [
        ("Root endpoint", test_root_endpoint),
        ("Patterns endpoint", test_patterns_endpoint),
        ("Generate detailed code", test_generate_detailed_code),
        ("Execute code", test_execute_code)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            print(f"✅ {test_name} passed")
            passed += 1
        else:
            print(f"❌ {test_name} failed")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
