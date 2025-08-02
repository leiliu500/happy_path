-- Assessment and Screening Tools Schema
-- Handles wellness questionnaires, self-assessment tools, and progress tracking
-- 
-- IMPORTANT: These tools are for wellness tracking and self-awareness purposes.
-- They do not constitute medical diagnosis and should not replace professional
-- medical evaluation. Users should consult licensed healthcare providers for
-- medical diagnosis and treatment decisions.

-- Assessment types for different mental health conditions
CREATE TYPE assessment_type AS ENUM (
    'phq9',              -- Patient Health Questionnaire-9 (Depression)
    'gad7',              -- Generalized Anxiety Disorder 7-item
    'dass21',            -- Depression, Anxiety and Stress Scale
    'beck_depression',   -- Beck Depression Inventory
    'beck_anxiety',      -- Beck Anxiety Inventory
    'ptsd_checklist',    -- PTSD Checklist for DSM-5
    'yale_brown_ocd',    -- Yale-Brown Obsessive Compulsive Scale
    'edinburgh_postnatal', -- Edinburgh Postnatal Depression Scale
    'audit',             -- Alcohol Use Disorders Identification Test
    'cage',              -- CAGE Questionnaire for alcohol screening
    'mdq',               -- Mood Disorder Questionnaire
    'ham_d',             -- Hamilton Depression Rating Scale
    'mini_mental',       -- Mini-Mental State Examination
    'sf36',              -- Short Form Health Survey
    'whodas',            -- WHO Disability Assessment Schedule
    'custom'             -- Custom assessment tools
);

-- Assessment status tracking
CREATE TYPE assessment_status AS ENUM (
    'not_started',
    'in_progress',
    'completed',
    'abandoned',
    'invalidated',
    'under_review'
);

-- Assessment urgency levels
CREATE TYPE assessment_urgency AS ENUM (
    'routine',
    'priority',
    'urgent',
    'critical'
);

-- Standardized assessment templates
CREATE TABLE assessment_templates (
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_type assessment_type NOT NULL,
    template_name VARCHAR(200) NOT NULL,
    version VARCHAR(20) NOT NULL,
    
    -- Assessment metadata
    description TEXT,
    target_population VARCHAR(100), -- 'adults', 'adolescents', 'elderly', 'postpartum'
    estimated_duration_minutes INTEGER,
    
    -- Clinical information
    measures TEXT[], -- What the assessment measures
    scoring_method TEXT NOT NULL,
    interpretation_guidelines TEXT,
    cutoff_scores JSONB, -- {"minimal": [0,4], "mild": [5,9], "moderate": [10,14]}
    
    -- Questionnaire structure
    total_questions INTEGER NOT NULL,
    question_format VARCHAR(50), -- 'likert', 'multiple_choice', 'yes_no', 'mixed'
    questions JSONB NOT NULL, -- Full question structure with scoring
    
    -- Validation and reliability
    validity_studies TEXT[],
    reliability_coefficient DECIMAL(4,3), -- Cronbach's alpha
    sensitivity DECIMAL(4,3),
    specificity DECIMAL(4,3),
    
    -- Usage and administration
    requires_training BOOLEAN DEFAULT FALSE,
    self_administered BOOLEAN DEFAULT TRUE,
    clinician_administered BOOLEAN DEFAULT FALSE,
    frequency_recommendation VARCHAR(100), -- 'baseline_only', 'weekly', 'monthly', 'as_needed'
    
    -- Regulatory and compliance
    copyright_info TEXT,
    license_required BOOLEAN DEFAULT FALSE,
    regulatory_approval TEXT[],
    
    -- Management
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(user_id),
    reviewed_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_duration_positive CHECK (estimated_duration_minutes > 0),
    CONSTRAINT chk_questions_positive CHECK (total_questions > 0),
    CONSTRAINT chk_reliability_range CHECK (reliability_coefficient IS NULL OR (reliability_coefficient >= 0 AND reliability_coefficient <= 1))
);

-- Individual assessment instances
CREATE TABLE assessments (
    assessment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID NOT NULL REFERENCES assessment_templates(template_id),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Assessment context
    administered_by UUID REFERENCES users(user_id), -- NULL for self-administered
    assessment_reason VARCHAR(100), -- 'intake', 'progress_monitoring', 'discharge', 'crisis'
    therapeutic_context UUID, -- Reference to therapy session if applicable
    
    -- Status and timing
    status assessment_status NOT NULL DEFAULT 'not_started',
    urgency_level assessment_urgency DEFAULT 'routine',
    
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    time_taken_minutes INTEGER,
    
    -- Responses and scoring
    responses JSONB, -- {"q1": 2, "q2": 1, "q3": 3, ...}
    raw_score INTEGER,
    scaled_score DECIMAL(6,2),
    percentile_rank INTEGER,
    severity_level VARCHAR(50), -- Based on cutoff scores
    
    -- Clinical interpretation
    interpretation_summary TEXT,
    clinical_significance BOOLEAN,
    recommendations TEXT[],
    follow_up_needed BOOLEAN DEFAULT FALSE,
    
    -- Progress tracking
    previous_assessment_id UUID REFERENCES assessments(assessment_id),
    score_change DECIMAL(6,2), -- Change from previous assessment
    reliable_change_index DECIMAL(6,2), -- Statistical significance of change
    
    -- Quality assurance
    validity_checks JSONB, -- {"response_time_flags": [], "pattern_flags": []}
    data_quality_score DECIMAL(3,2), -- 0-1 scale
    requires_review BOOLEAN DEFAULT FALSE,
    reviewed_by UUID REFERENCES users(user_id),
    review_notes TEXT,
    
    -- Privacy and consent
    shared_with_therapist BOOLEAN DEFAULT FALSE,
    research_consent BOOLEAN DEFAULT FALSE,
    data_retention_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_time_taken_positive CHECK (time_taken_minutes IS NULL OR time_taken_minutes > 0),
    CONSTRAINT chk_percentile_range CHECK (percentile_rank IS NULL OR (percentile_rank >= 1 AND percentile_rank <= 100)),
    CONSTRAINT chk_data_quality_range CHECK (data_quality_score IS NULL OR (data_quality_score >= 0 AND data_quality_score <= 1))
);

-- Assessment scheduling and reminders
CREATE TABLE assessment_schedules (
    schedule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    template_id UUID NOT NULL REFERENCES assessment_templates(template_id),
    
    -- Scheduling parameters
    schedule_type VARCHAR(50) NOT NULL, -- 'one_time', 'recurring', 'conditional'
    frequency_days INTEGER, -- For recurring assessments
    next_due_date DATE NOT NULL,
    
    -- Conditions for conditional scheduling
    trigger_conditions JSONB, -- {"mood_threshold": 3, "crisis_detected": true}
    
    -- Status and management
    is_active BOOLEAN DEFAULT TRUE,
    last_completed_date DATE,
    completion_count INTEGER DEFAULT 0,
    missed_count INTEGER DEFAULT 0,
    
    -- Reminders
    reminder_enabled BOOLEAN DEFAULT TRUE,
    reminder_days_before INTEGER DEFAULT 1,
    reminder_methods TEXT[] DEFAULT '{"email", "push_notification"}',
    
    -- Clinical oversight
    ordered_by UUID REFERENCES users(user_id), -- Therapist who ordered the assessment
    priority_level assessment_urgency DEFAULT 'routine',
    special_instructions TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_frequency_positive CHECK (frequency_days IS NULL OR frequency_days > 0),
    CONSTRAINT chk_reminder_days_positive CHECK (reminder_days_before >= 0)
);

-- Assessment results history and trends
CREATE TABLE assessment_trends (
    trend_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    assessment_type assessment_type NOT NULL,
    
    -- Trend analysis period
    analysis_start_date DATE NOT NULL,
    analysis_end_date DATE NOT NULL,
    assessment_count INTEGER NOT NULL,
    
    -- Trend metrics
    baseline_score DECIMAL(6,2),
    latest_score DECIMAL(6,2),
    average_score DECIMAL(6,2),
    score_variance DECIMAL(8,4),
    
    -- Trend direction and significance
    trend_direction VARCHAR(20), -- 'improving', 'declining', 'stable', 'volatile'
    trend_strength DECIMAL(4,3), -- Correlation coefficient
    clinical_significance BOOLEAN DEFAULT FALSE,
    
    -- Change metrics
    total_change DECIMAL(6,2),
    percent_change DECIMAL(6,2),
    rate_of_change DECIMAL(8,4), -- Points per day
    
    -- Statistical analysis
    regression_slope DECIMAL(8,4),
    r_squared DECIMAL(4,3),
    confidence_interval JSONB, -- {"lower": x, "upper": y}
    
    -- Clinical interpretation
    interpretation TEXT,
    treatment_response VARCHAR(50), -- 'excellent', 'good', 'partial', 'poor', 'deterioration'
    recommendations TEXT[],
    
    -- Analysis metadata
    calculation_method VARCHAR(100),
    data_quality_indicators JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_assessment_count_positive CHECK (assessment_count > 0),
    CONSTRAINT chk_trend_strength_range CHECK (trend_strength IS NULL OR (trend_strength >= -1 AND trend_strength <= 1)),
    CONSTRAINT chk_r_squared_range CHECK (r_squared IS NULL OR (r_squared >= 0 AND r_squared <= 1))
);

-- Composite assessment reports
CREATE TABLE assessment_reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Report metadata
    report_type VARCHAR(50) NOT NULL, -- 'intake', 'progress', 'discharge', 'comprehensive'
    report_title VARCHAR(200) NOT NULL,
    report_period_start DATE,
    report_period_end DATE,
    
    -- Included assessments
    assessment_ids UUID[] NOT NULL,
    primary_assessments TEXT[], -- Which assessments are highlighted
    
    -- Clinical summary
    overall_severity VARCHAR(50),
    primary_diagnoses TEXT[],
    comorbidities TEXT[],
    risk_factors TEXT[],
    protective_factors TEXT[],
    
    -- Progress summary
    areas_of_improvement TEXT[],
    areas_of_concern TEXT[],
    treatment_response VARCHAR(50),
    
    -- Recommendations
    clinical_recommendations TEXT[],
    medication_recommendations TEXT[],
    therapy_modifications TEXT[],
    lifestyle_recommendations TEXT[],
    
    -- Follow-up planning
    recommended_assessments TEXT[],
    reassessment_timeline VARCHAR(100),
    monitoring_frequency VARCHAR(50),
    
    -- Report generation
    generated_by UUID REFERENCES users(user_id),
    auto_generated BOOLEAN DEFAULT FALSE,
    template_used VARCHAR(100),
    
    -- Sharing and distribution
    shared_with_therapist BOOLEAN DEFAULT FALSE,
    shared_with_psychiatrist BOOLEAN DEFAULT FALSE,
    patient_summary_provided BOOLEAN DEFAULT FALSE,
    
    -- Document management
    report_version INTEGER DEFAULT 1,
    is_final BOOLEAN DEFAULT FALSE,
    approved_by UUID REFERENCES users(user_id),
    approval_date TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_assessments_user_id ON assessments(user_id);
CREATE INDEX idx_assessments_template_id ON assessments(template_id);
CREATE INDEX idx_assessments_status ON assessments(status);
CREATE INDEX idx_assessments_completed_at ON assessments(completed_at);
CREATE INDEX idx_assessment_schedules_user_id ON assessment_schedules(user_id);
CREATE INDEX idx_assessment_schedules_next_due ON assessment_schedules(next_due_date) WHERE is_active = TRUE;
CREATE INDEX idx_assessment_trends_user_type ON assessment_trends(user_id, assessment_type);

-- Row Level Security
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_trends ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_reports ENABLE ROW LEVEL SECURITY;

-- Triggers for automated timestamp updates
CREATE TRIGGER update_assessment_templates_updated_at
    BEFORE UPDATE ON assessment_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assessments_updated_at
    BEFORE UPDATE ON assessments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assessment_schedules_updated_at
    BEFORE UPDATE ON assessment_schedules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assessment_reports_updated_at
    BEFORE UPDATE ON assessment_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE assessment_templates IS 'Standardized mental health assessment questionnaires and clinical tools';
COMMENT ON TABLE assessments IS 'Individual instances of completed assessments with scores and interpretations';
COMMENT ON TABLE assessment_schedules IS 'Scheduling and reminder system for recurring assessments';
COMMENT ON TABLE assessment_trends IS 'Longitudinal analysis of assessment scores and clinical progress';
COMMENT ON TABLE assessment_reports IS 'Comprehensive clinical reports combining multiple assessments';
