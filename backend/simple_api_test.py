#!/usr/bin/env python3
import requests
import json

def test_api():
    print("🧪 Testing Pattern Learning Platform API")
    print("=" * 40)

    # Test 1: Basic connectivity
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Basic API: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Basic API failed: {e}")
        return

    # Test 2: AI Code Generation
    try:
        payload = {
            "pattern_name": "Square Pattern (Solid)",
            "language": "python"
        }
        response = requests.post(
            "http://localhost:8000/ai/generate-detailed-code",
            json=payload,
            timeout=10
        )
        print(f"✅ AI Code Generation: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Pattern: {result.get('pattern')}")
            print(f"   Language: {result.get('language')}")
            print(f"   Has explanation: {bool(result.get('explanation'))}")
            print(f"   Code length: {len(result.get('generated_code', ''))}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ AI endpoint failed: {e}")

    # Test 3: Code Execution
    try:
        payload = {
            "code": "print('Hello World')",
            "language": "python",
            "input": ""
        }
        response = requests.post(
            "http://localhost:8000/execute-code",
            json=payload,
            timeout=10
        )
        print(f"✅ Code Execution: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Output: {result.get('output', '').strip()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Code execution failed: {e}")

    # Test 4: Error handling
    try:
        response = requests.get("http://localhost:8000/invalid-endpoint", timeout=5)
        print(f"✅ Error Handling: {response.status_code}")
        print(f"   Proper error response: {response.status_code in [404, 405]}")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

if __name__ == "__main__":
    test_api()
