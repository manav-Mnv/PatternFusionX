"""
Database Operations for CodePatternMaster
Demonstrates Supabase integration for pattern storage and user progress tracking
"""

from supabase import create_client, Client
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database operations with Supabase"""

    def __init__(self):
        self.supabase: Client = None
        self._initialize_supabase()

    def _initialize_supabase(self):
        """Initialize Supabase client"""
        try:
            # In production, use environment variables
            supabase_url = os.getenv("SUPABASE_URL", "https://cmmxtopgavawhtbgkczw.supabase.co")
            supabase_key = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNtbXh0b3BnYXZhd2h0YmdrY3p3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgzNjE3NjAsImV4cCI6MjA3MzkzNzc2MH0.kufU6wv8CFLLk-3OZM-4Ex1Omezm0ohaRbdduvaWhSY")

            self.supabase = create_client(supabase_url, supabase_key)
            logger.info("✅ Database connection established")

        except Exception as e:
            logger.error(f"❌ Failed to connect to database: {e}")
            self.supabase = None

    async def save_user_progress(self, user_id: str, pattern_id: int, progress_data: Dict[str, Any]) -> bool:
        """Save user progress to database"""
        if not self.supabase:
            logger.warning("Database not available, skipping progress save")
            return False

        try:
            data = {
                "user_id": user_id,
                "pattern_id": pattern_id,
                "progress_percentage": progress_data.get("progress", 0),
                "time_spent": progress_data.get("time_spent", 0),
                "attempts": progress_data.get("attempts", 1),
                "completed": progress_data.get("completed", False),
                "last_attempt_at": datetime.utcnow().isoformat(),
                "code_submitted": progress_data.get("code", ""),
                "ai_feedback": progress_data.get("ai_feedback", {})
            }

            result = self.supabase.table("user_progress").insert(data).execute()
            logger.info(f"✅ User progress saved for pattern {pattern_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save user progress: {e}")
            return False

    async def get_user_progress(self, user_id: str, pattern_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get user progress from database"""
        if not self.supabase:
            return []

        try:
            query = self.supabase.table("user_progress").select("*").eq("user_id", user_id)

            if pattern_id:
                query = query.eq("pattern_id", pattern_id)

            result = query.order("last_attempt_at", desc=True).execute()
            return result.data

        except Exception as e:
            logger.error(f"❌ Failed to get user progress: {e}")
            return []

    async def save_pattern_attempt(self, user_id: str, pattern_id: int, code: str, success: bool) -> bool:
        """Save individual pattern attempt"""
        if not self.supabase:
            return False

        try:
            data = {
                "user_id": user_id,
                "pattern_id": pattern_id,
                "code_submitted": code,
                "success": success,
                "attempted_at": datetime.utcnow().isoformat(),
                "ai_analysis": {}  # Will be filled by AI analysis
            }

            result = self.supabase.table("pattern_attempts").insert(data).execute()
            logger.info(f"✅ Pattern attempt saved for pattern {pattern_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save pattern attempt: {e}")
            return False

    async def get_pattern_statistics(self, pattern_id: int) -> Dict[str, Any]:
        """Get statistics for a specific pattern"""
        if not self.supabase:
            return {"total_attempts": 0, "success_rate": 0, "average_time": 0}

        try:
            # Get all attempts for this pattern
            result = self.supabase.table("pattern_attempts").select("*").eq("pattern_id", pattern_id).execute()

            if not result.data:
                return {"total_attempts": 0, "success_rate": 0, "average_time": 0}

            attempts = result.data
            successful_attempts = sum(1 for attempt in attempts if attempt.get("success", False))

            return {
                "total_attempts": len(attempts),
                "success_rate": successful_attempts / len(attempts),
                "average_time": 0,  # Would calculate from user_progress table
                "difficulty_trend": "increasing" if successful_attempts > len(attempts) * 0.7 else "challenging"
            }

        except Exception as e:
            logger.error(f"❌ Failed to get pattern statistics: {e}")
            return {"total_attempts": 0, "success_rate": 0, "average_time": 0}

    async def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user leaderboard based on progress"""
        if not self.supabase:
            return []

        try:
            # This would be a more complex query in a real application
            # For now, return mock data
            return [
                {"user_id": "user1", "patterns_completed": 15, "total_time": 1200},
                {"user_id": "user2", "patterns_completed": 12, "total_time": 980},
                {"user_id": "user3", "patterns_completed": 10, "total_time": 850}
            ]

        except Exception as e:
            logger.error(f"❌ Failed to get leaderboard: {e}")
            return []

    async def save_ai_analysis(self, user_id: str, pattern_id: int, analysis_data: Dict[str, Any]) -> bool:
        """Save AI analysis results to database"""
        if not self.supabase:
            return False

        try:
            data = {
                "user_id": user_id,
                "pattern_id": pattern_id,
                "analysis_type": analysis_data.get("type", "general"),
                "complexity_score": analysis_data.get("complexity_score", 0),
                "suggestions": analysis_data.get("suggestions", []),
                "explanation": analysis_data.get("explanation", ""),
                "analyzed_at": datetime.utcnow().isoformat()
            }

            result = self.supabase.table("ai_analyses").insert(data).execute()
            logger.info(f"✅ AI analysis saved for pattern {pattern_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save AI analysis: {e}")
            return False

# Global database instance
db_manager = DatabaseManager()

async def save_user_learning_path(user_id: str, learning_data: Dict[str, Any]) -> bool:
    """Save user's learning journey"""
    return await db_manager.save_user_progress(
        user_id,
        learning_data.get("current_pattern", 1),
        {
            "progress": learning_data.get("progress", 0),
            "time_spent": learning_data.get("time_spent", 0),
            "completed": learning_data.get("completed", False),
            "ai_feedback": learning_data.get("ai_feedback", {})
        }
    )
