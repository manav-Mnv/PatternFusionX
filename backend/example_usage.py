"""
Example Usage of Hugging Face AI Models and Database Integration
This script demonstrates how to use the enhanced CodePatternMaster API
"""

import asyncio
import requests
import json
from datetime import datetime

# Base URL for our API
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def test_basic_endpoints():
    """Test basic API endpoints"""
    print_section("1. TESTING BASIC ENDPOINTS")

    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Root endpoint: {response.json()}")

    # Test patterns endpoint
    response = requests.get(f"{BASE_URL}/patterns")
    patterns = response.json()
    print(f"✅ Found {len(patterns)} patterns")

    # Show first pattern
    if patterns:
        print(f"📋 First pattern: {patterns[0]['name']} (ID: {patterns[0]['id']})")

def test_hugging_face_ai():
    """Test Hugging Face AI integration"""
    print_section("2. TESTING HUGGING FACE AI INTEGRATION")

    # Sample code for analysis
    sample_code = """
for i in range(4):
    for j in range(4):
        print('*', end='')
    print()
"""

    # Test enhanced AI analysis
    payload = {
        "pattern_id": 1,  # Square Pattern
        "user_code": sample_code,
        "analysis_type": "implementation"
    }

    response = requests.post(f"{BASE_URL}/ai/enhanced-analysis", json=payload)
    if response.status_code == 200:
        result = response.json()
        print("✅ Enhanced AI Analysis Results:")
        print(f"   - Model Used: {result['model_used']}")
        print(f"   - Database Saved: {result['database_saved']}")
        print(f"   - Complexity Score: {result['ai_analysis']['complexity_analysis']['complexity_score']}")
        print(f"   - AI Confidence: {result['ai_analysis']['complexity_analysis'].get('ai_confidence', 'N/A')}")
        print(f"   - Explanation: {result['ai_analysis']['explanation'][:100]}...")
    else:
        print(f"❌ AI Analysis failed: {response.status_code}")

def test_database_operations():
    """Test database operations"""
    print_section("3. TESTING DATABASE OPERATIONS")

    # Test saving user progress
    progress_data = {
        "progress": 75,
        "time_spent": 1200,  # seconds
        "completed": False,
        "ai_feedback": {"suggestions": ["Use nested loops", "Add comments"]}
    }

    response = requests.post(
        f"{BASE_URL}/user/progress",
        params={"user_id": "demo_user", "pattern_id": 1},
        json=progress_data
    )

    if response.status_code == 200:
        print("✅ User progress saved successfully")
        print(f"   - Response: {response.json()}")
    else:
        print(f"❌ Failed to save progress: {response.status_code}")

    # Test getting user progress
    response = requests.get(f"{BASE_URL}/user/progress/demo_user")
    if response.status_code == 200:
        progress = response.json()
        print("✅ Retrieved user progress:")
        print(f"   - Total attempts: {progress['total_attempts']}")
    else:
        print(f"❌ Failed to get progress: {response.status_code}")

def test_pattern_statistics():
    """Test pattern statistics"""
    print_section("4. TESTING PATTERN STATISTICS")

    response = requests.get(f"{BASE_URL}/patterns/1/statistics")
    if response.status_code == 200:
        stats = response.json()
        print("✅ Pattern statistics:")
        print(f"   - Total attempts: {stats['statistics']['total_attempts']}")
        print(f"   - Success rate: {stats['statistics']['success_rate']}")
        print(f"   - Difficulty assessment: {stats['difficulty_assessment']}")
    else:
        print(f"❌ Failed to get statistics: {response.status_code}")

def test_code_explanation():
    """Test AI code explanation"""
    print_section("5. TESTING AI CODE EXPLANATION")

    sample_code = """
n = 4
for i in range(1, n + 1):
    print('*' * i)
"""

    response = requests.post(
        f"{BASE_URL}/ai/code-explanation",
        json={
            "code": sample_code,
            "pattern_name": "Right Triangle Pattern"
        }
    )

    if response.status_code == 200:
        result = response.json()
        print("✅ AI Code Explanation:")
        print(f"   - Pattern: {result['pattern']}")
        print(f"   - Complexity Level: {result['complexity']['complexity_level']}")
        print(f"   - Explanation: {result['explanation'][:150]}...")
        print(f"   - Suggestions: {', '.join(result['suggestions'][:2])}")
    else:
        print(f"❌ Failed to get explanation: {response.status_code}")

def test_leaderboard():
    """Test leaderboard functionality"""
    print_section("6. TESTING LEADERBOARD")

    response = requests.get(f"{BASE_URL}/leaderboard?limit=5")
    if response.status_code == 200:
        data = response.json()
        print("✅ Leaderboard:")
        for i, user in enumerate(data['leaderboard'], 1):
            print(f"   {i}. {user['user_id']} - {user['patterns_completed']} patterns completed")
    else:
        print(f"❌ Failed to get leaderboard: {response.status_code}")

def demonstrate_hugging_face_vs_fallback():
    """Demonstrate the difference between Hugging Face and fallback analysis"""
    print_section("7. HUGGING FACE VS FALLBACK COMPARISON")

    print("🔬 This example shows how the system gracefully handles:")
    print("   • Hugging Face models when available (GPU/CPU)")
    print("   • Fallback analysis when models aren't loaded")
    print("   • Database integration for both scenarios")
    print("   • Real-time AI confidence scoring")

    # Test with different code samples
    test_cases = [
        {
            "name": "Simple Loop",
            "code": "for i in range(3): print('*' * i)",
            "pattern": "Simple Triangle"
        },
        {
            "name": "Complex Pattern",
            "code": """
n = 5
for i in range(n):
    for j in range(n):
        if i == 0 or i == n-1 or j == 0 or j == n-1:
            print('*', end='')
        else:
            print(' ', end='')
    print()
""",
            "pattern": "Hollow Square"
        }
    ]

    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        response = requests.post(
            f"{BASE_URL}/ai/code-explanation",
            json={
                "code": test_case['code'],
                "pattern_name": test_case['pattern']
            }
        )

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Analysis completed")
            print(f"   🤖 AI Confidence: {result['complexity'].get('ai_confidence', 'N/A')}")
            print(f"   📊 Complexity Score: {result['complexity']['complexity_score']}")

def show_database_schema():
    """Show the database schema structure"""
    print_section("8. DATABASE SCHEMA OVERVIEW")

    print("🗄️  The application uses the following database tables:")
    print()
    print("📋 user_progress:")
    print("   - user_id (string)")
    print("   - pattern_id (integer)")
    print("   - progress_percentage (float)")
    print("   - time_spent (integer)")
    print("   - attempts (integer)")
    print("   - completed (boolean)")
    print("   - last_attempt_at (timestamp)")
    print("   - code_submitted (text)")
    print("   - ai_feedback (json)")
    print()
    print("📋 pattern_attempts:")
    print("   - user_id (string)")
    print("   - pattern_id (integer)")
    print("   - code_submitted (text)")
    print("   - success (boolean)")
    print("   - attempted_at (timestamp)")
    print("   - ai_analysis (json)")
    print()
    print("📋 ai_analyses:")
    print("   - user_id (string)")
    print("   - pattern_id (integer)")
    print("   - analysis_type (string)")
    print("   - complexity_score (float)")
    print("   - suggestions (json array)")
    print("   - explanation (text)")
    print("   - analyzed_at (timestamp)")

def main():
    """Main demonstration function"""
    print("🚀 HUGGING FACE AI & DATABASE INTEGRATION DEMO")
    print("This demonstrates the complete CodePatternMaster system with:")
    print("• Hugging Face AI models for code analysis")
    print("• Supabase database for data persistence")
    print("• Real-time AI feedback and progress tracking")
    print("• Fallback mechanisms for robust operation")

    try:
        # Run all tests
        test_basic_endpoints()
        test_hugging_face_ai()
        test_database_operations()
        test_pattern_statistics()
        test_code_explanation()
        test_leaderboard()
        demonstrate_hugging_face_vs_fallback()
        show_database_schema()

        print_section("🎉 DEMONSTRATION COMPLETE")
        print("✅ All features demonstrated successfully!")
        print("📖 Check the enhanced_main.py file for the complete implementation")
        print("🤖 The system gracefully handles both Hugging Face models and fallbacks")
        print("💾 Database integration provides persistent learning analytics")

    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        print("💡 Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    main()
