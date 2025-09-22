import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:8000"

    print("🧪 Testing Pattern Learning Platform API")
    print("=" * 50)

    # Test 1: Basic API endpoint
    try:
        response = requests.get(f"{base_url}/")
        print("✅ Test 1 - Basic API endpoint:")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        print()

    # Test 2: New AI generate-detailed-code endpoint
    print("✅ Test 2 - AI generate-detailed-code endpoint:")
    test_cases = [
        {"pattern_name": "Square Pattern (Solid)", "language": "python"},
        {"pattern_name": "Right Triangle Pattern", "language": "javascript"},
        {"pattern_name": "Diamond Pattern (Solid)", "language": "java"},
        {"pattern_name": "Square Pattern (Solid)", "language": "cpp"}
    ]

    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/ai/generate-detailed-code",
                json=test_case,
                timeout=10
            )
            print(f"   Test 2.{i} - {test_case['pattern_name']} ({test_case['language']}):")
            print(f"     Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"     Pattern: {result.get('pattern')}")
                print(f"     Language: {result.get('language')}")
                print(f"     Has explanation: {'Yes' if result.get('explanation') else 'No'}")
                print(f"     Has generated code: {'Yes' if result.get('generated_code') else 'No'}")
                print(f"     Code length: {len(result.get('generated_code', ''))}")
            else:
                print(f"     Error: {response.text}")
            print()
        except Exception as e:
            print(f"   Test 2.{i} failed: {e}")
            print()

    # Test 3: Test with invalid pattern name
    print("✅ Test 3 - Error handling:")
    try:
        response = requests.post(
            f"{base_url}/ai/generate-detailed-code",
            json={"pattern_name": "Invalid Pattern", "language": "python"},
            timeout=10
        )
        print(f"   Invalid pattern test - Status: {response.status_code}")
        if response.status_code != 200:
            print("   ✅ Proper error handling for invalid pattern")
        else:
            print("   ⚠️  Should have returned error for invalid pattern")
        print()
    except Exception as e:
        print(f"   Error handling test failed: {e}")
        print()

    # Test 4: Test with invalid language
    print("✅ Test 4 - Invalid language handling:")
    try:
        response = requests.post(
            f"{base_url}/ai/generate-detailed-code",
            json={"pattern_name": "Square Pattern (Solid)", "language": "invalid"},
            timeout=10
        )
        print(f"   Invalid language test - Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Fallback language: {result.get('language')}")
            print("   ✅ Proper fallback for invalid language")
        else:
            print("   ⚠️  Should have handled invalid language gracefully")
        print()
    except Exception as e:
        print(f"   Invalid language test failed: {e}")
        print()

if __name__ == "__main__":
    test_api_endpoints()
