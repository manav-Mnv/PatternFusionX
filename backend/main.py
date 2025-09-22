from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from supabase import create_client, Client
import logging

# Import our custom modules
from ai_models import get_ai_code_analysis, ai_analyzer
from database import db_manager, save_user_learning_path

# Initialize FastAPI app
app = FastAPI(title="CodePatternMaster API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration
SUPABASE_URL = "https://cmmxtopgavawhtbgkczw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNtbXh0b3BnYXZhd2h0YmdrY3p3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjE3NjAsImV4cCI6MjA3MzkzNzc2MH0.kufU6wv8CFLLk-3OZM-4Ex1Omezm0ohaRbdduvaWhSY"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic models
class Pattern(BaseModel):
    id: int
    name: str
    category: str
    difficulty: str
    description: str
    preview: List[str]
    rows: int
    popularity: int
    completion_rate: int
    formula: str
    loops: int
    conditions: int

class AIAnalysisRequest(BaseModel):
    pattern_id: int
    user_code: Optional[str] = None
    analysis_type: str = "visual"

class AIAnalysisResponse(BaseModel):
    analysis_type: str
    results: Dict[str, Any]
    suggestions: List[str]
    complexity_score: float

class CodeFeedbackRequest(BaseModel):
    pattern_id: int
    user_code: str
    language: str

class CodeFeedbackResponse(BaseModel):
    feedback: str
    suggestions: List[str]
    correctness_score: float
    hints: List[str]

# API Routes
@app.get("/")
async def read_root():
    return {
        "message": "CodePatternMaster API", 
        "version": "1.0.0",
        "status": "running",
        "features": [
            "AI Pattern Analysis",
            "Code Generation",
            "Educational Chat",
            "Pattern Recognition",
            "User Progress Tracking"
        ]
    }

@app.get("/patterns", response_model=List[Pattern])
async def get_patterns(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 50
):
    """Get patterns with optional filtering"""
    return get_sample_patterns()

@app.get("/patterns/{pattern_id}", response_model=Pattern)
async def get_pattern(pattern_id: int):
    """Get a specific pattern by ID"""
    patterns = get_sample_patterns()
    for pattern in patterns:
        if pattern.id == pattern_id:
            return pattern
    raise HTTPException(status_code=404, detail="Pattern not found")

@app.post("/ai/analyze", response_model=AIAnalysisResponse)
async def analyze_pattern(request: AIAnalysisRequest):
    """AI-powered pattern analysis"""
    patterns = get_sample_patterns()
    pattern = next((p for p in patterns if p.id == request.pattern_id), None)
    
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    
    # Run AI analysis based on type
    if request.analysis_type == "visual":
        analysis_results = analyze_visual_pattern(pattern)
    elif request.analysis_type == "mathematical":
        analysis_results = analyze_mathematical_pattern(pattern)
    elif request.analysis_type == "logical":
        analysis_results = analyze_logical_pattern(pattern)
    elif request.analysis_type == "implementation":
        analysis_results = analyze_implementation_pattern(pattern, request.user_code)
    else:
        raise HTTPException(status_code=400, detail="Invalid analysis type")
    
    return AIAnalysisResponse(
        analysis_type=request.analysis_type,
        results=analysis_results,
        suggestions=generate_suggestions(pattern, request.analysis_type),
        complexity_score=calculate_complexity_score(pattern)
    )

@app.post("/ai/code-feedback", response_model=CodeFeedbackResponse)
async def get_code_feedback(request: CodeFeedbackRequest):
    """Get AI feedback on user's code"""
    patterns = get_sample_patterns()
    pattern = next((p for p in patterns if p.id == request.pattern_id), None)
    
    feedback = generate_code_feedback(request.user_code, pattern)
    suggestions = generate_code_suggestions(request.user_code, pattern)
    hints = generate_progressive_hints(pattern, request.user_code)
    
    return CodeFeedbackResponse(
        feedback=feedback,
        suggestions=suggestions,
        correctness_score=calculate_correctness_score(request.user_code, pattern),
        hints=hints
    )

@app.post("/ai/generate-code")
async def generate_code(pattern_id: int, language: str = "python"):
    """Generate code for a pattern using AI"""
    patterns = get_sample_patterns()
    pattern = next((p for p in patterns if p.id == pattern_id), None)

    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    generated_code = generate_code_template(pattern, language)

    return {
        "generated_code": generated_code,
        "pattern": pattern,
        "language": language
    }

@app.post("/ai/generate-detailed-code")
async def generate_detailed_code(request: Dict[str, Any]):
    """Generate detailed code with explanations"""
    pattern_name = request.get("pattern_name", "")
    language = request.get("language", "python")

    # Find pattern by name
    patterns = get_sample_patterns()
    pattern = next((p for p in patterns if p.name.lower() == pattern_name.lower()), None)

    if not pattern:
        # Try to find by partial match
        pattern = next((p for p in patterns if pattern_name.lower() in p.name.lower()), None)

    if not pattern:
        raise HTTPException(status_code=404, detail=f"Pattern '{pattern_name}' not found")

    generated_code = generate_code_template(pattern, language)

    # Generate detailed explanation
    explanation = generate_detailed_explanation(pattern, language)

    return {
        "pattern": pattern.name,
        "language": language,
        "generated_code": generated_code,
        "explanation": explanation,
        "difficulty": pattern.difficulty,
        "complexity": calculate_complexity_score(pattern)
    }

@app.post("/execute-code")
async def execute_code(request: Dict[str, Any]):
    """Execute user code and return results"""
    code = request.get("code", "")
    language = request.get("language", "python")
    input_data = request.get("input", "")

    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    # Simple code execution simulation (in production, use secure sandbox)
    try:
        if language == "python":
            # Simulate Python execution
            output = simulate_python_execution(code)
        elif language == "javascript":
            # Simulate JavaScript execution
            output = simulate_javascript_execution(code)
        elif language == "java":
            # Simulate Java execution
            output = simulate_java_execution(code)
        else:
            output = f"Language '{language}' not supported for execution"

        return {
            "output": output,
            "language": language,
            "execution_time": "0.1s",
            "status": "success"
        }
    except Exception as e:
        return {
            "output": f"Error: {str(e)}",
            "language": language,
            "execution_time": "0.0s",
            "status": "error"
        }

@app.post("/ai/chat")
async def educational_chat(message: str, context: Optional[str] = None):
    """Educational chat with AI tutor"""
    responses = {
        "hello": "Hello! I'm your AI coding tutor. How can I help you learn programming patterns today?",
        "help": "I can help you understand programming patterns, analyze code, and provide step-by-step guidance. What would you like to learn?",
        "pattern": "Programming patterns are visual representations of code logic. They help you understand loops, conditions, and algorithms. Which pattern interests you?",
        "loop": "Loops are fundamental in programming patterns. They help you repeat actions and create structured output. Would you like to see some examples?",
        "difficult": "Don't worry! Every programmer starts somewhere. Let's break down the problem into smaller, manageable steps. What specific part is challenging?",
    }
    
    message_lower = message.lower()
    for key, response in responses.items():
        if key in message_lower:
            return {"response": response, "context": context}
    
    return {
        "response": "That's a great question! Let me help you understand that concept. Can you tell me more about what specific part you'd like to explore?",
        "context": context
    }

# Helper functions
def get_sample_patterns():
    """Return sample patterns"""
    return [
        Pattern(
            id=1,
            name="Square Pattern (Solid)",
            category="basic-star",
            difficulty="easy",
            description="A solid square filled with stars",
            preview=["****", "****", "****", "****"],
            rows=4,
            popularity=95,
            completion_rate=92,
            formula="stars = n, spaces = 0",
            loops=2,
            conditions=0
        ),
        Pattern(
            id=2,
            name="Right Triangle Pattern",
            category="basic-star",
            difficulty="easy",
            description="Stars forming a right triangle",
            preview=["*", "**", "***", "****"],
            rows=4,
            popularity=98,
            completion_rate=95,
            formula="stars = i, spaces = 0",
            loops=2,
            conditions=0
        ),
        Pattern(
            id=3,
            name="Left Triangle Pattern",
            category="basic-star",
            difficulty="easy",
            description="Stars aligned to the left forming triangle",
            preview=["   *", "  **", " ***", "****"],
            rows=4,
            popularity=87,
            completion_rate=89,
            formula="stars = i, spaces = n-i",
            loops=2,
            conditions=0
        ),
        Pattern(
            id=4,
            name="Inverted Right Triangle",
            category="basic-star",
            difficulty="easy",
            description="Upside-down right triangle",
            preview=["****", "***", "**", "*"],
            rows=4,
            popularity=85,
            completion_rate=88,
            formula="stars = n-i+1, spaces = 0",
            loops=2,
            conditions=0
        ),
        Pattern(
            id=5,
            name="Isosceles Triangle",
            category="basic-star",
            difficulty="easy",
            description="Centered triangle with equal sides",
            preview=["  *  ", " *** ", "*****"],
            rows=3,
            popularity=91,
            completion_rate=90,
            formula="stars = 2*i+1, spaces = n-i-1",
            loops=2,
            conditions=0
        ),
        Pattern(
            id=11,
            name="Hollow Square",
            category="hollow",
            difficulty="medium",
            description="Square with hollow interior",
            preview=["****", "*  *", "*  *", "****"],
            rows=4,
            popularity=84,
            completion_rate=76,
            formula="stars = n (if first/last row/col), spaces = n-2 (middle)",
            loops=2,
            conditions=4
        ),
        Pattern(
            id=31,
            name="Diamond Pattern (Solid)",
            category="diamond",
            difficulty="medium",
            description="Solid diamond shape",
            preview=["  *  ", " *** ", "*****", " *** ", "  *  "],
            rows=5,
            popularity=89,
            completion_rate=82,
            formula="stars = 2*i+1 (upper), 2*(n-i-1)+1 (lower), spaces = n-i-1",
            loops=2,
            conditions=1
        ),
        Pattern(
            id=32,
            name="Hollow Diamond",
            category="diamond",
            difficulty="medium",
            description="Diamond with hollow center",
            preview=["  *  ", " * * ", "*   *", " * * ", "  *  "],
            rows=5,
            popularity=85,
            completion_rate=76,
            formula="stars = 1 (if first/last), spaces = n-i-1 + i-1 (middle)",
            loops=2,
            conditions=4
        ),
        Pattern(
            id=41,
            name="Number Triangle (1,2,3...)",
            category="number",
            difficulty="easy",
            description="Triangle with sequential numbers",
            preview=["1", "12", "123", "1234"],
            rows=4,
            popularity=92,
            completion_rate=88,
            formula="numbers = 1 to i",
            loops=2,
            conditions=0
        ),
        Pattern(
            id=66,
            name="Butterfly Pattern",
            category="special",
            difficulty="hard",
            description="Butterfly wing pattern",
            preview=["*    *", "**  **", "******", "**  **", "*    *"],
            rows=5,
            popularity=91,
            completion_rate=67,
            formula="stars = i+1 (left), 2*(n-i-1) (right), spaces = 2*(n-i-1)",
            loops=2,
            conditions=2
        ),
        Pattern(
            id=69,
            name="X Pattern (Cross)",
            category="special",
            difficulty="medium",
            description="X or cross pattern",
            preview=["*   *", " * * ", "  *  ", " * * ", "*   *"],
            rows=5,
            popularity=86,
            completion_rate=78,
            formula="stars = 1 (if i==j or i+j==n-1)",
            loops=2,
            conditions=2
        )
    ]

def analyze_visual_pattern(pattern):
    """Analyze visual aspects of pattern"""
    return {
        "rows": pattern.rows,
        "columns": max(len(line) for line in pattern.preview),
        "total_elements": sum(len(line) for line in pattern.preview),
        "unique_elements": len(set("".join(pattern.preview))),
        "symmetry": "symmetric" if "diamond" in pattern.name.lower() or "x" in pattern.name.lower() else "asymmetric",
        "density": sum(len(line.replace(" ", "")) for line in pattern.preview) / sum(len(line) for line in pattern.preview)
    }

def analyze_mathematical_pattern(pattern):
    """Analyze mathematical aspects of pattern"""
    return {
        "formula": pattern.formula,
        "complexity": "O(n²)" if pattern.difficulty == "medium" else "O(n)" if pattern.difficulty == "easy" else "O(n³)",
        "loops": pattern.loops,
        "conditions": pattern.conditions,
        "growth_pattern": "increasing" if len(pattern.preview[0]) < len(pattern.preview[-1]) else "decreasing"
    }

def analyze_logical_pattern(pattern):
    """Analyze logical structure of pattern"""
    return {
        "nested_loops": pattern.loops,
        "conditions": pattern.conditions,
        "variables": ["i", "j", "spaces", "stars"],
        "approach": "direct iteration" if pattern.difficulty == "easy" else "conditional logic" if pattern.difficulty == "medium" else "complex algorithms"
    }

def analyze_implementation_pattern(pattern, user_code):
    """Analyze implementation aspects"""
    return {
        "code_structure": "good" if user_code and "for" in user_code else "needs_improvement",
        "variable_usage": "appropriate" if user_code and "i" in user_code else "missing",
        "loop_structure": "correct" if user_code and "range" in user_code else "incorrect"
    }

def generate_suggestions(pattern, analysis_type):
    """Generate suggestions based on analysis"""
    suggestions = []
    
    if analysis_type == "visual":
        suggestions.extend([
            "Try to identify the symmetry in this pattern",
            "Count the elements in each row to find the pattern",
            "Notice how the pattern changes from row to row"
        ])
    elif analysis_type == "mathematical":
        suggestions.extend([
            f"Use the formula: {pattern.formula}",
            f"This pattern requires {pattern.loops} nested loops",
            "Calculate spaces and stars for each row"
        ])
    elif analysis_type == "logical":
        suggestions.extend([
            "Start with the outer loop for rows",
            "Use inner loop for columns",
            "Apply conditions for special cases"
        ])
    
    return suggestions

def calculate_complexity_score(pattern):
    """Calculate complexity score (0-1)"""
    base_score = 0.3 if pattern.difficulty == "easy" else 0.6 if pattern.difficulty == "medium" else 0.9
    loop_penalty = pattern.loops * 0.1
    condition_penalty = pattern.conditions * 0.05
    return min(1.0, base_score + loop_penalty + condition_penalty)

def generate_code_feedback(user_code, pattern):
    """Generate feedback on user's code"""
    if not user_code:
        return "Please write some code to get feedback!"
    
    feedback_parts = []
    
    if "for" in user_code:
        feedback_parts.append("✅ Good! You're using loops.")
    else:
        feedback_parts.append("💡 Try using loops to iterate through rows.")
    
    if "print" in user_code or "console.log" in user_code or "System.out.print" in user_code:
        feedback_parts.append("✅ Great! You're printing output.")
    else:
        feedback_parts.append("💡 Don't forget to print the pattern!")
    
    if pattern and pattern.loops > 1 and user_code.count("for") >= 2:
        feedback_parts.append("✅ Excellent! You're using nested loops correctly.")
    elif pattern and pattern.loops > 1:
        feedback_parts.append("💡 This pattern needs nested loops.")
    
    return " ".join(feedback_parts)

def generate_code_suggestions(user_code, pattern):
    """Generate code suggestions"""
    suggestions = []
    
    if not user_code:
        suggestions.append("Start by creating a variable for the pattern size")
        suggestions.append("Use a for loop to iterate through rows")
        return suggestions
    
    if "range" not in user_code and "for" in user_code:
        suggestions.append("Use range() function for loop iteration")
    
    if pattern and pattern.conditions > 0 and "if" not in user_code:
        suggestions.append("Add conditional statements for special cases")
    
    if "print" not in user_code:
        suggestions.append("Add print statements to display the pattern")
    
    return suggestions

def generate_progressive_hints(pattern, user_code):
    """Generate progressive hints"""
    hints = []
    
    if not user_code:
        hints.extend([
            f"Start with a variable n = {pattern.rows}",
            "Create a loop from 0 to n-1",
            "Calculate spaces and stars for each row",
            "Print spaces, then stars, then newline"
        ])
    elif "for" not in user_code:
        hints.extend([
            "Add a for loop to iterate through rows",
            "Use range() function for the loop"
        ])
    elif user_code.count("for") < pattern.loops:
        hints.extend([
            "You need nested loops for this pattern",
            "Add an inner loop for columns"
        ])
    else:
        hints.extend([
            "Great progress! Now add the print statements",
            "Make sure to print newline after each row"
        ])
    
    return hints

def calculate_correctness_score(user_code, pattern):
    """Calculate correctness score (0-1)"""
    if not user_code:
        return 0.0
    
    score = 0.0
    
    # Check for loops
    if "for" in user_code:
        score += 0.3
    
    # Check for nested loops if needed
    if pattern and pattern.loops > 1 and user_code.count("for") >= 2:
        score += 0.3
    
    # Check for print statements
    if "print" in user_code or "console.log" in user_code or "System.out.print" in user_code:
        score += 0.2
    
    # Check for conditions if needed
    if pattern and pattern.conditions > 0 and "if" in user_code:
        score += 0.2
    
    return min(1.0, score)

def generate_code_template(pattern, language):
    """Generate code template for pattern"""
    if language == "python":
        if pattern.id == 1:  # Square Pattern
            return """# Square Pattern (Solid)
n = 4
for i in range(n):
    for j in range(n):
        print('*', end='')
    print()"""
        elif pattern.id == 2:  # Right Triangle
            return """# Right Triangle Pattern
n = 4
for i in range(1, n + 1):
    print('*' * i)"""
        elif pattern.id == 31:  # Diamond
            return """# Diamond Pattern
n = 5
# Upper half
for i in range(n//2 + 1):
    spaces = ' ' * (n//2 - i)
    stars = '*' * (2*i + 1)
    print(spaces + stars)
    
# Lower half
for i in range(n//2 - 1, -1, -1):
    spaces = ' ' * (n//2 - i)
    stars = '*' * (2*i + 1)
    print(spaces + stars)"""
        else:
            return f"# {pattern.name}\n# TODO: Implement this pattern\n# Formula: {pattern.formula}"
    
    elif language == "javascript":
        if pattern.id == 2:  # Right Triangle
            return """// Right Triangle Pattern
const n = 4;
for (let i = 1; i <= n; i++) {
    console.log('*'.repeat(i));
}"""
        else:
            return f"// {pattern.name}\n// TODO: Implement this pattern\n// Formula: {pattern.formula}"
    
    else:
        return f"// {pattern.name}\n// TODO: Implement this pattern\n// Formula: {pattern.formula}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



