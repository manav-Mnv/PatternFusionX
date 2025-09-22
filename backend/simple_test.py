#!/usr/bin/env python3
"""
Simple test to verify backend functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if we can import the main modules"""
    try:
        from main import get_sample_patterns, analyze_visual_pattern
        print("✅ Successfully imported main module functions")

        # Test getting patterns
        patterns = get_sample_patterns()
        print(f"✅ Successfully loaded {len(patterns)} patterns")

        # Test pattern analysis
        if patterns:
            pattern = patterns[0]
            analysis = analyze_visual_pattern(pattern)
            print(f"✅ Pattern analysis working: {analysis['rows']} rows, {analysis['columns']} columns")

        return True
    except Exception as e:
        print(f"❌ Error importing or testing main module: {e}")
        return False

def test_code_execution_module():
    """Test the code execution module"""
    try:
        from code_execution import generate_detailed_explanation, simulate_code_execution

        # Test explanation generation
        patterns = [
            type('Pattern', (), {
                'name': 'Test Pattern',
                'difficulty': 'easy',
                'loops': 2,
                'conditions': 1,
                'formula': 'test formula'
            })()
        ]

        explanation = generate_detailed_explanation(patterns[0], 'python')
        print(f"✅ Explanation generation working: {len(explanation)} characters")

        # Test code execution simulation
        result = simulate_code_execution("print('Hello')", "python")
        print(f"✅ Code execution simulation working: {result['status']}")

        return True
    except Exception as e:
        print(f"❌ Error testing code execution module: {e}")
        return False

if __name__ == "__main__":
    print("Testing Pattern Learning Platform Backend...")
    print("=" * 50)

    tests = [
        ("Main module imports", test_imports),
        ("Code execution module", test_code_execution_module)
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
        print("🎉 All tests passed! Backend modules are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
