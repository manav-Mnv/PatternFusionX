import requests
import json

def test_new_endpoint():
    url = "http://localhost:8000/ai/generate-detailed-code"
    payload = {
        "pattern_name": "Square Pattern (Solid)",
        "language": "python"
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response:")
            print(f"Pattern: {result.get('pattern')}")
            print(f"Language: {result.get('language')}")
            print(f"Explanation: {result.get('explanation')[:100]}...")
            print(f"Generated Code:\n{result.get('generated_code')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_new_endpoint()
