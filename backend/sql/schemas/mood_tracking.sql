-- Mood Tracking Schema
-- Handles daily mood check-ins, mood patterns, and emotional state tracking

-- Mood scale enumeration (1-10 scale)
CREATE TYPE mood_scale AS ENUM ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10');

-- Anxiety level enumeration
CREATE TYPE anxiety_level AS ENUM ('none', 'mild', 'moderate', 'high', 'severe');

-- Energy level enumeration
CREATE TYPE energy_level AS ENUM ('very_low', 'low', 'moderate', 'high', 'very_high');

-- Sleep quality enumeration
CREATE TYPE sleep_quality AS ENUM ('very_poor', 'poor', 'fair', 'good', 'excellent');

-- Stress level enumeration
CREATE TYPE stress_level AS ENUM ('none', 'low', 'moderate', 'high', 'overwhelming');

-- Primary mood entries table
CREATE TABLE mood_entries (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    entry_date DATE NOT NULL,
    entry_time TIME WITH TIME ZONE DEFAULT CURRENT_TIME,
    
    -- Core mood metrics
    overall_mood mood_scale NOT NULL,
    anxiety_level anxiety_level,
    stress_level stress_level,
    energy_level energy_level,
    sleep_quality sleep_quality,
    sleep_hours DECIMAL(3,1), -- e.g., 7.5 hours
    
    -- Additional metrics
    medication_taken BOOLEAN,
    medication_notes TEXT,
    exercise_minutes INTEGER DEFAULT 0,
    social_interaction_quality mood_scale,
    productivity_level mood_scale,
    
    -- Emotional state tags
    emotions TEXT[], -- ['happy', 'anxious', 'hopeful', 'frustrated']
    triggers TEXT[], -- ['work_stress', 'family_conflict', 'financial_worry']
    coping_strategies TEXT[], -- ['deep_breathing', 'exercise', 'journaling']
    
    -- Contextual information
    weather VARCHAR(50),
    location_type VARCHAR(50), -- 'home', 'work', 'outdoors', 'social'
    
    -- Free text for additional context
    notes TEXT,
    gratitude_note TEXT,
    
    -- Goal tracking
    daily_goals_met INTEGER DEFAULT 0,
    daily_goals_total INTEGER DEFAULT 0,
    
    -- Metadata
    data_source VARCHAR(50) DEFAULT 'manual', -- 'manual', 'wearable', 'ai_prompt'
    confidence_score DECIMAL(3,2), -- AI confidence in mood detection (0-1)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_unique_daily_entry UNIQUE(user_id, entry_date),
    CONSTRAINT chk_sleep_hours_valid CHECK (sleep_hours IS NULL OR (sleep_hours >= 0 AND sleep_hours <= 24)),
    CONSTRAINT chk_exercise_minutes_valid CHECK (exercise_minutes >= 0 AND exercise_minutes <= 1440),
    CONSTRAINT chk_goals_valid CHECK (daily_goals_met <= daily_goals_total),
    CONSTRAINT chk_confidence_score_valid CHECK (confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1))
);

-- Mood patterns and trends analysis
CREATE TABLE mood_patterns (
    pattern_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    pattern_type VARCHAR(50) NOT NULL, -- 'weekly', 'monthly', 'seasonal', 'trigger_based'
    pattern_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Pattern metrics
    average_mood DECIMAL(3,2),
    mood_variance DECIMAL(5,4),
    trend_direction VARCHAR(20), -- 'improving', 'declining', 'stable', 'volatile'
    
    -- Time-based patterns
    start_date DATE,
    end_date DATE,
    days_of_week INTEGER[], -- [1,2,3,4,5] for weekdays
    time_of_day_start TIME,
    time_of_day_end TIME,
    
    -- Pattern triggers and correlations
    common_triggers TEXT[],
    common_emotions TEXT[],
    effective_coping_strategies TEXT[],
    
    -- Statistical data
    sample_size INTEGER NOT NULL DEFAULT 0,
    confidence_level DECIMAL(5,4),
    
    -- Metadata
    detected_by VARCHAR(50) DEFAULT 'ai_analysis', -- 'ai_analysis', 'manual', 'therapist'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_average_mood_valid CHECK (average_mood >= 1 AND average_mood <= 10),
    CONSTRAINT chk_sample_size_positive CHECK (sample_size >= 0),
    CONSTRAINT chk_date_range_valid CHECK (start_date IS NULL OR end_date IS NULL OR start_date <= end_date)
);

-- Mood goals and targets
CREATE TABLE mood_goals (
    goal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    goal_type VARCHAR(50) NOT NULL, -- 'mood_stability', 'anxiety_reduction', 'sleep_improvement'
    goal_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Goal metrics
    target_metric VARCHAR(50) NOT NULL, -- 'overall_mood', 'anxiety_level', 'sleep_hours'
    target_value DECIMAL(5,2) NOT NULL,
    target_operator VARCHAR(10) NOT NULL, -- '>=', '<=', '=', 'between'
    target_frequency VARCHAR(50), -- 'daily', 'weekly', '5_days_per_week'
    
    -- Time frame
    start_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Progress tracking
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    total_successes INTEGER DEFAULT 0,
    total_attempts INTEGER DEFAULT 0,
    
    -- Metadata
    created_by UUID REFERENCES users(user_id), -- therapist or self
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT chk_goal_date_range CHECK (end_date IS NULL OR start_date <= end_date),
    CONSTRAINT chk_target_operator_valid CHECK (target_operator IN ('>=', '<=', '=', 'between')),
    CONSTRAINT chk_streak_values CHECK (current_streak >= 0 AND best_streak >= 0),
    CONSTRAINT chk_progress_values CHECK (total_successes >= 0 AND total_attempts >= 0 AND total_successes <= total_attempts)
);

-- Mood entry reminders and notifications
CREATE TABLE mood_reminders (
    reminder_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    reminder_name VARCHAR(100) NOT NULL,
    reminder_time TIME NOT NULL,
    days_of_week INTEGER[] NOT NULL, -- [1,2,3,4,5,6,7] for all days
    is_active BOOLEAN DEFAULT TRUE,
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Reminder content
    message TEXT,
    prompt_type VARCHAR(50), -- 'basic', 'gratitude', 'reflection', 'cbt'
    
    -- Tracking
    total_sent INTEGER DEFAULT 0,
    total_responded INTEGER DEFAULT 0,
    last_sent TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_days_of_week_valid CHECK (
        array_length(days_of_week, 1) > 0 AND 
        days_of_week <@ ARRAY[1,2,3,4,5,6,7]
    )
);

-- Mood insights and analytics
CREATE TABLE mood_insights (
    insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    insight_type VARCHAR(50) NOT NULL, -- 'correlation', 'trend', 'recommendation', 'alert'
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    
    -- Insight data
    insight_data JSONB, -- Flexible storage for various insight types
    confidence_score DECIMAL(3,2),
    importance_level VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    
    -- Time relevance
    relevant_from DATE,
    relevant_until DATE,
    
    -- Action items
    recommendations TEXT[],
    action_taken BOOLEAN DEFAULT FALSE,
    action_notes TEXT,
    
    -- Generation metadata
    generated_by VARCHAR(50) DEFAULT 'ai', -- 'ai', 'therapist', 'system'
    algorithm_version VARCHAR(20),
    data_period_start DATE,
    data_period_end DATE,
    
    -- User interaction
    viewed_at TIMESTAMP WITH TIME ZONE,
    dismissed_at TIMESTAMP WITH TIME ZONE,
    shared_with_therapist BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_confidence_score_valid CHECK (confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1)),
    CONSTRAINT chk_importance_level_valid CHECK (importance_level IN ('low', 'medium', 'high', 'critical')),
    CONSTRAINT chk_relevance_period CHECK (relevant_from IS NULL OR relevant_until IS NULL OR relevant_from <= relevant_until)
);

-- Indexes for performance
CREATE INDEX idx_mood_entries_user_id ON mood_entries(user_id);
CREATE INDEX idx_mood_entries_date ON mood_entries(entry_date);
CREATE INDEX idx_mood_entries_user_date ON mood_entries(user_id, entry_date);
CREATE INDEX idx_mood_entries_overall_mood ON mood_entries(overall_mood);
CREATE INDEX idx_mood_entries_created_at ON mood_entries(created_at);
CREATE INDEX idx_mood_patterns_user_id ON mood_patterns(user_id);
CREATE INDEX idx_mood_patterns_type ON mood_patterns(pattern_type);
CREATE INDEX idx_mood_goals_user_id ON mood_goals(user_id);
CREATE INDEX idx_mood_goals_active ON mood_goals(is_active);
CREATE INDEX idx_mood_reminders_user_id ON mood_reminders(user_id);
CREATE INDEX idx_mood_reminders_active ON mood_reminders(is_active);
CREATE INDEX idx_mood_insights_user_id ON mood_insights(user_id);
CREATE INDEX idx_mood_insights_type ON mood_insights(insight_type);
CREATE INDEX idx_mood_insights_importance ON mood_insights(importance_level);

-- Triggers for updated_at
CREATE TRIGGER update_mood_entries_updated_at BEFORE UPDATE ON mood_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_mood_patterns_updated_at BEFORE UPDATE ON mood_patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_mood_goals_updated_at BEFORE UPDATE ON mood_goals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_mood_reminders_updated_at BEFORE UPDATE ON mood_reminders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Mood-specific utility function (requires mood_entries table to exist)
CREATE OR REPLACE FUNCTION calculate_mood_trend(
    user_id_param UUID,
    days_back INTEGER DEFAULT 30
)
RETURNS TEXT AS $$
DECLARE
    recent_avg DECIMAL;
    older_avg DECIMAL;
    trend TEXT;
BEGIN
    -- Get recent average (last 7 days)
    SELECT AVG(overall_mood::INTEGER)
    INTO recent_avg
    FROM mood_entries
    WHERE user_id = user_id_param
      AND entry_date >= CURRENT_DATE - INTERVAL '7 days'
      AND entry_date >= CURRENT_DATE - INTERVAL (days_back || ' days');
    
    -- Get older average (8-30 days back)
    SELECT AVG(overall_mood::INTEGER)
    INTO older_avg
    FROM mood_entries
    WHERE user_id = user_id_param
      AND entry_date < CURRENT_DATE - INTERVAL '7 days'
      AND entry_date >= CURRENT_DATE - INTERVAL (days_back || ' days');
    
    -- Determine trend
    IF recent_avg IS NULL OR older_avg IS NULL THEN
        RETURN 'insufficient_data';
    ELSIF recent_avg > older_avg + 0.5 THEN
        RETURN 'improving';
    ELSIF recent_avg < older_avg - 0.5 THEN
        RETURN 'declining';
    ELSE
        RETURN 'stable';
    END IF;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION calculate_mood_trend(UUID, INTEGER) IS 'Calculates mood trend for a user over specified time period';
