-- Journaling Schema
-- Handles journaling entries, prompts, reflection guidance, and CBT techniques

-- Journal entry types
CREATE TYPE journal_entry_type AS ENUM (
    'free_writing',
    'guided_prompt',
    'gratitude',
    'cbt_thought_record',
    'daily_reflection',
    'goal_setting',
    'mood_exploration',
    'trigger_analysis',
    'coping_strategies',
    'therapy_homework'
);

-- CBT technique types
CREATE TYPE cbt_technique AS ENUM (
    'thought_challenging',
    'behavioral_activation',
    'exposure_therapy',
    'mindfulness',
    'problem_solving',
    'cognitive_restructuring',
    'activity_scheduling',
    'relaxation_techniques',
    'grounding_exercises'
);

-- Emotional intensity scale
CREATE TYPE intensity_scale AS ENUM ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10');

-- Journal entries table
CREATE TABLE journal_entries (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    entry_type journal_entry_type NOT NULL DEFAULT 'free_writing',
    
    -- Content
    title VARCHAR(200),
    content TEXT NOT NULL,
    word_count INTEGER DEFAULT 0,
    
    -- Prompts and guidance
    prompt_id UUID, -- References journal_prompts table
    prompt_question TEXT,
    
    -- Emotional context
    emotions_before TEXT[], -- emotions before writing
    emotions_after TEXT[], -- emotions after writing
    mood_before intensity_scale,
    mood_after intensity_scale,
    
    -- CBT-specific fields
    cbt_technique cbt_technique,
    situation_description TEXT,
    automatic_thoughts TEXT,
    cognitive_distortions TEXT[],
    evidence_for TEXT,
    evidence_against TEXT,
    balanced_thought TEXT,
    behavioral_response TEXT,
    intensity_before intensity_scale,
    intensity_after intensity_scale,
    
    -- Gratitude-specific fields
    gratitude_items TEXT[],
    gratitude_reasons TEXT,
    
    -- Goal and action items
    goals_mentioned TEXT[],
    action_items TEXT[],
    insights_gained TEXT,
    
    -- Privacy and sharing
    is_private BOOLEAN DEFAULT TRUE,
    shared_with_therapist BOOLEAN DEFAULT FALSE,
    shared_at TIMESTAMP WITH TIME ZONE,
    
    -- AI analysis
    sentiment_score DECIMAL(3,2), -- -1 to 1 scale
    emotion_analysis JSONB,
    key_themes TEXT[],
    risk_indicators TEXT[],
    ai_insights TEXT,
    
    -- Metadata
    writing_duration_minutes INTEGER, -- time spent writing
    device_type VARCHAR(50),
    location_written VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_word_count_positive CHECK (word_count >= 0),
    CONSTRAINT chk_sentiment_range CHECK (sentiment_score IS NULL OR (sentiment_score >= -1 AND sentiment_score <= 1)),
    CONSTRAINT chk_duration_positive CHECK (writing_duration_minutes IS NULL OR writing_duration_minutes >= 0)
);

-- Journal prompts library
CREATE TABLE journal_prompts (
    prompt_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    prompt_type journal_entry_type NOT NULL,
    
    -- Prompt content
    question TEXT NOT NULL,
    description TEXT,
    follow_up_questions TEXT[],
    
    -- CBT-specific prompt data
    cbt_technique cbt_technique,
    therapeutic_goal VARCHAR(100),
    difficulty_level VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    
    -- Targeting and personalization
    target_emotions TEXT[],
    target_situations TEXT[],
    age_group VARCHAR(20), -- 'teen', 'adult', 'senior', 'all'
    clinical_conditions TEXT[], -- 'anxiety', 'depression', 'ptsd', etc.
    
    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    effectiveness_rating DECIMAL(3,2), -- average user rating
    
    -- Content management
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(user_id),
    approved_by UUID REFERENCES users(user_id),
    language VARCHAR(10) DEFAULT 'en',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_effectiveness_rating CHECK (effectiveness_rating IS NULL OR (effectiveness_rating >= 0 AND effectiveness_rating <= 5))
);

-- User's prompt history and preferences
CREATE TABLE user_prompt_history (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    prompt_id UUID NOT NULL REFERENCES journal_prompts(prompt_id),
    
    -- Usage data
    presented_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP WITH TIME ZONE,
    skipped_at TIMESTAMP WITH TIME ZONE,
    
    -- User feedback
    helpfulness_rating INTEGER, -- 1-5 scale
    difficulty_rating INTEGER, -- 1-5 scale
    user_notes TEXT,
    
    -- Outcome tracking
    completed_writing BOOLEAN DEFAULT FALSE,
    mood_improvement BOOLEAN,
    insights_gained BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT chk_helpfulness_rating CHECK (helpfulness_rating IS NULL OR (helpfulness_rating >= 1 AND helpfulness_rating <= 5)),
    CONSTRAINT chk_difficulty_rating CHECK (difficulty_rating IS NULL OR (difficulty_rating >= 1 AND difficulty_rating <= 5))
);

-- Journaling streaks and statistics
CREATE TABLE journaling_stats (
    stats_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Streak tracking
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_entry_date DATE,
    
    -- Totals
    total_entries INTEGER DEFAULT 0,
    total_words_written INTEGER DEFAULT 0,
    total_writing_time_minutes INTEGER DEFAULT 0,
    
    -- By type
    free_writing_count INTEGER DEFAULT 0,
    guided_prompt_count INTEGER DEFAULT 0,
    gratitude_count INTEGER DEFAULT 0,
    cbt_count INTEGER DEFAULT 0,
    
    -- Monthly targets and achievements
    monthly_target INTEGER DEFAULT 15, -- entries per month
    current_month_count INTEGER DEFAULT 0,
    months_target_achieved INTEGER DEFAULT 0,
    
    -- Insights and progress
    average_mood_improvement DECIMAL(3,2),
    most_common_emotions TEXT[],
    most_effective_techniques TEXT[],
    
    -- Time-based stats
    preferred_writing_times TIME[],
    average_session_duration DECIMAL(5,2),
    
    -- Last calculation
    last_calculated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_streak_values CHECK (current_streak >= 0 AND longest_streak >= 0),
    CONSTRAINT chk_count_values CHECK (
        total_entries >= 0 AND 
        total_words_written >= 0 AND 
        total_writing_time_minutes >= 0 AND
        current_month_count >= 0
    )
);

-- Journaling goals and challenges
CREATE TABLE journaling_goals (
    goal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Goal definition
    goal_type VARCHAR(50) NOT NULL, -- 'streak', 'frequency', 'word_count', 'specific_technique'
    goal_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Target metrics
    target_value INTEGER NOT NULL,
    target_period VARCHAR(20), -- 'daily', 'weekly', 'monthly'
    target_entry_type journal_entry_type,
    
    -- Time frame
    start_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Progress tracking
    current_progress INTEGER DEFAULT 0,
    milestones_reached INTEGER DEFAULT 0,
    
    -- Rewards and motivation
    reward_description TEXT,
    reward_earned BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT chk_target_value_positive CHECK (target_value > 0),
    CONSTRAINT chk_progress_valid CHECK (current_progress >= 0),
    CONSTRAINT chk_goal_dates CHECK (end_date IS NULL OR start_date <= end_date)
);

-- CBT thought records (detailed structure)
CREATE TABLE cbt_thought_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    journal_entry_id UUID REFERENCES journal_entries(entry_id),
    
    -- Situation
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    situation TEXT NOT NULL,
    context_details TEXT,
    
    -- Emotions
    emotions JSONB NOT NULL, -- [{"emotion": "anxious", "intensity": 8}, {"emotion": "sad", "intensity": 6}]
    physical_sensations TEXT,
    
    -- Thoughts
    automatic_thoughts TEXT NOT NULL,
    images_or_memories TEXT,
    
    -- Cognitive distortions
    distortions TEXT[], -- ['catastrophizing', 'all_or_nothing', 'mind_reading']
    distortion_analysis TEXT,
    
    -- Evidence examination
    evidence_for_thought TEXT,
    evidence_against_thought TEXT,
    
    -- Balanced perspective
    balanced_thought TEXT NOT NULL,
    alternative_perspectives TEXT[],
    
    -- Outcome
    emotions_after JSONB, -- [{"emotion": "anxious", "intensity": 4}, {"emotion": "hopeful", "intensity": 6}]
    behavioral_response TEXT,
    helpful_actions TEXT[],
    
    -- Learning and insights
    what_learned TEXT,
    future_strategy TEXT,
    
    -- Therapist review
    therapist_reviewed BOOLEAN DEFAULT FALSE,
    therapist_feedback TEXT,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Gratitude entries (detailed structure)
CREATE TABLE gratitude_entries (
    gratitude_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    journal_entry_id UUID REFERENCES journal_entries(entry_id),
    entry_date DATE DEFAULT CURRENT_DATE,
    
    -- Gratitude items
    gratitude_items JSONB NOT NULL, -- [{"item": "good health", "reason": "allows me to exercise", "category": "health"}]
    
    -- Reflection
    why_grateful TEXT,
    how_it_affects_me TEXT,
    sharing_plan TEXT, -- how user plans to express gratitude
    
    -- Emotional impact
    mood_before intensity_scale,
    mood_after intensity_scale,
    gratitude_intensity intensity_scale,
    
    -- Categories for analysis
    categories TEXT[], -- ['health', 'relationships', 'achievements', 'nature']
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_journal_entries_user_id ON journal_entries(user_id);
CREATE INDEX idx_journal_entries_type ON journal_entries(entry_type);
CREATE INDEX idx_journal_entries_created_at ON journal_entries(created_at);
CREATE INDEX idx_journal_entries_shared ON journal_entries(shared_with_therapist);
CREATE INDEX idx_journal_prompts_category ON journal_prompts(category);
CREATE INDEX idx_journal_prompts_type ON journal_prompts(prompt_type);
CREATE INDEX idx_journal_prompts_active ON journal_prompts(is_active);
CREATE INDEX idx_user_prompt_history_user_id ON user_prompt_history(user_id);
CREATE INDEX idx_user_prompt_history_prompt_id ON user_prompt_history(prompt_id);
CREATE INDEX idx_journaling_stats_user_id ON journaling_stats(user_id);
CREATE INDEX idx_cbt_thought_records_user_id ON cbt_thought_records(user_id);
CREATE INDEX idx_cbt_thought_records_date ON cbt_thought_records(date_time);
CREATE INDEX idx_gratitude_entries_user_id ON gratitude_entries(user_id);
CREATE INDEX idx_gratitude_entries_date ON gratitude_entries(entry_date);

-- Full-text search indexes
CREATE INDEX idx_journal_entries_content_fts ON journal_entries USING gin(to_tsvector('english', content));
CREATE INDEX idx_journal_entries_title_fts ON journal_entries USING gin(to_tsvector('english', title));

-- Triggers for updated_at
CREATE TRIGGER update_journal_entries_updated_at BEFORE UPDATE ON journal_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_journal_prompts_updated_at BEFORE UPDATE ON journal_prompts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_journaling_goals_updated_at BEFORE UPDATE ON journaling_goals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cbt_thought_records_updated_at BEFORE UPDATE ON cbt_thought_records
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
