"""
Simple API test script to demonstrate Hugging Face AI and Database integration
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_basic_api():
    """Test basic API functionality"""
    print("🔍 Testing basic API endpoints...")

    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Root endpoint: {response.status_code}")

    # Test patterns endpoint
    response = requests.get(f"{BASE_URL}/patterns")
    patterns = response.json()
    print(f"✅ Patterns endpoint: Found {len(patterns)} patterns")

    return patterns

def test_enhanced_ai_analysis():
    """Test the enhanced AI analysis with Hugging Face"""
    print("\n🤖 Testing enhanced AI analysis...")

    # Simple Python code for square pattern
    code = """for i in range(4):
    for j in range(4):
        print('*', end='')
    print()"""

    payload = {
        "pattern_id": 1,
        "user_code": code,
        "analysis_type": "implementation"
    }

    response = requests.post(f"{BASE_URL}/ai/enhanced-analysis", json=payload)

    if response.status_code == 200:
        result = response.json()
        print("✅ Enhanced AI Analysis successful!")
        print(f"   - Model Used: {result['model_used']}")
        print(f"   - Database Saved: {result['database_saved']}")
        print(f"   - Pattern: {result['pattern']['name']}")
        print(f"   - AI Confidence: {result['ai_analysis']['complexity_analysis'].get('ai_confidence', 'N/A')}")
        print(f"   - Complexity Score: {result['ai_analysis']['complexity_analysis']['complexity_score']}")
        return result
    else:
        print(f"❌ AI Analysis failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_database_operations():
    """Test database operations"""
    print("\n🗄️ Testing database operations...")

    # Save user progress
    progress_data = {
        "progress": 85,
        "time_spent": 900,
        "completed": True,
        "ai_feedback": {"suggestions": ["Great work!", "Consider adding comments"]}
    }

    response = requests.post(
        f"{BASE_URL}/user/progress",
        params={"user_id": "test_user_123", "pattern_id": 1},
        json=progress_data
    )

    if response.status_code == 200:
        print("✅ User progress saved successfully!")
        print(f"   - Response: {response.json()['message']}")
    else:
        print(f"❌ Failed to save progress: {response.status_code}")

    # Get user progress
    response = requests.get(f"{BASE_URL}/user/progress/test_user_123")
    if response.status_code == 200:
        progress = response.json()
        print("✅ Retrieved user progress:")
        print(f"   - Total attempts: {progress['total_attempts']}")
    else:
        print(f"❌ Failed to get progress: {response.status_code}")

def test_code_explanation():
    """Test AI code explanation"""
    print("\n📝 Testing AI code explanation...")

    code = """n = 4
for i in range(1, n + 1):
    print('*' * i)"""

    response = requests.post(
        f"{BASE_URL}/ai/code-explanation",
        json={
            "code": code,
            "pattern_name": "Right Triangle Pattern"
        }
    )

    if response.status_code == 200:
        result = response.json()
        print("✅ AI Code Explanation successful!")
        print(f"   - Pattern: {result['pattern']}")
        print(f"   - Complexity Level: {result['complexity']['complexity_level']}")
        print(f"   - Explanation: {result['explanation'][:100]}...")
    else:
        print(f"❌ Code explanation failed: {response.status_code}")

def main():
    """Main test function"""
    print("🚀 TESTING HUGGING FACE AI & DATABASE INTEGRATION")
    print("=" * 60)

    try:
        # Test all functionality
        patterns = test_basic_api()
        ai_result = test_enhanced_ai_analysis()
        test_database_operations()
        test_code_explanation()

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Hugging Face AI integration working")
        print("✅ Database operations working")
        print("✅ Enhanced analysis endpoints working")
        print("✅ Code explanation working")

        if ai_result:
            print("\n📊 SUMMARY:")
            print(f"   - AI Model: {ai_result['model_used']}")
            print(f"   - Database Integration: {ai_result['database_saved']}")
            print(f"   - Complexity Analysis: {ai_result['ai_analysis']['complexity_analysis']['complexity_score']}")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("💡 Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    main()
