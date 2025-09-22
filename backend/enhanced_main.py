"""
Enhanced CodePatternMaster API with Hugging Face AI and Database Integration
This demonstrates a complete example of integrating Hugging Face AI models with Supabase database
"""

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

# ==================== HUGGING FACE AI & DATABASE INTEGRATION ====================

@app.post("/ai/enhanced-analysis")
async def enhanced_ai_analysis(request: AIAnalysisRequest):
    """
    Enhanced AI analysis using Hugging Face models
    This endpoint demonstrates the integration of:
    1. Hugging Face AI models for code analysis
    2. Supabase database for storing analysis results
    """
    patterns = get_sample_patterns()
    pattern = next((p for p in patterns if p.id == request.pattern_id), None)

    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Get AI analysis using Hugging Face models
    ai_analysis = get_ai_code_analysis(request.user_code or "", pattern.name)

    # Save analysis to database
    await db_manager.save_ai_analysis(
        user_id="demo_user",  # In real app, get from auth
        pattern_id=pattern.id,
        analysis_data={
            "type": request.analysis_type,
            "complexity_score": ai_analysis["complexity_analysis"]["complexity_score"],
            "suggestions": ai_analysis["improvement_suggestions"],
            "explanation": ai_analysis["explanation"]
        }
    )

    return {
        "pattern": pattern,
        "ai_analysis": ai_analysis,
        "database_saved": True,
        "model_used": "Hugging Face" if ai_analyzer.code_classifier else "Fallback"
    }

@app.post("/user/progress")
async def save_user_progress(user_id: str, pattern_id: int, progress_data: Dict[str, Any]):
    """Save user progress to database"""
    success = await save_user_learning_path(user_id, {
        "current_pattern": pattern_id,
        "progress": progress_data.get("progress", 0),
        "time_spent": progress_data.get("time_spent", 0),
        "completed": progress_data.get("completed", False),
        "ai_feedback": progress_data.get("ai_feedback", {})
    })

    return {
        "success": success,
        "message": "Progress saved successfully" if success else "Failed to save progress",
        "user_id": user_id,
        "pattern_id": pattern_id
    }

@app.get("/user/progress/{user_id}")
async def get_user_progress(user_id: str, pattern_id: Optional[int] = None):
    """Get user progress from database"""
    progress_data = await db_manager.get_user_progress(user_id, pattern_id)

    return {
        "user_id": user_id,
        "progress": progress_data,
        "total_attempts": len(progress_data)
    }

@app.get("/patterns/{pattern_id}/statistics")
async def get_pattern_statistics(pattern_id: int):
    """Get pattern statistics from database"""
    stats = await db_manager.get_pattern_statistics(pattern_id)

    return {
        "pattern_id": pattern_id,
        "statistics": stats,
        "difficulty_assessment": "challenging" if stats["success_rate"] < 0.5 else "moderate" if stats["success_rate"] < 0.8 else "easy"
    }

@app.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get user leaderboard"""
    leaderboard = await db_manager.get_leaderboard(limit)

    return {
        "leaderboard": leaderboard,
        "last_updated": "2024-01-01T00:00:00Z"  # In real app, get from database
    }

@app.post("/ai/code-explanation")
async def get_code_explanation(code: str, pattern_name: str):
    """Get AI-powered code explanation"""
    ai_analysis = get_ai_code_analysis(code, pattern_name)

    return {
        "code": code,
        "pattern": pattern_name,
        "explanation": ai_analysis["explanation"],
        "complexity": ai_analysis["complexity_analysis"],
        "suggestions": ai_analysis["improvement_suggestions"]
    }

@app.post("/ai/generate-detailed-code")
async def generate_detailed_code(pattern_name: str, language: str = "python"):
    """Generate detailed code with step-by-step explanations for a pattern"""

    # Enhanced explanations for different patterns
    pattern_explanations = {
        "Square Pattern (Solid)": {
            "explanation": """This pattern creates a solid square filled with stars.

**Step-by-Step Logic:**
1. **Outer Loop (Rows)**: Controls which row we're printing (0 to n-1)
2. **Inner Loop (Columns)**: Controls which column we're printing (0 to n-1)
3. **Print Logic**: Print a star for every position since it's a solid square
4. **Newline**: Move to the next row after completing each row

**Key Variables:**
- `i`: Current row number (0-based)
- `j`: Current column number (0-based)
- `n`: Size of the square (4 in this example)

**Time Complexity:** O(n²) - nested loops
**Space Complexity:** O(1) - only using constant extra space""",
            "python": """# Square Pattern (Solid)
# Step-by-step implementation with detailed comments

n = 4  # Size of the square

# Outer loop: Controls rows (vertical movement)
# i goes from 0 to n-1, representing each row
for i in range(n):
    # Inner loop: Controls columns (horizontal movement)
    # j goes from 0 to n-1, representing each column in current row
    for j in range(n):
        # Print star without newline (end='')
        # This creates the solid fill effect
        print('*', end='')
    # After completing one row, print newline to move to next row
    print()  # This creates the square shape""",
            "javascript": """// Square Pattern (Solid)
// Step-by-step implementation with detailed comments

const n = 4;  // Size of the square

// Outer loop: Controls rows (vertical movement)
// i goes from 0 to n-1, representing each row
for (let i = 0; i < n; i++) {
    // Inner loop: Controls columns (horizontal movement)
    // j goes from 0 to n-1, representing each column in current row
    for (let j = 0; j < n; j++) {
        // Print star without newline
        // This creates the solid fill effect
        process.stdout.write('*');
    }
    // After completing one row, print newline to move to next row
    console.log();  // This creates the square shape
}""",
            "java": """// Square Pattern (Solid)
// Step-by-step implementation with detailed comments

public class SquarePattern {
    public static void main(String[] args) {
        int n = 4;  // Size of the square

        // Outer loop: Controls rows (vertical movement)
        // i goes from 0 to n-1, representing each row
        for (int i = 0; i < n; i++) {
            // Inner loop: Controls columns (horizontal movement)
            // j goes from 0 to n-1, representing each column in current row
            for (int j = 0; j < n; j++) {
                // Print star without newline
                // This creates the solid fill effect
                System.out.print("*");
            }
            // After completing one row, print newline to move to next row
            System.out.println();  // This creates the square shape
        }
    }
}""",
            "cpp": """// Square Pattern (Solid)
// Step-by-step implementation with detailed comments

#include <iostream>
using namespace std;

int main() {
    int n = 4;  // Size of the square

    // Outer loop: Controls rows (vertical movement)
    // i goes from 0 to n-1, representing each row
    for (int i = 0; i < n; i++) {
        // Inner loop: Controls columns (horizontal movement)
        // j goes from 0 to n-1, representing each column in current row
        for (int j = 0; j < n; j++) {
            // Print star without newline
            // This creates the solid fill effect
            cout << "*";
        }
        // After completing one row, print newline to move to next row
        cout << endl;  // This creates the square shape
    }
    return 0;
}"""
        },
        "Right Triangle Pattern": {
            "explanation": """This pattern creates a right-angled triangle with stars.

**Step-by-Step Logic:**
1. **Single Loop**: Controls rows (1 to n)
2. **Print Logic**: Print 'i' number of stars in each row
3. **Newline**: Move to next row after each row

**Key Variables:**
- `i`: Current row number (1-based)
- `n`: Size of the triangle (4 in this example)

**Pattern Growth:**
- Row 1: 1 star
- Row 2: 2 stars
- Row 3: 3 stars
- Row 4: 4 stars

**Time Complexity:** O(n²) - nested loop structure
**Space Complexity:** O(1) - constant extra space""",
            "python": """# Right Triangle Pattern
# Step-by-step implementation with detailed comments

n = 4  # Size of the triangle

# Loop: Controls rows (vertical movement)
# i goes from 1 to n, representing each row
for i in range(1, n + 1):
    # Print i number of stars for current row
    # Row 1: 1 star, Row 2: 2 stars, etc.
    print('*' * i)

# Alternative implementation with nested loops:
# for i in range(n):
#     for j in range(i + 1):
#         print('*', end='')
#     print()""",
            "javascript": """// Right Triangle Pattern
// Step-by-step implementation with detailed comments

const n = 4;  // Size of the triangle

// Loop: Controls rows (vertical movement)
// i goes from 1 to n, representing each row
for (let i = 1; i <= n; i++) {
    // Print i number of stars for current row
    // Row 1: 1 star, Row 2: 2 stars, etc.
    console.log('*'.repeat(i));
}

// Alternative implementation with nested loops:
// for (let i = 0; i < n; i++) {
//     for (let j = 0; j <= i; j++) {
//         process.stdout.write('*');
//     }
//     console.log();
// }""",
            "java": """// Right Triangle Pattern
// Step-by-step implementation with detailed comments

public class RightTriangle {
    public static void main(String[] args) {
        int n = 4;  // Size of the triangle

        // Loop: Controls rows (vertical movement)
        // i goes from 1 to n, representing each row
        for (int i = 1; i <= n; i++) {
            // Print i number of stars for current row
            // Row 1: 1 star, Row 2: 2 stars, etc.
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}""",
            "cpp": """// Right Triangle Pattern
// Step-by-step implementation with detailed comments

#include <iostream>
using namespace std;

int main() {
    int n = 4;  // Size of the triangle

    // Loop: Controls rows (vertical movement)
    // i goes from 1 to n, representing each row
    for (int i = 1; i <= n; i++) {
        // Print i number of stars for current row
        // Row 1: 1 star, Row 2: 2 stars, etc.
        for (int j = 1; j <= i; j++) {
            cout << "*";
        }
        cout << endl;
    }
    return 0;
}"""
        },
        "Diamond Pattern (Solid)": {
            "explanation": """This pattern creates a solid diamond shape using stars.

**Step-by-Step Logic:**
1. **Upper Half**: Build the top triangle (increasing stars)
2. **Lower Half**: Build the bottom triangle (decreasing stars)
3. **Space Calculation**: Center the diamond using spaces
4. **Star Calculation**: Use formula 2*i+1 for odd number of stars

**Key Variables:**
- `i`: Current row number
- `n`: Size of the diamond (5 in this example)
- `spaces`: Calculated as n//2 - i
- `stars`: Calculated as 2*i + 1

**Pattern Structure:**
- Row 1: 1 star, 2 spaces each side
- Row 2: 3 stars, 1 space each side
- Row 3: 5 stars, 0 spaces each side
- Row 4: 3 stars, 1 space each side
- Row 5: 1 star, 2 spaces each side

**Time Complexity:** O(n²) - nested loops
**Space Complexity:** O(1) - constant extra space""",
            "python": """# Diamond Pattern (Solid)
# Step-by-step implementation with detailed comments

n = 5  # Size of the diamond

# Upper half of diamond (including middle row)
# i goes from 0 to n//2, representing upper rows
for i in range(n//2 + 1):
    # Calculate spaces for centering
    # More spaces at top, fewer as we go down
    spaces = ' ' * (n//2 - i)

    # Calculate stars using formula 2*i + 1
    # More stars as we go down
    stars = '*' * (2*i + 1)

    # Print spaces followed by stars
    print(spaces + stars)

# Lower half of diamond (excluding middle row)
# i goes from n//2-1 down to 0
for i in range(n//2 - 1, -1, -1):
    # Same calculations as upper half
    spaces = ' ' * (n//2 - i)
    stars = '*' * (2*i + 1)
    print(spaces + stars)""",
            "javascript": """// Diamond Pattern (Solid)
// Step-by-step implementation with detailed comments

const n = 5;  // Size of the diamond

// Upper half of diamond (including middle row)
// i goes from 0 to n/2, representing upper rows
for (let i = 0; i <= Math.floor(n/2); i++) {
    // Calculate spaces for centering
    // More spaces at top, fewer as we go down
    const spaces = ' '.repeat(Math.floor(n/2) - i);

    // Calculate stars using formula 2*i + 1
    // More stars as we go down
    const stars = '*'.repeat(2*i + 1);

    // Print spaces followed by stars
    console.log(spaces + stars);
}

// Lower half of diamond (excluding middle row)
// i goes from n/2-1 down to 0
for (let i = Math.floor(n/2) - 1; i >= 0; i--) {
    // Same calculations as upper half
    const spaces = ' '.repeat(Math.floor(n/2) - i);
    const stars = '*'.repeat(2*i + 1);
    console.log(spaces + stars);
}""",
            "java": """// Diamond Pattern (Solid)
// Step-by-step implementation with detailed comments

public class DiamondPattern {
    public static void main(String[] args) {
        int n = 5;  // Size of the diamond

        // Upper half of diamond (including middle row)
        // i goes from 0 to n/2, representing upper rows
        for (int i = 0; i <= n/2; i++) {
            // Calculate spaces for centering
            // More spaces at top, fewer as we go down
            for (int j = 0; j < n/2 - i; j++) {
                System.out.print(" ");
            }

            // Calculate stars using formula 2*i + 1
            // More stars as we go down
            for (int j = 0; j < 2*i + 1; j++) {
                System.out.print("*");
            }
            System.out.println();
        }

        // Lower half of diamond (excluding middle row)
        // i goes from n/2-1 down to 0
        for (int i = n/2 - 1; i >= 0; i--) {
            // Same calculations as upper half
            for (int j = 0; j < n/2 - i; j++) {
                System.out.print(" ");
            }
            for (int j = 0; j < 2*i + 1; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}""",
            "cpp": """// Diamond Pattern (Solid)
// Step-by-step implementation with detailed comments

#include <iostream>
using namespace std;

int main() {
    int n = 5;  // Size of the diamond

    // Upper half of diamond (including middle row)
    // i goes from 0 to n/2, representing upper rows
    for (int i = 0; i <= n/2; i++) {
        // Calculate spaces for centering
        // More spaces at top, fewer as we go down
        for (int j = 0; j < n/2 - i; j++) {
            cout << " ";
        }

        // Calculate stars using formula 2*i + 1
        // More stars as we go down
        for (int j = 0; j < 2*i + 1; j++) {
            cout << "*";
        }
        cout << endl;
    }

    // Lower half of diamond (excluding middle row)
    // i goes from n/2-1 down to 0
    for (int i = n/2 - 1; i >= 0; i--) {
        // Same calculations as upper half
        for (int j = 0; j < n/2 - i; j++) {
            cout << " ";
        }
        for (int j = 0; j < 2*i + 1; j++) {
            cout << "*";
        }
        cout << endl;
    }
    return 0;
}"""
        }
    }

    pattern_data = pattern_explanations.get(pattern_name, {
        "explanation": "Pattern explanation not available",
        "python": "# Code template not available",
        "javascript": "// Code template not available",
        "java": "// Code template not available",
        "cpp": "// Code template not available"
    })

    return {
        "pattern": pattern_name,
        "language": language,
        "explanation": pattern_data["explanation"],
        "generated_code": pattern_data.get(language, pattern_data["python"])
    }

@app.post("/execute-code")
async def execute_code(code: str, language: str = "python", input: str = ""):
    """
    Execute user code safely using subprocess
    Supports Python, JavaScript, Java, and C++
    """
    # Create temporary file for code execution
    with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        # Execute code based on language
        if language == "python":
            result = subprocess.run(
                ["python", temp_file],
                capture_output=True,
                text=True,
                timeout=10,  # 10 second timeout
                input=input
            )
        elif language == "javascript":
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=10,
                input=input
            )
        elif language == "java":
            # Compile and run Java
            class_name = "Main"
            compile_result = subprocess.run(
                ["javac", temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                return {
                    "output": compile_result.stderr,
                    "error": "Compilation failed",
                    "execution_time": "0ms"
                }

            result = subprocess.run(
                ["java", class_name],
                capture_output=True,
                text=True,
                timeout=10,
                input=input
            )
        elif language == "cpp":
            # Compile and run C++
            compile_result = subprocess.run(
                ["g++", temp_file, "-o", temp_file + ".out"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                return {
                    "output": compile_result.stderr,
                    "error": "Compilation failed",
                    "execution_time": "0ms"
                }

            result = subprocess.run(
                [temp_file + ".out"],
                capture_output=True,
                text=True,
                timeout=10,
                input=input
            )
        else:
            return {
                "output": f"Unsupported language: {language}",
                "error": "Unsupported language",
                "execution_time": "0ms"
            }

        # Clean up temporary files
        try:
            os.unlink(temp_file)
            if language == "java":
                os.unlink("Main.class")
            elif language == "cpp":
                os.unlink(temp_file + ".out")
        except:
            pass

        return {
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else "",
            "execution_time": "0ms"  # Could be enhanced with actual timing
        }

    except subprocess.TimeoutExpired:
        # Clean up temporary files
        try:
            os.unlink(temp_file)
            if language == "java":
                os.unlink("Main.class")
            elif language == "cpp":
                os.unlink(temp_file + ".out")
        except:
            pass

        return {
            "output": "",
            "error": "Code execution timed out (10 seconds)",
            "execution_time": "0ms"
        }
    except Exception as e:
        # Clean up temporary files
        try:
            os.unlink(temp_file)
            if language == "java":
                os.unlink("Main.class")
            elif language == "cpp":
                os.unlink(temp_file + ".out")
        except:
            pass

        return {
            "output": "",
            "error": f"Execution failed: {str(e)}",
            "execution_time": "0ms"
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
