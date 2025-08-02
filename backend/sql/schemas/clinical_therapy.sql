-- Clinical and Therapy Support Schema
-- Handles therapist-patient relationships, treatment plans, and clinical oversight

-- Therapy modalities
CREATE TYPE therapy_modality AS ENUM (
    'cbt',              -- Cognitive Behavioral Therapy
    'dbt',              -- Dialectical Behavior Therapy
    'emdr',             -- Eye Movement Desensitization and Reprocessing
    'psychodynamic',
    'humanistic',
    'gestalt',
    'family_therapy',
    'group_therapy',
    'mindfulness_based',
    'acceptance_commitment',
    'interpersonal',
    'solution_focused'
);

-- Treatment phases
CREATE TYPE treatment_phase AS ENUM (
    'assessment',
    'engagement',
    'active_treatment',
    'maintenance',
    'relapse_prevention',
    'termination',
    'follow_up'
);

-- Clinical severity
CREATE TYPE clinical_severity AS ENUM (
    'minimal',
    'mild',
    'moderate',
    'severe',
    'extreme'
);

-- Therapist-patient relationships
CREATE TABLE therapeutic_relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    therapist_id UUID NOT NULL REFERENCES users(user_id),
    patient_id UUID NOT NULL REFERENCES users(user_id),
    
    -- Relationship details
    relationship_type VARCHAR(50) DEFAULT 'primary', -- 'primary', 'consulting', 'supervision'
    start_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Treatment context
    primary_modality therapy_modality NOT NULL,
    secondary_modalities therapy_modality[],
    treatment_setting VARCHAR(50), -- 'in_person', 'telehealth', 'hybrid', 'app_assisted'
    
    -- Clinical information
    presenting_concerns TEXT[],
    diagnosis_codes TEXT[], -- ICD-10 codes
    treatment_goals TEXT[],
    contraindications TEXT[],
    
    -- Session logistics
    typical_session_length INTEGER DEFAULT 50, -- minutes
    session_frequency VARCHAR(50) DEFAULT 'weekly',
    preferred_session_times JSONB, -- Scheduling preferences
    
    -- Consent and agreements
    informed_consent_obtained BOOLEAN DEFAULT FALSE,
    app_integration_consent BOOLEAN DEFAULT FALSE,
    data_sharing_consent BOOLEAN DEFAULT FALSE,
    emergency_contact_consent BOOLEAN DEFAULT FALSE,
    
    -- Clinical notes access
    notes_access_level VARCHAR(50) DEFAULT 'summary', -- 'none', 'summary', 'full'
    patient_access_to_notes BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_different_users CHECK (therapist_id != patient_id),
    CONSTRAINT chk_session_length_positive CHECK (typical_session_length > 0),
    CONSTRAINT chk_relationship_dates CHECK (end_date IS NULL OR start_date <= end_date)
);

-- Treatment plans
CREATE TABLE treatment_plans (
    plan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    relationship_id UUID NOT NULL REFERENCES therapeutic_relationships(relationship_id),
    patient_id UUID NOT NULL REFERENCES users(user_id),
    therapist_id UUID NOT NULL REFERENCES users(user_id),
    
    -- Plan details
    plan_name VARCHAR(100) NOT NULL,
    version_number INTEGER DEFAULT 1,
    is_current BOOLEAN DEFAULT TRUE,
    
    -- Clinical assessment
    current_phase treatment_phase NOT NULL DEFAULT 'assessment',
    severity_level clinical_severity,
    risk_level VARCHAR(20), -- 'low', 'moderate', 'high'
    
    -- Goals and objectives
    long_term_goals JSONB NOT NULL, -- [{"goal": "Reduce anxiety", "target_date": "2024-06-01", "status": "active"}]
    short_term_objectives JSONB NOT NULL,
    behavioral_targets JSONB,
    
    -- Treatment approach
    primary_interventions TEXT[],
    therapeutic_techniques TEXT[],
    homework_assignments TEXT[],
    between_session_activities TEXT[],
    
    -- App integration
    app_supported_interventions TEXT[],
    digital_homework JSONB, -- App-based assignments
    mood_tracking_required BOOLEAN DEFAULT TRUE,
    journaling_assignments TEXT[],
    
    -- Crisis planning
    crisis_indicators TEXT[],
    crisis_response_plan TEXT,
    safety_plan_required BOOLEAN DEFAULT FALSE,
    
    -- Progress measurement
    outcome_measures TEXT[], -- Standardized assessment tools
    progress_indicators JSONB,
    measurement_frequency VARCHAR(50), -- 'weekly', 'biweekly', 'monthly'
    
    -- Timeline
    estimated_duration_sessions INTEGER,
    target_completion_date DATE,
    review_date DATE NOT NULL,
    
    -- Collaboration
    patient_input TEXT,
    family_involvement BOOLEAN DEFAULT FALSE,
    care_team_members JSONB, -- Other healthcare providers
    
    -- Documentation
    clinical_rationale TEXT NOT NULL,
    evidence_base TEXT,
    cultural_considerations TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_version_positive CHECK (version_number > 0),
    CONSTRAINT chk_duration_positive CHECK (estimated_duration_sessions IS NULL OR estimated_duration_sessions > 0)
);

-- Clinical sessions/appointments
CREATE TABLE clinical_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    relationship_id UUID NOT NULL REFERENCES therapeutic_relationships(relationship_id),
    patient_id UUID NOT NULL REFERENCES users(user_id),
    therapist_id UUID NOT NULL REFERENCES users(user_id),
    
    -- Session logistics
    session_type VARCHAR(50) DEFAULT 'individual', -- 'individual', 'group', 'family', 'consultation'
    session_format VARCHAR(50), -- 'in_person', 'video', 'phone', 'app_assisted'
    scheduled_start TIMESTAMP WITH TIME ZONE NOT NULL,
    scheduled_duration INTEGER DEFAULT 50, -- minutes
    
    -- Attendance
    actual_start TIMESTAMP WITH TIME ZONE,
    actual_end TIMESTAMP WITH TIME ZONE,
    patient_attended BOOLEAN DEFAULT TRUE,
    late_arrival_minutes INTEGER DEFAULT 0,
    no_show BOOLEAN DEFAULT FALSE,
    cancellation_reason TEXT,
    
    -- Session content
    session_focus TEXT[],
    interventions_used TEXT[],
    homework_assigned TEXT[],
    homework_reviewed TEXT[],
    
    -- Progress assessment
    mood_rating_start INTEGER, -- 1-10 scale
    mood_rating_end INTEGER, -- 1-10 scale
    anxiety_level_start INTEGER, -- 1-10 scale
    anxiety_level_end INTEGER, -- 1-10 scale
    session_productivity INTEGER, -- 1-5 therapist rating
    patient_engagement INTEGER, -- 1-5 therapist rating
    
    -- Clinical observations
    mental_status_observations TEXT,
    behavioral_observations TEXT,
    therapeutic_alliance_quality INTEGER, -- 1-5 scale
    
    -- Risk assessment
    suicide_risk_level VARCHAR(20), -- 'none', 'low', 'moderate', 'high'
    self_harm_risk_level VARCHAR(20),
    substance_use_indicators BOOLEAN DEFAULT FALSE,
    crisis_intervention_needed BOOLEAN DEFAULT FALSE,
    
    -- App integration data
    app_data_reviewed BOOLEAN DEFAULT FALSE,
    mood_data_discussed BOOLEAN DEFAULT FALSE,
    journal_entries_reviewed BOOLEAN DEFAULT FALSE,
    ai_insights_discussed BOOLEAN DEFAULT FALSE,
    
    -- Follow-up planning
    next_session_scheduled TIMESTAMP WITH TIME ZONE,
    between_session_contact_plan TEXT,
    emergency_plan_reviewed BOOLEAN DEFAULT FALSE,
    
    -- Documentation
    session_notes TEXT,
    treatment_plan_updates TEXT,
    recommendations TEXT,
    
    -- Billing and administrative
    billing_code VARCHAR(20),
    insurance_authorization TEXT,
    copay_collected DECIMAL(8,2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_mood_ratings CHECK (
        (mood_rating_start IS NULL OR (mood_rating_start >= 1 AND mood_rating_start <= 10)) AND
        (mood_rating_end IS NULL OR (mood_rating_end >= 1 AND mood_rating_end <= 10))
    ),
    CONSTRAINT chk_session_ratings CHECK (
        (session_productivity IS NULL OR (session_productivity >= 1 AND session_productivity <= 5)) AND
        (patient_engagement IS NULL OR (patient_engagement >= 1 AND patient_engagement <= 5)) AND
        (therapeutic_alliance_quality IS NULL OR (therapeutic_alliance_quality >= 1 AND therapeutic_alliance_quality <= 5))
    )
);

-- Clinical assessments and evaluations
CREATE TABLE clinical_assessments (
    assessment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(user_id),
    therapist_id UUID NOT NULL REFERENCES users(user_id),
    session_id UUID REFERENCES clinical_sessions(session_id),
    
    -- Assessment details
    assessment_type VARCHAR(50) NOT NULL, -- 'intake', 'progress', 'outcome', 'diagnostic'
    assessment_name VARCHAR(100), -- Name of standardized tool
    assessment_version VARCHAR(20),
    
    -- Scores and results
    raw_scores JSONB,
    scaled_scores JSONB,
    percentile_scores JSONB,
    clinical_interpretation TEXT,
    
    -- Standardized measures
    phq9_score INTEGER, -- Depression screening
    gad7_score INTEGER, -- Anxiety screening
    ptsd_checklist_score INTEGER,
    beck_depression_score INTEGER,
    beck_anxiety_score INTEGER,
    
    -- Functional assessment
    functioning_level clinical_severity,
    impairment_areas TEXT[],
    strengths_identified TEXT[],
    
    -- Risk assessment
    suicide_risk_score INTEGER,
    self_harm_risk_score INTEGER,
    substance_abuse_risk_score INTEGER,
    
    -- Comparison data
    baseline_assessment_id UUID REFERENCES clinical_assessments(assessment_id),
    previous_assessment_id UUID REFERENCES clinical_assessments(assessment_id),
    change_from_baseline JSONB,
    change_from_previous JSONB,
    
    -- Clinical significance
    clinically_significant_change BOOLEAN DEFAULT FALSE,
    reliable_change BOOLEAN DEFAULT FALSE,
    treatment_response VARCHAR(50), -- 'excellent', 'good', 'partial', 'minimal', 'none'
    
    -- Recommendations
    treatment_recommendations TEXT[],
    referral_recommendations TEXT[],
    medication_considerations TEXT,
    
    -- Administrative
    assessment_date DATE NOT NULL,
    completed_by UUID REFERENCES users(user_id),
    reviewed_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_standardized_scores CHECK (
        (phq9_score IS NULL OR (phq9_score >= 0 AND phq9_score <= 27)) AND
        (gad7_score IS NULL OR (gad7_score >= 0 AND gad7_score <= 21))
    )
);

-- Treatment progress tracking
CREATE TABLE treatment_progress (
    progress_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    treatment_plan_id UUID NOT NULL REFERENCES treatment_plans(plan_id),
    patient_id UUID NOT NULL REFERENCES users(user_id),
    
    -- Progress period
    reporting_period_start DATE NOT NULL,
    reporting_period_end DATE NOT NULL,
    
    -- Goal progress
    goals_progress JSONB NOT NULL, -- Progress on each goal
    objectives_met INTEGER DEFAULT 0,
    objectives_total INTEGER NOT NULL,
    
    -- Symptom tracking
    symptom_severity_scores JSONB,
    functional_improvement JSONB,
    quality_of_life_scores JSONB,
    
    -- Treatment engagement
    sessions_attended INTEGER DEFAULT 0,
    sessions_scheduled INTEGER DEFAULT 0,
    homework_completion_rate DECIMAL(5,2),
    app_engagement_score DECIMAL(5,2),
    
    -- Clinical improvements
    mood_improvement BOOLEAN DEFAULT FALSE,
    anxiety_reduction BOOLEAN DEFAULT FALSE,
    coping_skills_improved BOOLEAN DEFAULT FALSE,
    social_functioning_improved BOOLEAN DEFAULT FALSE,
    
    -- Barriers and challenges
    treatment_barriers TEXT[],
    adherence_challenges TEXT[],
    environmental_factors TEXT[],
    
    -- Recommendations
    treatment_modifications TEXT[],
    intensity_changes VARCHAR(50), -- 'increase', 'decrease', 'maintain'
    referral_needs TEXT[],
    
    -- Next steps
    next_review_date DATE,
    continuation_recommendation BOOLEAN DEFAULT TRUE,
    discharge_planning BOOLEAN DEFAULT FALSE,
    
    -- Documentation
    progress_summary TEXT NOT NULL,
    therapist_observations TEXT,
    patient_feedback TEXT,
    
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_progress_period CHECK (reporting_period_start <= reporting_period_end),
    CONSTRAINT chk_objectives_valid CHECK (objectives_met <= objectives_total),
    CONSTRAINT chk_completion_rate CHECK (homework_completion_rate IS NULL OR (homework_completion_rate >= 0 AND homework_completion_rate <= 100))
);

-- Clinical supervision and oversight
CREATE TABLE clinical_supervision (
    supervision_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supervisor_id UUID NOT NULL REFERENCES users(user_id),
    supervisee_id UUID NOT NULL REFERENCES users(user_id),
    
    -- Supervision session
    supervision_date DATE NOT NULL,
    session_duration_minutes INTEGER DEFAULT 60,
    supervision_type VARCHAR(50), -- 'individual', 'group', 'consultation'
    
    -- Cases discussed
    cases_reviewed UUID[], -- Array of patient IDs
    high_risk_cases UUID[], -- Array of patient IDs needing attention
    
    -- Supervision content
    clinical_issues_discussed TEXT[],
    ethical_issues_discussed TEXT[],
    skills_development_areas TEXT[],
    
    -- App integration oversight
    ai_interactions_reviewed BOOLEAN DEFAULT FALSE,
    crisis_detections_reviewed BOOLEAN DEFAULT FALSE,
    data_quality_issues TEXT[],
    
    -- Recommendations and actions
    supervisor_recommendations TEXT[],
    action_items TEXT[],
    training_needs_identified TEXT[],
    
    -- Quality assurance
    documentation_quality_score INTEGER, -- 1-5 scale
    clinical_judgment_score INTEGER, -- 1-5 scale
    professional_development_goals TEXT[],
    
    -- Follow-up
    next_supervision_date DATE,
    interim_check_ins_needed BOOLEAN DEFAULT FALSE,
    
    supervision_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_quality_scores CHECK (
        (documentation_quality_score IS NULL OR (documentation_quality_score >= 1 AND documentation_quality_score <= 5)) AND
        (clinical_judgment_score IS NULL OR (clinical_judgment_score >= 1 AND clinical_judgment_score <= 5))
    )
);

-- Indexes for performance
CREATE INDEX idx_therapeutic_relationships_therapist ON therapeutic_relationships(therapist_id);
CREATE INDEX idx_therapeutic_relationships_patient ON therapeutic_relationships(patient_id);
CREATE INDEX idx_therapeutic_relationships_active ON therapeutic_relationships(is_active);
CREATE INDEX idx_treatment_plans_relationship ON treatment_plans(relationship_id);
CREATE INDEX idx_treatment_plans_current ON treatment_plans(is_current);
CREATE INDEX idx_clinical_sessions_relationship ON clinical_sessions(relationship_id);
CREATE INDEX idx_clinical_sessions_scheduled ON clinical_sessions(scheduled_start);
CREATE INDEX idx_clinical_sessions_therapist ON clinical_sessions(therapist_id);
CREATE INDEX idx_clinical_assessments_patient ON clinical_assessments(patient_id);
CREATE INDEX idx_clinical_assessments_type ON clinical_assessments(assessment_type);
CREATE INDEX idx_clinical_assessments_date ON clinical_assessments(assessment_date);
CREATE INDEX idx_treatment_progress_plan ON treatment_progress(treatment_plan_id);
CREATE INDEX idx_clinical_supervision_supervisor ON clinical_supervision(supervisor_id);
CREATE INDEX idx_clinical_supervision_supervisee ON clinical_supervision(supervisee_id);
CREATE INDEX idx_clinical_supervision_date ON clinical_supervision(supervision_date);

-- Triggers for updated_at
CREATE TRIGGER update_therapeutic_relationships_updated_at BEFORE UPDATE ON therapeutic_relationships
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_treatment_plans_updated_at BEFORE UPDATE ON treatment_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_clinical_sessions_updated_at BEFORE UPDATE ON clinical_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
