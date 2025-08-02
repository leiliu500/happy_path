-- Conversational Agent Schema
-- Handles chat sessions, AI interactions, conversation analysis, and therapeutic guidance

-- Conversation types
CREATE TYPE conversation_type AS ENUM (
    'casual_chat',
    'mood_check_in',
    'crisis_support',
    'cbt_session',
    'mindfulness_guidance',
    'goal_setting',
    'reflection',
    'psychoeducation',
    'therapy_homework',
    'medication_reminder'
);

-- Message types
CREATE TYPE message_type AS ENUM (
    'user_message',
    'ai_response',
    'system_notification',
    'prompt_suggestion',
    'resource_share',
    'crisis_intervention',
    'follow_up_question'
);

-- AI response quality
CREATE TYPE response_quality AS ENUM (
    'excellent',
    'good',
    'acceptable',
    'poor',
    'harmful'
);

-- Therapeutic techniques used
CREATE TYPE therapeutic_technique AS ENUM (
    'active_listening',
    'cognitive_restructuring',
    'behavioral_activation',
    'mindfulness',
    'grounding',
    'validation',
    'motivational_interviewing',
    'psychoeducation',
    'problem_solving',
    'exposure_therapy'
);

-- Chat sessions
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Session metadata
    session_title VARCHAR(200),
    conversation_type conversation_type NOT NULL DEFAULT 'casual_chat',
    session_purpose TEXT,
    
    -- Session state
    is_active BOOLEAN DEFAULT TRUE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Session context
    user_mood_start INTEGER, -- 1-10 scale
    user_mood_end INTEGER, -- 1-10 scale
    user_goals TEXT[],
    session_objectives TEXT[],
    
    -- AI agent information
    ai_agent_version VARCHAR(50),
    ai_model_used VARCHAR(100),
    personality_profile VARCHAR(50), -- 'empathetic', 'professional', 'casual'
    
    -- Session metrics
    total_messages INTEGER DEFAULT 0,
    user_messages INTEGER DEFAULT 0,
    ai_messages INTEGER DEFAULT 0,
    session_duration_minutes INTEGER,
    
    -- Therapeutic assessment
    therapeutic_techniques_used therapeutic_technique[],
    session_effectiveness INTEGER, -- 1-5 user rating
    crisis_detected BOOLEAN DEFAULT FALSE,
    escalation_needed BOOLEAN DEFAULT FALSE,
    
    -- Follow-up
    follow_up_scheduled BOOLEAN DEFAULT FALSE,
    follow_up_notes TEXT,
    homework_assigned TEXT[],
    
    -- Privacy and sharing
    shared_with_therapist BOOLEAN DEFAULT FALSE,
    consent_for_analysis BOOLEAN DEFAULT TRUE,
    
    -- Analysis results
    sentiment_trend JSONB, -- Track sentiment over conversation
    emotion_analysis JSONB,
    key_topics TEXT[],
    insights_generated TEXT[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_mood_range CHECK (
        (user_mood_start IS NULL OR (user_mood_start >= 1 AND user_mood_start <= 10)) AND
        (user_mood_end IS NULL OR (user_mood_end >= 1 AND user_mood_end <= 10))
    ),
    CONSTRAINT chk_effectiveness_range CHECK (
        session_effectiveness IS NULL OR (session_effectiveness >= 1 AND session_effectiveness <= 5)
    ),
    CONSTRAINT chk_message_counts CHECK (
        total_messages >= 0 AND 
        user_messages >= 0 AND 
        ai_messages >= 0 AND
        total_messages >= (user_messages + ai_messages)
    )
);

-- Individual chat messages
CREATE TABLE chat_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Message content
    message_type message_type NOT NULL,
    content TEXT NOT NULL,
    content_length INTEGER DEFAULT 0,
    
    -- Message metadata
    sequence_number INTEGER NOT NULL, -- Order within session
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMP WITH TIME ZONE,
    
    -- AI response metadata (for AI messages)
    prompt_used TEXT,
    model_version VARCHAR(50),
    response_time_ms INTEGER,
    temperature DECIMAL(3,2), -- AI creativity parameter
    tokens_used INTEGER,
    
    -- Content analysis
    sentiment_score DECIMAL(3,2), -- -1 to 1
    emotion_detected TEXT[],
    intent_detected VARCHAR(100),
    topics_mentioned TEXT[],
    entities_extracted JSONB, -- Named entities, dates, etc.
    
    -- Crisis detection
    crisis_keywords_detected TEXT[],
    crisis_score DECIMAL(3,2), -- 0 to 1
    requires_escalation BOOLEAN DEFAULT FALSE,
    
    -- Therapeutic context
    therapeutic_technique therapeutic_technique,
    cbt_element VARCHAR(100), -- Specific CBT technique used
    intervention_type VARCHAR(100),
    
    -- Quality and feedback
    user_reaction VARCHAR(50), -- 'helpful', 'not_helpful', 'harmful'
    quality_score DECIMAL(3,2), -- AI-assessed quality 0-1
    human_reviewed BOOLEAN DEFAULT FALSE,
    reviewer_rating response_quality,
    
    -- Context and references
    references_previous_messages UUID[], -- IDs of referenced messages
    context_used JSONB, -- Context from user profile, mood, etc.
    
    -- Personalization
    personalization_factors JSONB, -- User preferences, history, etc.
    adaptation_notes TEXT,
    
    CONSTRAINT chk_sentiment_range CHECK (sentiment_score IS NULL OR (sentiment_score >= -1 AND sentiment_score <= 1)),
    CONSTRAINT chk_crisis_score_range CHECK (crisis_score IS NULL OR (crisis_score >= 0 AND crisis_score <= 1)),
    CONSTRAINT chk_quality_score_range CHECK (quality_score IS NULL OR (quality_score >= 0 AND quality_score <= 1)),
    CONSTRAINT chk_temperature_range CHECK (temperature IS NULL OR (temperature >= 0 AND temperature <= 2)),
    CONSTRAINT chk_content_length_positive CHECK (content_length >= 0)
);

-- AI agent configurations and personalities
CREATE TABLE ai_agent_configs (
    config_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    
    -- Personality settings
    personality_type VARCHAR(50) NOT NULL, -- 'empathetic', 'professional', 'casual'
    empathy_level DECIMAL(3,2) DEFAULT 0.8, -- 0 to 1
    formality_level DECIMAL(3,2) DEFAULT 0.5, -- 0 to 1
    enthusiasm_level DECIMAL(3,2) DEFAULT 0.6, -- 0 to 1
    
    -- Response behavior
    response_length_preference VARCHAR(20) DEFAULT 'medium', -- 'short', 'medium', 'long'
    question_frequency DECIMAL(3,2) DEFAULT 0.3, -- How often to ask questions
    validation_frequency DECIMAL(3,2) DEFAULT 0.7, -- How often to validate feelings
    
    -- Therapeutic approach
    primary_therapeutic_approach VARCHAR(50) DEFAULT 'cbt', -- 'cbt', 'dbt', 'humanistic'
    intervention_aggressiveness DECIMAL(3,2) DEFAULT 0.5, -- 0 conservative, 1 aggressive
    crisis_sensitivity DECIMAL(3,2) DEFAULT 0.9, -- Crisis detection threshold
    
    -- Content preferences
    use_metaphors BOOLEAN DEFAULT TRUE,
    use_humor BOOLEAN DEFAULT FALSE,
    use_personal_examples BOOLEAN DEFAULT FALSE,
    educational_content_frequency DECIMAL(3,2) DEFAULT 0.2,
    
    -- Model parameters
    default_temperature DECIMAL(3,2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,
    system_prompt TEXT NOT NULL,
    
    -- Targeting
    target_age_groups TEXT[], -- ['teens', 'adults', 'seniors']
    target_conditions TEXT[], -- ['anxiety', 'depression', 'ptsd']
    
    -- Quality control
    is_active BOOLEAN DEFAULT TRUE,
    requires_supervision BOOLEAN DEFAULT FALSE,
    effectiveness_rating DECIMAL(3,2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_personality_levels CHECK (
        empathy_level >= 0 AND empathy_level <= 1 AND
        formality_level >= 0 AND formality_level <= 1 AND
        enthusiasm_level >= 0 AND enthusiasm_level <= 1
    ),
    CONSTRAINT chk_behavior_frequencies CHECK (
        question_frequency >= 0 AND question_frequency <= 1 AND
        validation_frequency >= 0 AND validation_frequency <= 1 AND
        educational_content_frequency >= 0 AND educational_content_frequency <= 1
    )
);

-- Conversation templates and prompts
CREATE TABLE conversation_prompts (
    prompt_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_name VARCHAR(100) NOT NULL,
    conversation_type conversation_type NOT NULL,
    
    -- Prompt content
    system_prompt TEXT NOT NULL,
    user_prompt_template TEXT,
    follow_up_prompts TEXT[],
    
    -- Therapeutic context
    therapeutic_goal VARCHAR(100),
    therapeutic_technique therapeutic_technique,
    target_outcome TEXT,
    
    -- Usage conditions
    trigger_conditions JSONB, -- When to use this prompt
    user_mood_range INTEGER[], -- [3, 7] for moderate moods
    conversation_stage VARCHAR(50), -- 'opening', 'middle', 'closing'
    
    -- Effectiveness tracking
    usage_count INTEGER DEFAULT 0,
    success_rate DECIMAL(3,2),
    user_satisfaction_avg DECIMAL(3,2),
    
    -- Content management
    is_active BOOLEAN DEFAULT TRUE,
    requires_review BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES users(user_id),
    approved_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User conversation preferences
CREATE TABLE user_conversation_preferences (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- AI personality preferences
    preferred_personality VARCHAR(50), -- 'empathetic', 'professional', 'casual'
    preferred_formality DECIMAL(3,2) DEFAULT 0.5,
    preferred_response_length VARCHAR(20) DEFAULT 'medium',
    
    -- Communication preferences
    likes_questions BOOLEAN DEFAULT TRUE,
    likes_validation BOOLEAN DEFAULT TRUE,
    likes_educational_content BOOLEAN DEFAULT TRUE,
    likes_metaphors BOOLEAN DEFAULT TRUE,
    likes_humor BOOLEAN DEFAULT FALSE,
    
    -- Therapeutic preferences
    preferred_techniques therapeutic_technique[],
    avoids_techniques therapeutic_technique[],
    
    -- Topics and boundaries
    comfortable_topics TEXT[],
    uncomfortable_topics TEXT[],
    trigger_words TEXT[],
    
    -- Interaction style
    prefers_short_sessions BOOLEAN DEFAULT FALSE,
    max_session_length_minutes INTEGER DEFAULT 60,
    reminder_frequency_hours INTEGER DEFAULT 24,
    
    -- Privacy preferences
    allows_session_recording BOOLEAN DEFAULT TRUE,
    allows_ai_learning BOOLEAN DEFAULT TRUE,
    shares_anonymized_data BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_formality_range CHECK (preferred_formality >= 0 AND preferred_formality <= 1),
    CONSTRAINT chk_session_length_positive CHECK (max_session_length_minutes > 0),
    CONSTRAINT chk_reminder_frequency_positive CHECK (reminder_frequency_hours > 0)
);

-- Conversation analytics and insights
CREATE TABLE conversation_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    session_id UUID REFERENCES chat_sessions(session_id),
    
    -- Time period (for user-level analytics)
    analysis_period_start DATE,
    analysis_period_end DATE,
    
    -- Engagement metrics
    total_sessions INTEGER DEFAULT 0,
    average_session_length DECIMAL(8,2),
    total_messages INTEGER DEFAULT 0,
    words_per_message_avg DECIMAL(8,2),
    
    -- Mood and progress
    mood_improvement_sessions INTEGER DEFAULT 0,
    crisis_sessions INTEGER DEFAULT 0,
    breakthrough_moments INTEGER DEFAULT 0,
    
    -- Communication patterns
    most_discussed_topics TEXT[],
    most_used_emotions TEXT[],
    communication_style_trends JSONB,
    
    -- AI effectiveness
    helpful_responses_percentage DECIMAL(5,2),
    average_response_quality DECIMAL(3,2),
    personalization_effectiveness DECIMAL(3,2),
    
    -- Therapeutic progress
    goals_discussed INTEGER DEFAULT 0,
    goals_achieved INTEGER DEFAULT 0,
    coping_strategies_learned TEXT[],
    insights_documented TEXT[],
    
    -- Behavioral insights
    usage_patterns JSONB, -- Time of day, frequency patterns
    engagement_trends JSONB, -- Increasing/decreasing engagement
    risk_factors_identified TEXT[],
    protective_factors_identified TEXT[],
    
    -- Recommendations
    ai_recommendations TEXT[],
    suggested_interventions TEXT[],
    therapy_readiness_score DECIMAL(3,2),
    
    -- Generated metadata
    generated_by VARCHAR(50) DEFAULT 'ai_system',
    confidence_score DECIMAL(3,2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_percentage_range CHECK (helpful_responses_percentage IS NULL OR (helpful_responses_percentage >= 0 AND helpful_responses_percentage <= 100)),
    CONSTRAINT chk_quality_range CHECK (average_response_quality IS NULL OR (average_response_quality >= 0 AND average_response_quality <= 1)),
    CONSTRAINT chk_readiness_range CHECK (therapy_readiness_score IS NULL OR (therapy_readiness_score >= 0 AND therapy_readiness_score <= 1))
);

-- Indexes for performance
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_type ON chat_sessions(conversation_type);
CREATE INDEX idx_chat_sessions_active ON chat_sessions(is_active);
CREATE INDEX idx_chat_sessions_created_at ON chat_sessions(created_at);
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_type ON chat_messages(message_type);
CREATE INDEX idx_chat_messages_sequence ON chat_messages(session_id, sequence_number);
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp);
CREATE INDEX idx_chat_messages_crisis ON chat_messages(requires_escalation);
CREATE INDEX idx_ai_agent_configs_active ON ai_agent_configs(is_active);
CREATE INDEX idx_conversation_prompts_type ON conversation_prompts(conversation_type);
CREATE INDEX idx_conversation_prompts_active ON conversation_prompts(is_active);
CREATE INDEX idx_user_conversation_preferences_user_id ON user_conversation_preferences(user_id);
CREATE INDEX idx_conversation_analytics_user_id ON conversation_analytics(user_id);

-- Full-text search indexes
CREATE INDEX idx_chat_messages_content_fts ON chat_messages USING gin(to_tsvector('english', content));
CREATE INDEX idx_conversation_prompts_fts ON conversation_prompts USING gin(to_tsvector('english', system_prompt));

-- Triggers for updated_at
CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_agent_configs_updated_at BEFORE UPDATE ON ai_agent_configs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversation_prompts_updated_at BEFORE UPDATE ON conversation_prompts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_conversation_preferences_updated_at BEFORE UPDATE ON user_conversation_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
