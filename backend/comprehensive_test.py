#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Pattern Learning Platform
Tests all API endpoints, functionality, and edge cases
"""
import requests
import json
import time
from typing import Dict, List, Any

class PatternLearningPlatformTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []

    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {details}")

    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log_test("Basic Connectivity", "PASS", f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Basic Connectivity", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Basic Connectivity", "FAIL", str(e))
            return False

    def test_ai_code_generation(self):
        """Test AI code generation endpoint"""
        test_cases = [
            {"pattern_name": "Square Pattern (Solid)", "language": "python"},
            {"pattern_name": "Right Triangle Pattern", "language": "javascript"},
            {"pattern_name": "Diamond Pattern (Solid)", "language": "java"},
            {"pattern_name": "Hollow Square", "language": "cpp"},
            {"pattern_name": "Invalid Pattern", "language": "python"},  # Error case
            {"pattern_name": "Square Pattern (Solid)", "language": "invalid"}  # Invalid language
        ]

        all_passed = True
        for i, test_case in enumerate(test_cases, 1):
            try:
                response = requests.post(
                    f"{self.base_url}/ai/generate-detailed-code",
                    json=test_case,
                    timeout=10
                )

                if test_case["pattern_name"] == "Invalid Pattern":
                    # Should handle invalid pattern gracefully
                    if response.status_code != 200:
                        self.log_test(f"AI Code Gen Test {i}", "PASS",
                                    f"Proper error handling for invalid pattern: {response.status_code}")
                    else:
                        self.log_test(f"AI Code Gen Test {i}", "FAIL",
                                    "Should have returned error for invalid pattern")
                        all_passed = False
                elif test_case["language"] == "invalid":
                    # Should handle invalid language gracefully
                    if response.status_code == 200:
                        result = response.json()
                        self.log_test(f"AI Code Gen Test {i}", "PASS",
                                    f"Handled invalid language: {result.get('language', 'unknown')}")
                    else:
                        self.log_test(f"AI Code Gen Test {i}", "FAIL",
                                    f"Failed to handle invalid language: {response.status_code}")
                        all_passed = False
                else:
                    # Valid test case
                    if response.status_code == 200:
                        result = response.json()
                        required_fields = ['pattern', 'language', 'generated_code']
                        missing_fields = [field for field in required_fields if not result.get(field)]

                        if missing_fields:
                            self.log_test(f"AI Code Gen Test {i}", "FAIL",
                                        f"Missing fields: {missing_fields}")
                            all_passed = False
                        else:
                            self.log_test(f"AI Code Gen Test {i}", "PASS",
                                        f"Generated {len(result.get('generated_code', ''))} chars of code")
                    else:
                        self.log_test(f"AI Code Gen Test {i}", "FAIL",
                                    f"Status: {response.status_code}")
                        all_passed = False

            except Exception as e:
                self.log_test(f"AI Code Gen Test {i}", "FAIL", str(e))
                all_passed = False

        return all_passed

    def test_code_execution(self):
        """Test code execution endpoint"""
        test_cases = [
            {
                "code": "print('Hello World')",
                "language": "python",
                "expected": "Hello World"
            },
            {
                "code": "console.log('Hello World');",
                "language": "javascript",
                "expected": "Hello World"
            },
            {
                "code": "System.out.println(\"Hello World\");",
                "language": "java",
                "expected": "Hello World"
            }
        ]

        all_passed = True
        for i, test_case in enumerate(test_cases, 1):
            try:
                response = requests.post(
                    f"{self.base_url}/execute-code",
                    json={
                        "code": test_case["code"],
                        "language": test_case["language"],
                        "input": ""
                    },
                    timeout=15
                )

                if response.status_code == 200:
                    result = response.json()
                    output = result.get('output', '').strip()
                    if test_case["expected"] in output:
                        self.log_test(f"Code Execution Test {i}", "PASS",
                                    f"Got expected output: {output[:50]}...")
                    else:
                        self.log_test(f"Code Execution Test {i}", "FAIL",
                                    f"Expected '{test_case['expected']}', got: {output}")
                        all_passed = False
                else:
                    self.log_test(f"Code Execution Test {i}", "FAIL",
                                f"Status: {response.status_code}")
                    all_passed = False

            except Exception as e:
                self.log_test(f"Code Execution Test {i}", "FAIL", str(e))
                all_passed = False

        return all_passed

    def test_performance(self):
        """Test API performance"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to ms

            if response_time < 1000:  # Less than 1 second
                self.log_test("Performance Test", "PASS",
                            f"Response time: {response_time:.0f}ms")
                return True
            else:
                self.log_test("Performance Test", "FAIL",
                            f"Slow response time: {response_time:.0f}ms")
                return False
        except Exception as e:
            self.log_test("Performance Test", "FAIL", str(e))
            return False

    def test_error_handling(self):
        """Test error handling for various scenarios"""
        test_cases = [
            ("GET", "/invalid-endpoint"),
            ("POST", "/ai/generate-detailed-code", {"invalid": "data"}),
            ("POST", "/execute-code", {"invalid": "data"}),
        ]

        all_passed = True
        for method, endpoint, data in test_cases:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}",
                                           json=data, timeout=5)

                # Should return proper error codes, not crash
                if response.status_code in [400, 404, 405, 500]:
                    self.log_test(f"Error Handling: {method} {endpoint}", "PASS",
                                f"Proper error code: {response.status_code}")
                else:
                    self.log_test(f"Error Handling: {method} {endpoint}", "FAIL",
                                f"Unexpected status: {response.status_code}")
                    all_passed = False

            except Exception as e:
                self.log_test(f"Error Handling: {method} {endpoint}", "FAIL", str(e))
                all_passed = False

        return all_passed

    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🧪 Starting Comprehensive Testing Suite")
        print("=" * 50)

        tests = [
            ("Basic Connectivity", self.test_basic_connectivity),
            ("AI Code Generation", self.test_ai_code_generation),
            ("Code Execution", self.test_code_execution),
            ("Performance", self.test_performance),
            ("Error Handling", self.test_error_handling),
        ]

        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name}...")
            if test_func():
                passed += 1

        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100".1f"}%")

        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check details above.")

        return passed == total

def main():
    tester = PatternLearningPlatformTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
