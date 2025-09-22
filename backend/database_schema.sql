-- CodePatternMaster Database Schema
-- This file contains the SQL schema for the Supabase database

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Patterns table
CREATE TABLE IF NOT EXISTS patterns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    difficulty VARCHAR(20) NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    description TEXT NOT NULL,
    preview TEXT[] NOT NULL,
    rows INTEGER NOT NULL,
    popularity INTEGER DEFAULT 0 CHECK (popularity >= 0 AND popularity <= 100),
    completion_rate INTEGER DEFAULT 0 CHECK (completion_rate >= 0 AND completion_rate <= 100),
    formula TEXT NOT NULL,
    loops INTEGER NOT NULL DEFAULT 1,
    conditions INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    level INTEGER DEFAULT 1,
    experience_points INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    pattern_id INTEGER REFERENCES patterns(id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    best_score FLOAT DEFAULT 0.0 CHECK (best_score >= 0.0 AND best_score <= 1.0),
    time_spent INTEGER DEFAULT 0, -- in seconds
    last_attempt_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, pattern_id)
);

-- Code submissions table
CREATE TABLE IF NOT EXISTS code_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    pattern_id INTEGER REFERENCES patterns(id) ON DELETE CASCADE,
    language VARCHAR(50) NOT NULL,
    code TEXT NOT NULL,
    feedback TEXT,
    correctness_score FLOAT CHECK (correctness_score >= 0.0 AND correctness_score <= 1.0),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI analysis cache table
CREATE TABLE IF NOT EXISTS ai_analysis_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pattern_id INTEGER REFERENCES patterns(id) ON DELETE CASCADE,
    analysis_type VARCHAR(50) NOT NULL,
    analysis_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '24 hours')
);

-- User achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(100) NOT NULL,
    achievement_data JSONB,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_name VARCHAR(255),
    context TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patterns_category ON patterns(category);
CREATE INDEX IF NOT EXISTS idx_patterns_difficulty ON patterns(difficulty);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_pattern_id ON user_progress(pattern_id);
CREATE INDEX IF NOT EXISTS idx_code_submissions_user_id ON code_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_code_submissions_pattern_id ON code_submissions(pattern_id);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_cache_pattern_id ON ai_analysis_cache(pattern_id);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_cache_expires_at ON ai_analysis_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_patterns_updated_at BEFORE UPDATE ON patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE ON user_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample patterns
INSERT INTO patterns (name, category, difficulty, description, preview, rows, popularity, completion_rate, formula, loops, conditions) VALUES
('Square Pattern (Solid)', 'basic-star', 'easy', 'A solid square filled with stars', ARRAY['****', '****', '****', '****'], 4, 95, 92, 'stars = n, spaces = 0', 2, 0),
('Right Triangle Pattern', 'basic-star', 'easy', 'Stars forming a right triangle', ARRAY['*', '**', '***', '****'], 4, 98, 95, 'stars = i, spaces = 0', 2, 0),
('Left Triangle Pattern', 'basic-star', 'easy', 'Stars aligned to the left forming triangle', ARRAY['   *', '  **', ' ***', '****'], 4, 87, 89, 'stars = i, spaces = n-i', 2, 0),
('Inverted Right Triangle', 'basic-star', 'easy', 'Upside-down right triangle', ARRAY['****', '***', '**', '*'], 4, 85, 88, 'stars = n-i+1, spaces = 0', 2, 0),
('Isosceles Triangle', 'basic-star', 'easy', 'Centered triangle with equal sides', ARRAY['  *  ', ' *** ', '*****'], 3, 91, 90, 'stars = 2*i+1, spaces = n-i-1', 2, 0),
('Hollow Square', 'hollow', 'medium', 'Square with hollow interior', ARRAY['****', '*  *', '*  *', '****'], 4, 84, 76, 'stars = n (if first/last row/col), spaces = n-2 (middle)', 2, 4),
('Hollow Rectangle', 'hollow', 'medium', 'Rectangle with empty center', ARRAY['******', '*    *', '*    *', '******'], 4, 81, 74, 'stars = width (if first/last row/col), spaces = width-2 (middle)', 2, 4),
('Hollow Right Triangle', 'hollow', 'medium', 'Right triangle with hollow center', ARRAY['*', '**', '* *', '****'], 4, 78, 71, 'stars = i (if first/last col), spaces = i-2 (middle)', 2, 3),
('Diamond Pattern (Solid)', 'diamond', 'medium', 'Solid diamond shape', ARRAY['  *  ', ' *** ', '*****', ' *** ', '  *  '], 5, 89, 82, 'stars = 2*i+1 (upper), 2*(n-i-1)+1 (lower), spaces = n-i-1', 2, 1),
('Hollow Diamond', 'diamond', 'medium', 'Diamond with hollow center', ARRAY['  *  ', ' * * ', '*   *', ' * * ', '  *  '], 5, 85, 76, 'stars = 1 (if first/last), spaces = n-i-1 + i-1 (middle)', 2, 4),
('Number Triangle (1,2,3...)', 'number', 'easy', 'Triangle with sequential numbers', ARRAY['1', '12', '123', '1234'], 4, 92, 88, 'numbers = 1 to i', 2, 0),
('Floyd''s Triangle', 'number', 'medium', 'Sequential numbers in triangular form', ARRAY['1', '2 3', '4 5 6', '7 8 9 10'], 4, 84, 79, 'numbers = counter to counter+i-1', 2, 0),
('Butterfly Pattern', 'special', 'hard', 'Butterfly wing pattern', ARRAY['*    *', '**  **', '******', '**  **', '*    *'], 5, 91, 67, 'stars = i+1 (left), 2*(n-i-1) (right), spaces = 2*(n-i-1)', 2, 2),
('X Pattern (Cross)', 'special', 'medium', 'X or cross pattern', ARRAY['*   *', ' * * ', '  *  ', ' * * ', '*   *'], 5, 86, 78, 'stars = 1 (if i==j or i+j==n-1)', 2, 2)
ON CONFLICT DO NOTHING;

-- Create Row Level Security (RLS) policies
ALTER TABLE patterns ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_analysis_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- Patterns are publicly readable
CREATE POLICY "Patterns are publicly readable" ON patterns
    FOR SELECT USING (true);

-- Users can only access their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- User progress policies
CREATE POLICY "Users can view own progress" ON user_progress
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress" ON user_progress
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress" ON user_progress
    FOR UPDATE USING (auth.uid() = user_id);

-- Code submissions policies
CREATE POLICY "Users can view own submissions" ON code_submissions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own submissions" ON code_submissions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- AI analysis cache is publicly readable
CREATE POLICY "AI analysis cache is publicly readable" ON ai_analysis_cache
    FOR SELECT USING (true);

-- User achievements policies
CREATE POLICY "Users can view own achievements" ON user_achievements
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own achievements" ON user_achievements
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Chat sessions policies
CREATE POLICY "Users can view own chat sessions" ON chat_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own chat sessions" ON chat_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own chat sessions" ON chat_sessions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own chat sessions" ON chat_sessions
    FOR DELETE USING (auth.uid() = user_id);

-- Chat messages policies
CREATE POLICY "Users can view messages in own sessions" ON chat_messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM chat_sessions 
            WHERE chat_sessions.id = chat_messages.session_id 
            AND chat_sessions.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert messages in own sessions" ON chat_messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM chat_sessions 
            WHERE chat_sessions.id = chat_messages.session_id 
            AND chat_sessions.user_id = auth.uid()
        )
    );



