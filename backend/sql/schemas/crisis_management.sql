-- Crisis Detection and Management Schema
-- Handles crisis detection, escalation protocols, and emergency response

-- Crisis severity levels
CREATE TYPE crisis_severity AS ENUM (
    'low',           -- Mild distress, monitor
    'moderate',      -- Elevated concern, check-in
    'high',          -- Immediate attention needed
    'critical',      -- Emergency response required
    'imminent'       -- Life-threatening emergency
);

-- Crisis types
CREATE TYPE crisis_type AS ENUM (
    'suicidal_ideation',
    'self_harm',
    'substance_abuse',
    'psychotic_episode',
    'panic_attack',
    'severe_depression',
    'domestic_violence',
    'eating_disorder',
    'trauma_response',
    'other'
);

-- Escalation status
CREATE TYPE escalation_status AS ENUM (
    'detected',
    'under_review',
    'escalated',
    'contacted_user',
    'emergency_services_called',
    'resolved',
    'false_positive'
);

-- Crisis keywords and patterns library
CREATE TABLE crisis_keywords (
    keyword_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword_phrase TEXT NOT NULL,
    crisis_type crisis_type NOT NULL,
    severity_weight DECIMAL(3,2) NOT NULL, -- 0.1 to 1.0
    context_required BOOLEAN DEFAULT FALSE,
    
    -- Pattern matching
    is_regex BOOLEAN DEFAULT FALSE,
    case_sensitive BOOLEAN DEFAULT FALSE,
    word_boundary_required BOOLEAN DEFAULT TRUE,
    
    -- Effectiveness tracking
    true_positive_count INTEGER DEFAULT 0,
    false_positive_count INTEGER DEFAULT 0,
    last_triggered TIMESTAMP WITH TIME ZONE,
    
    -- Management
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(user_id),
    reviewed_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_severity_weight_range CHECK (severity_weight > 0 AND severity_weight <= 1)
);

-- Crisis detection events
CREATE TABLE crisis_detections (
    detection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Detection source
    source_type VARCHAR(50) NOT NULL, -- 'chat', 'journal', 'mood_entry', 'direct_report'
    source_id UUID, -- ID of the source content (journal_entry_id, chat_message_id, etc.)
    content_excerpt TEXT NOT NULL,
    full_content TEXT,
    
    -- Crisis assessment
    crisis_type crisis_type NOT NULL,
    severity_level crisis_severity NOT NULL,
    confidence_score DECIMAL(3,2) NOT NULL, -- AI confidence 0-1
    
    -- Detected keywords/patterns
    triggered_keywords TEXT[],
    keyword_scores JSONB, -- {"suicidal": 0.9, "hopeless": 0.7}
    
    -- Context analysis
    sentiment_score DECIMAL(3,2), -- -1 to 1
    emotion_intensity DECIMAL(3,2), -- 0 to 1
    temporal_indicators TEXT[], -- 'immediate', 'planning', 'historical'
    contextual_factors TEXT[], -- 'isolation', 'recent_loss', 'substance_use'
    
    -- Detection metadata
    detection_algorithm VARCHAR(50),
    algorithm_version VARCHAR(20),
    processing_time_ms INTEGER,
    
    -- Review and validation
    human_reviewed BOOLEAN DEFAULT FALSE,
    human_assessment crisis_severity,
    reviewer_id UUID REFERENCES users(user_id),
    review_notes TEXT,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    
    -- False positive tracking
    is_false_positive BOOLEAN,
    false_positive_reason TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_confidence_score_range CHECK (confidence_score >= 0 AND confidence_score <= 1),
    CONSTRAINT chk_sentiment_range CHECK (sentiment_score IS NULL OR (sentiment_score >= -1 AND sentiment_score <= 1)),
    CONSTRAINT chk_emotion_intensity_range CHECK (emotion_intensity IS NULL OR (emotion_intensity >= 0 AND emotion_intensity <= 1))
);

-- Crisis escalation and response tracking
CREATE TABLE crisis_escalations (
    escalation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    detection_id UUID NOT NULL REFERENCES crisis_detections(detection_id),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Escalation details
    escalation_level INTEGER NOT NULL, -- 1, 2, 3, etc.
    escalation_status escalation_status NOT NULL DEFAULT 'detected',
    escalation_reason TEXT NOT NULL,
    
    -- Response actions
    automatic_response TEXT, -- Auto-generated message to user
    hotline_info_provided BOOLEAN DEFAULT FALSE,
    emergency_contacts_notified BOOLEAN DEFAULT FALSE,
    emergency_services_contacted BOOLEAN DEFAULT FALSE,
    therapist_notified BOOLEAN DEFAULT FALSE,
    
    -- Contact attempts
    contact_method VARCHAR(50), -- 'app_notification', 'sms', 'email', 'phone_call'
    contact_successful BOOLEAN,
    contact_response TEXT,
    contact_attempts INTEGER DEFAULT 0,
    
    -- Human intervention
    assigned_to UUID REFERENCES users(user_id), -- Crisis counselor/support staff
    assigned_at TIMESTAMP WITH TIME ZONE,
    first_response_time TIMESTAMP WITH TIME ZONE,
    resolution_time TIMESTAMP WITH TIME ZONE,
    
    -- Outcome tracking
    user_safe BOOLEAN,
    follow_up_required BOOLEAN DEFAULT TRUE,
    follow_up_scheduled TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    
    -- Performance metrics
    response_time_minutes INTEGER, -- Time from detection to first response
    resolution_time_minutes INTEGER, -- Time from detection to resolution
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT chk_escalation_level_positive CHECK (escalation_level > 0),
    CONSTRAINT chk_contact_attempts_positive CHECK (contact_attempts >= 0)
);

-- Crisis hotlines and resources
CREATE TABLE crisis_resources (
    resource_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_name VARCHAR(200) NOT NULL,
    resource_type VARCHAR(50) NOT NULL, -- 'hotline', 'text_line', 'chat', 'website', 'app'
    
    -- Contact information
    phone_number VARCHAR(20),
    text_number VARCHAR(20),
    website_url VARCHAR(500),
    email VARCHAR(255),
    
    -- Availability
    available_24_7 BOOLEAN DEFAULT FALSE,
    available_hours TEXT, -- "Monday-Friday 9AM-5PM EST"
    timezone VARCHAR(50),
    
    -- Targeting
    target_demographics TEXT[], -- 'teens', 'veterans', 'lgbtq', 'elderly'
    languages_supported TEXT[] DEFAULT ARRAY['en'],
    geographic_coverage TEXT[], -- 'US', 'CA', 'UK', etc.
    
    -- Specializations
    crisis_types crisis_type[],
    specialized_for TEXT[], -- 'suicide', 'domestic_violence', 'substance_abuse'
    
    -- Quality and verification
    verified BOOLEAN DEFAULT FALSE,
    last_verified TIMESTAMP WITH TIME ZONE,
    effectiveness_rating DECIMAL(3,2), -- User feedback rating
    usage_count INTEGER DEFAULT 0,
    
    -- Management
    is_active BOOLEAN DEFAULT TRUE,
    display_priority INTEGER DEFAULT 1,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User crisis history and follow-up
CREATE TABLE user_crisis_history (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    escalation_id UUID REFERENCES crisis_escalations(escalation_id),
    
    -- Crisis episode summary
    episode_date DATE NOT NULL,
    crisis_type crisis_type NOT NULL,
    severity_level crisis_severity NOT NULL,
    duration_hours INTEGER,
    
    -- Contributing factors
    triggers TEXT[],
    warning_signs TEXT[],
    life_stressors TEXT[],
    protective_factors TEXT[],
    
    -- Response and outcome
    interventions_used TEXT[],
    resources_accessed TEXT[],
    support_people_contacted TEXT[],
    professional_help_sought BOOLEAN DEFAULT FALSE,
    
    -- Follow-up care
    safety_plan_updated BOOLEAN DEFAULT FALSE,
    therapy_appointment_scheduled BOOLEAN DEFAULT FALSE,
    medication_reviewed BOOLEAN DEFAULT FALSE,
    support_system_activated BOOLEAN DEFAULT FALSE,
    
    -- Learning and prevention
    what_helped TEXT,
    what_didnt_help TEXT,
    lessons_learned TEXT,
    prevention_strategies TEXT[],
    
    -- Recovery tracking
    recovery_status VARCHAR(50), -- 'stable', 'improving', 'ongoing_concern'
    next_check_in TIMESTAMP WITH TIME ZONE,
    
    -- Privacy and sharing
    shared_with_therapist BOOLEAN DEFAULT FALSE,
    consent_for_follow_up BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_duration_positive CHECK (duration_hours IS NULL OR duration_hours >= 0)
);

-- Safety plans
CREATE TABLE safety_plans (
    plan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Plan identification
    plan_name VARCHAR(100) DEFAULT 'My Safety Plan',
    version_number INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Warning signs recognition
    warning_signs TEXT[] NOT NULL,
    personal_triggers TEXT[],
    
    -- Coping strategies
    internal_coping_strategies TEXT[], -- Self-help techniques
    social_settings_distractions TEXT[], -- Safe places, activities
    
    -- Support network
    support_people JSONB, -- [{"name": "John", "phone": "123-456-7890", "relationship": "brother"}]
    professional_contacts JSONB, -- Therapists, doctors, etc.
    
    -- Crisis contacts
    crisis_hotlines TEXT[],
    emergency_contacts JSONB,
    
    -- Environment safety
    means_restriction_steps TEXT[], -- Removing/securing harmful items
    safe_environment_plan TEXT,
    
    -- Reasons for living
    reasons_for_living TEXT[] NOT NULL,
    future_goals TEXT[],
    important_relationships TEXT[],
    
    -- Plan activation
    when_to_use TEXT,
    activation_triggers TEXT[],
    
    -- Collaboration
    created_with_therapist BOOLEAN DEFAULT FALSE,
    therapist_id UUID REFERENCES users(user_id),
    family_involved BOOLEAN DEFAULT FALSE,
    
    -- Review and updates
    last_reviewed TIMESTAMP WITH TIME ZONE,
    next_review_due TIMESTAMP WITH TIME ZONE,
    review_frequency_days INTEGER DEFAULT 90,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_version_positive CHECK (version_number > 0),
    CONSTRAINT chk_review_frequency_positive CHECK (review_frequency_days > 0)
);

-- Crisis analytics and reporting
CREATE TABLE crisis_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Time period
    analysis_period_start DATE NOT NULL,
    analysis_period_end DATE NOT NULL,
    
    -- Detection metrics
    total_detections INTEGER DEFAULT 0,
    true_positives INTEGER DEFAULT 0,
    false_positives INTEGER DEFAULT 0,
    false_negatives INTEGER DEFAULT 0, -- Manually identified
    
    -- Response metrics
    average_response_time_minutes DECIMAL(8,2),
    successful_contacts INTEGER DEFAULT 0,
    emergency_services_called INTEGER DEFAULT 0,
    users_helped INTEGER DEFAULT 0,
    
    -- Outcome metrics
    crisis_resolved INTEGER DEFAULT 0,
    ongoing_support_cases INTEGER DEFAULT 0,
    false_alarms INTEGER DEFAULT 0,
    
    -- Algorithm performance
    precision_score DECIMAL(5,4),
    recall_score DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    algorithm_version VARCHAR(20),
    
    -- Insights
    common_triggers TEXT[],
    peak_crisis_times JSONB, -- Hour/day patterns
    demographic_patterns JSONB,
    seasonal_trends JSONB,
    
    -- Generated by
    generated_by VARCHAR(50) DEFAULT 'system',
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_analysis_period CHECK (analysis_period_start <= analysis_period_end),
    CONSTRAINT chk_counts_positive CHECK (
        total_detections >= 0 AND 
        true_positives >= 0 AND 
        false_positives >= 0 AND 
        false_negatives >= 0
    ),
    CONSTRAINT chk_scores_range CHECK (
        (precision_score IS NULL OR (precision_score >= 0 AND precision_score <= 1)) AND
        (recall_score IS NULL OR (recall_score >= 0 AND recall_score <= 1)) AND
        (f1_score IS NULL OR (f1_score >= 0 AND f1_score <= 1))
    )
);

-- Indexes for performance
CREATE INDEX idx_crisis_keywords_type ON crisis_keywords(crisis_type);
CREATE INDEX idx_crisis_keywords_active ON crisis_keywords(is_active);
CREATE INDEX idx_crisis_detections_user_id ON crisis_detections(user_id);
CREATE INDEX idx_crisis_detections_severity ON crisis_detections(severity_level);
CREATE INDEX idx_crisis_detections_created_at ON crisis_detections(created_at);
CREATE INDEX idx_crisis_detections_reviewed ON crisis_detections(human_reviewed);
CREATE INDEX idx_crisis_escalations_user_id ON crisis_escalations(user_id);
CREATE INDEX idx_crisis_escalations_status ON crisis_escalations(escalation_status);
CREATE INDEX idx_crisis_escalations_assigned ON crisis_escalations(assigned_to);
CREATE INDEX idx_crisis_resources_type ON crisis_resources(resource_type);
CREATE INDEX idx_crisis_resources_active ON crisis_resources(is_active);
CREATE INDEX idx_user_crisis_history_user_id ON user_crisis_history(user_id);
CREATE INDEX idx_user_crisis_history_date ON user_crisis_history(episode_date);
CREATE INDEX idx_safety_plans_user_id ON safety_plans(user_id);
CREATE INDEX idx_safety_plans_active ON safety_plans(is_active);

-- Full-text search for crisis content
CREATE INDEX idx_crisis_detections_content_fts ON crisis_detections USING gin(to_tsvector('english', content_excerpt));

-- Triggers for updated_at
CREATE TRIGGER update_crisis_keywords_updated_at BEFORE UPDATE ON crisis_keywords
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_crisis_escalations_updated_at BEFORE UPDATE ON crisis_escalations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_crisis_resources_updated_at BEFORE UPDATE ON crisis_resources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_crisis_history_updated_at BEFORE UPDATE ON user_crisis_history
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_safety_plans_updated_at BEFORE UPDATE ON safety_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
