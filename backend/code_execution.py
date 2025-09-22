#!/usr/bin/env python3
"""
Code execution simulation module for Pattern Learning Platform
Provides safe code execution simulation for multiple languages
"""
import re
from typing import Dict, Any

def generate_detailed_explanation(pattern, language: str) -> str:
    """Generate detailed explanation for pattern implementation"""
    explanations = {
        "python": {
            "Square Pattern (Solid)": """This pattern creates a solid square using nested loops:

1. **Outer Loop**: Controls the rows (i from 0 to n-1)
2. **Inner Loop**: Controls the columns (j from 0 to n-1)
3. **Print Statement**: Prints '*' for each column without newline (end='')
4. **Newline**: After each row is complete, print() adds a newline

Key concepts:
- Nested loops for 2D structure
- Loop variables control position
- Print formatting with end parameter""",

            "Right Triangle Pattern": """This pattern creates a right triangle:

1. **Loop**: Iterates from 1 to n (inclusive)
2. **String Multiplication**: Uses '*' * i to create i stars
3. **Automatic Newline**: Each print() adds a newline

Key concepts:
- Single loop for triangular structure
- String repetition for pattern generation
- Incremental growth pattern""",

            "Diamond Pattern (Solid)": """This pattern creates a diamond shape:

1. **Upper Half**: Loop from 0 to n//2, creating increasing stars
2. **Lower Half**: Loop from n//2-1 to 0, creating decreasing stars
3. **Space Calculation**: (n//2 - i) spaces before stars
4. **Star Calculation**: (2*i + 1) stars per row

Key concepts:
- Two separate loops for upper and lower halves
- Mathematical calculation of spaces and stars
- Symmetric pattern construction""",

            "Hollow Square": """This pattern creates a hollow square:

1. **Outer Loop**: Controls rows
2. **Inner Loop**: Controls columns
3. **Conditions**: Print '*' if:
   - First row (i == 0)
   - Last row (i == n-1)
   - First column (j == 0)
   - Last column (j == n-1)
4. **Otherwise**: Print space

Key concepts:
- Multiple conditions for boundary detection
- Hollow interior with solid border
- Complex conditional logic"""
        }
    }

    # Get explanation for specific pattern and language
    lang_explanations = explanations.get(language, explanations.get("python", {}))
    explanation = lang_explanations.get(pattern.name, f"""This is a {pattern.difficulty} level pattern that requires:

1. **Loops**: {pattern.loops} nested loops
2. **Conditions**: {pattern.conditions} conditional statements
3. **Formula**: {pattern.formula}

The pattern creates a visual representation using:
- Outer loop for rows
- Inner loop for columns
- Conditional logic for special cases
- Print statements for output""")

    return explanation

def simulate_python_execution(code: str) -> str:
    """Simulate Python code execution"""
    output = ""

    try:
        # Basic Python code patterns
        if "print" in code:
            # Extract string literals from print statements
            print_matches = re.findall(r'print\(["\'](.*?)["\']', code)
            for match in print_matches:
                output += match + "\n"

            # Handle print with variables (basic simulation)
            if "print('*'" in code or "print('*'," in code:
                # Count asterisks in loops
                if "for" in code:
                    lines = code.split('\n')
                    for line in lines:
                        if "print('*'" in line or "print('*'," in line:
                            # Simple pattern detection
                            if "range" in code:
                                n_match = re.search(r'n\s*=\s*(\d+)', code)
                                if n_match:
                                    n = int(n_match.group(1))
                                    for i in range(n):
                                        output += "*" * n + "\n"
                                else:
                                    output += "Simulated pattern output\n"
                            break

        elif "for" in code and "*" in code:
            # Pattern generation simulation
            output += "Simulated pattern execution\n"

        else:
            output += "Code executed successfully\n"

    except Exception as e:
        output += f"Execution error: {str(e)}\n"

    return output

def simulate_javascript_execution(code: str) -> str:
    """Simulate JavaScript code execution"""
    output = ""

    try:
        if "console.log" in code:
            log_matches = re.findall(r'console\.log\(["\'](.*?)["\']', code)
            for match in log_matches:
                output += match + "\n"

            if "console.log('*'" in code:
                if "for" in code:
                    output += "Simulated JavaScript pattern output\n"
                else:
                    output += "*\n"

        else:
            output += "JavaScript code executed\n"

    except Exception as e:
        output += f"Execution error: {str(e)}\n"

    return output

def simulate_java_execution(code: str) -> str:
    """Simulate Java code execution"""
    output = ""

    try:
        if "System.out.println" in code or "System.out.print" in code:
            print_matches = re.findall(r'System\.out\.print(?:ln)?\(["\'](.*?)["\']', code)
            for match in print_matches:
                output += match + "\n"

            if "System.out.print" in code and "*" in code:
                output += "Simulated Java pattern output\n"

        else:
            output += "Java code executed\n"

    except Exception as e:
        output += f"Execution error: {str(e)}\n"

    return output

def simulate_code_execution(code: str, language: str) -> Dict[str, Any]:
    """Main function to simulate code execution"""
    if language == "python":
        output = simulate_python_execution(code)
    elif language == "javascript":
        output = simulate_javascript_execution(code)
    elif language == "java":
        output = simulate_java_execution(code)
    else:
        output = f"Language '{language}' not supported for execution"

    return {
        "output": output,
        "language": language,
        "execution_time": "0.1s",
        "status": "success"
    }
