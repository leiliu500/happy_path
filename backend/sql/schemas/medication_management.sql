-- Medication Management Schema
-- Handles medication tracking, reminders, and adherence support
-- 
-- IMPORTANT: This system provides medication tracking and reminder services only.
-- It does not prescribe medications or provide medical advice. All medication
-- decisions should be made in consultation with licensed healthcare providers.

-- Medication categories
CREATE TYPE medication_category AS ENUM (
    'antidepressant',
    'antianxiety',
    'antipsychotic',
    'mood_stabilizer',
    'stimulant',
    'sleep_aid',
    'supplement',
    'other_psychiatric',
    'non_psychiatric'
);

-- Dosage units
CREATE TYPE dosage_unit AS ENUM (
    'mg',
    'mcg',
    'g',
    'ml',
    'drops',
    'tablets',
    'capsules',
    'patches',
    'injections'
);

-- Frequency patterns
CREATE TYPE frequency_pattern AS ENUM (
    'once_daily',
    'twice_daily',
    'three_times_daily',
    'four_times_daily',
    'every_other_day',
    'weekly',
    'as_needed',
    'custom'
);

-- Side effect severity
CREATE TYPE side_effect_severity AS ENUM (
    'mild',
    'moderate',
    'severe',
    'life_threatening'
);

-- Medication status
CREATE TYPE medication_status AS ENUM (
    'active',
    'discontinued',
    'paused',
    'as_needed',
    'trial_period'
);

-- Drug database for psychiatric medications
CREATE TABLE psychiatric_medications (
    medication_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Basic medication information
    generic_name VARCHAR(200) NOT NULL,
    brand_names TEXT[],
    medication_category medication_category NOT NULL,
    
    -- Drug classification
    drug_class VARCHAR(100), -- 'SSRI', 'SNRI', 'Tricyclic', 'Benzodiazepine', etc.
    mechanism_of_action TEXT,
    primary_indications TEXT[],
    off_label_uses TEXT[],
    
    -- Dosage information
    available_strengths JSONB, -- [{"value": 10, "unit": "mg"}, {"value": 20, "unit": "mg"}]
    typical_starting_dose JSONB, -- {"value": 10, "unit": "mg", "frequency": "once_daily"}
    typical_maintenance_dose_range JSONB, -- {"min": 20, "max": 40, "unit": "mg"}
    maximum_dose JSONB,
    
    -- Administration details
    route_of_administration VARCHAR(50), -- 'oral', 'injection', 'transdermal', 'sublingual'
    food_restrictions TEXT,
    timing_recommendations TEXT,
    
    -- Pharmacokinetics
    half_life_hours DECIMAL(6,2),
    time_to_peak_hours DECIMAL(6,2),
    bioavailability_percent INTEGER,
    protein_binding_percent INTEGER,
    
    -- Clinical considerations
    onset_of_action TEXT, -- '2-4 weeks for antidepressants'
    contraindications TEXT[],
    warnings_precautions TEXT[],
    pregnancy_category VARCHAR(5),
    breastfeeding_safety VARCHAR(50),
    
    -- Drug interactions
    major_interactions TEXT[],
    moderate_interactions TEXT[],
    food_interactions TEXT[],
    
    -- Common side effects
    common_side_effects TEXT[],
    serious_side_effects TEXT[],
    withdrawal_considerations TEXT,
    
    -- Monitoring requirements
    required_lab_monitoring TEXT[],
    monitoring_frequency VARCHAR(100),
    baseline_assessments TEXT[],
    
    -- Regulatory information
    fda_approved BOOLEAN DEFAULT TRUE,
    controlled_substance_schedule VARCHAR(10),
    black_box_warning TEXT,
    
    -- Data management
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(user_id),
    last_reviewed_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User medication records
CREATE TABLE user_medications (
    medication_record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    medication_id UUID REFERENCES psychiatric_medications(medication_id),
    
    -- Medication details (for non-standard or external medications)
    custom_medication_name VARCHAR(200),
    
    -- Prescription information
    prescribed_by VARCHAR(200), -- Prescribing physician name
    prescriber_contact VARCHAR(200),
    prescription_date DATE NOT NULL,
    
    -- Current dosage and administration
    current_dose_amount DECIMAL(8,3) NOT NULL,
    dose_unit dosage_unit NOT NULL,
    frequency_pattern frequency_pattern NOT NULL,
    custom_frequency_details TEXT, -- For custom frequencies
    
    -- Timing and administration
    preferred_times TIME[], -- [08:00, 20:00] for twice daily
    with_food BOOLEAN,
    special_instructions TEXT,
    
    -- Medication status and duration
    status medication_status NOT NULL DEFAULT 'active',
    start_date DATE NOT NULL,
    end_date DATE,
    reason_for_discontinuation TEXT,
    
    -- Treatment context
    therapeutic_indication VARCHAR(200),
    target_symptoms TEXT[],
    treatment_goals TEXT[],
    
    -- Dosage history and titration
    initial_dose JSONB, -- {"amount": 10, "unit": "mg", "frequency": "once_daily"}
    dosage_increases INTEGER DEFAULT 0,
    dosage_decreases INTEGER DEFAULT 0,
    last_dose_change_date DATE,
    
    -- Clinical monitoring
    effectiveness_rating INTEGER, -- 1-10 scale
    side_effects_present BOOLEAN DEFAULT FALSE,
    adherence_percentage DECIMAL(5,2), -- Calculated from adherence tracking
    
    -- Cost and insurance
    insurance_covered BOOLEAN,
    copay_amount DECIMAL(8,2),
    pharmacy_name VARCHAR(200),
    
    -- Reminders and preferences
    reminder_enabled BOOLEAN DEFAULT TRUE,
    preferred_reminder_methods TEXT[] DEFAULT '{"push_notification"}',
    reminder_times TIME[],
    
    -- Data sharing
    shared_with_therapist BOOLEAN DEFAULT TRUE,
    emergency_access_enabled BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_dose_amount_positive CHECK (current_dose_amount > 0),
    CONSTRAINT chk_effectiveness_range CHECK (effectiveness_rating IS NULL OR (effectiveness_rating >= 1 AND effectiveness_rating <= 10)),
    CONSTRAINT chk_adherence_range CHECK (adherence_percentage IS NULL OR (adherence_percentage >= 0 AND adherence_percentage <= 100)),
    CONSTRAINT chk_medication_name CHECK (medication_id IS NOT NULL OR custom_medication_name IS NOT NULL)
);

-- Daily medication adherence tracking
CREATE TABLE medication_adherence (
    adherence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    medication_record_id UUID NOT NULL REFERENCES user_medications(medication_record_id) ON DELETE CASCADE,
    
    -- Adherence tracking
    scheduled_date DATE NOT NULL,
    scheduled_time TIME NOT NULL,
    
    -- Actual intake
    taken_date DATE,
    taken_time TIME,
    actual_dose_amount DECIMAL(8,3),
    
    -- Status tracking
    was_taken BOOLEAN NOT NULL DEFAULT FALSE,
    was_skipped BOOLEAN DEFAULT FALSE,
    skip_reason VARCHAR(100), -- 'forgot', 'side_effects', 'feeling_better', 'ran_out', 'other'
    
    -- Timing analysis
    minutes_late INTEGER DEFAULT 0, -- Negative for early
    within_window BOOLEAN DEFAULT TRUE, -- Based on acceptable timing window
    
    -- Context
    taken_with_food BOOLEAN,
    location_taken VARCHAR(100),
    mood_before_taking INTEGER, -- 1-10 scale
    mood_after_taking INTEGER,
    
    -- Side effects on this dose
    side_effects_experienced TEXT[],
    side_effect_severity side_effect_severity,
    side_effects_notes TEXT,
    
    -- Reminder effectiveness
    reminder_sent BOOLEAN DEFAULT FALSE,
    reminder_method VARCHAR(50),
    responded_to_reminder BOOLEAN DEFAULT FALSE,
    
    -- Data source
    reported_by VARCHAR(50) DEFAULT 'user', -- 'user', 'caregiver', 'automatic'
    confidence_level DECIMAL(3,2), -- For AI-detected adherence
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_actual_dose_positive CHECK (actual_dose_amount IS NULL OR actual_dose_amount > 0),
    CONSTRAINT chk_mood_range CHECK (
        (mood_before_taking IS NULL OR (mood_before_taking >= 1 AND mood_before_taking <= 10)) AND
        (mood_after_taking IS NULL OR (mood_after_taking >= 1 AND mood_after_taking <= 10))
    ),
    CONSTRAINT chk_timing_consistency CHECK (
        (was_taken = TRUE AND taken_date IS NOT NULL AND taken_time IS NOT NULL) OR
        (was_taken = FALSE)
    )
);

-- Side effects tracking
CREATE TABLE medication_side_effects (
    side_effect_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    medication_record_id UUID NOT NULL REFERENCES user_medications(medication_record_id) ON DELETE CASCADE,
    
    -- Side effect details
    side_effect_name VARCHAR(200) NOT NULL,
    severity side_effect_severity NOT NULL,
    frequency VARCHAR(50), -- 'daily', 'several_times_daily', 'weekly', 'occasional'
    
    -- Timing and pattern
    first_occurred_date DATE NOT NULL,
    last_occurred_date DATE,
    is_ongoing BOOLEAN DEFAULT TRUE,
    time_pattern VARCHAR(100), -- 'after_taking', 'between_doses', 'random'
    
    -- Impact assessment
    interference_with_daily_life INTEGER, -- 1-10 scale
    tolerability_rating INTEGER, -- 1-10 scale (10 = very tolerable)
    quality_of_life_impact INTEGER, -- 1-10 scale
    
    -- Management strategies
    management_strategies TEXT[],
    dose_reduction_helpful BOOLEAN,
    timing_change_helpful BOOLEAN,
    
    -- Clinical response
    reported_to_prescriber BOOLEAN DEFAULT FALSE,
    prescriber_response TEXT,
    action_taken VARCHAR(100), -- 'none', 'dose_reduction', 'medication_change', 'additional_medication'
    
    -- Resolution
    resolved BOOLEAN DEFAULT FALSE,
    resolution_date DATE,
    resolution_method VARCHAR(100),
    
    -- Additional context
    notes TEXT,
    related_to_dose_change BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_interference_range CHECK (interference_with_daily_life >= 1 AND interference_with_daily_life <= 10),
    CONSTRAINT chk_tolerability_range CHECK (tolerability_rating >= 1 AND tolerability_rating <= 10),
    CONSTRAINT chk_qol_impact_range CHECK (quality_of_life_impact >= 1 AND quality_of_life_impact <= 10)
);

-- Drug interaction checking
CREATE TABLE drug_interactions (
    interaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    medication_1_id UUID NOT NULL REFERENCES psychiatric_medications(medication_id),
    medication_2_id UUID NOT NULL REFERENCES psychiatric_medications(medication_id),
    
    -- Interaction details
    interaction_type VARCHAR(50) NOT NULL, -- 'major', 'moderate', 'minor'
    clinical_significance VARCHAR(100),
    mechanism TEXT,
    
    -- Effects and management
    potential_effects TEXT[],
    management_recommendations TEXT[],
    monitoring_requirements TEXT[],
    
    -- Documentation
    evidence_level VARCHAR(50), -- 'established', 'probable', 'possible', 'theoretical'
    literature_references TEXT[],
    
    -- Status
    is_contraindicated BOOLEAN DEFAULT FALSE,
    requires_dose_adjustment BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_different_medications CHECK (medication_1_id != medication_2_id)
);

-- User-specific interaction alerts
CREATE TABLE user_interaction_alerts (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    interaction_id UUID NOT NULL REFERENCES drug_interactions(interaction_id),
    medication_record_1_id UUID NOT NULL REFERENCES user_medications(medication_record_id),
    medication_record_2_id UUID NOT NULL REFERENCES user_medications(medication_record_id),
    
    -- Alert details
    alert_date DATE NOT NULL DEFAULT CURRENT_DATE,
    severity_level VARCHAR(50) NOT NULL,
    alert_message TEXT NOT NULL,
    
    -- Response tracking
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by UUID REFERENCES users(user_id),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    
    -- Clinical action
    action_required BOOLEAN DEFAULT FALSE,
    action_taken TEXT,
    prescriber_notified BOOLEAN DEFAULT FALSE,
    
    -- Resolution
    is_resolved BOOLEAN DEFAULT FALSE,
    resolution_date DATE,
    resolution_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Medication effectiveness tracking
CREATE TABLE medication_effectiveness (
    effectiveness_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    medication_record_id UUID NOT NULL REFERENCES user_medications(medication_record_id) ON DELETE CASCADE,
    
    -- Assessment period
    assessment_date DATE NOT NULL,
    weeks_on_medication INTEGER NOT NULL,
    
    -- Effectiveness ratings
    overall_effectiveness INTEGER NOT NULL, -- 1-10 scale
    symptom_improvement INTEGER, -- 1-10 scale
    functional_improvement INTEGER, -- 1-10 scale
    quality_of_life_improvement INTEGER, -- 1-10 scale
    
    -- Specific symptom tracking
    target_symptoms JSONB, -- {"depression": 7, "anxiety": 5, "sleep": 8}
    symptom_severity_before JSONB,
    symptom_severity_current JSONB,
    
    -- Side effect burden
    side_effect_burden INTEGER, -- 1-10 scale (10 = no side effects)
    tolerability_rating INTEGER, -- 1-10 scale
    
    -- Treatment satisfaction
    satisfaction_rating INTEGER, -- 1-10 scale
    would_recommend BOOLEAN,
    
    -- Clinical context
    dose_at_assessment JSONB,
    concurrent_medications TEXT[],
    therapy_involvement BOOLEAN DEFAULT FALSE,
    
    -- Assessment source
    assessed_by VARCHAR(50) DEFAULT 'patient', -- 'patient', 'clinician', 'caregiver'
    assessment_method VARCHAR(100), -- 'self_report', 'clinical_interview', 'standardized_scale'
    
    -- Follow-up
    next_assessment_date DATE,
    recommendations TEXT[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_weeks_positive CHECK (weeks_on_medication > 0),
    CONSTRAINT chk_effectiveness_ratings CHECK (
        overall_effectiveness >= 1 AND overall_effectiveness <= 10 AND
        (symptom_improvement IS NULL OR (symptom_improvement >= 1 AND symptom_improvement <= 10)) AND
        (functional_improvement IS NULL OR (functional_improvement >= 1 AND functional_improvement <= 10)) AND
        (quality_of_life_improvement IS NULL OR (quality_of_life_improvement >= 1 AND quality_of_life_improvement <= 10)) AND
        (side_effect_burden IS NULL OR (side_effect_burden >= 1 AND side_effect_burden <= 10)) AND
        (tolerability_rating IS NULL OR (tolerability_rating >= 1 AND tolerability_rating <= 10)) AND
        (satisfaction_rating IS NULL OR (satisfaction_rating >= 1 AND satisfaction_rating <= 10))
    )
);

-- Indexes for performance
CREATE INDEX idx_user_medications_user_id ON user_medications(user_id);
CREATE INDEX idx_user_medications_status ON user_medications(status);
CREATE INDEX idx_medication_adherence_user_date ON medication_adherence(user_id, scheduled_date);
CREATE INDEX idx_medication_adherence_medication_record ON medication_adherence(medication_record_id);
CREATE INDEX idx_side_effects_user_medication ON medication_side_effects(user_id, medication_record_id);
CREATE INDEX idx_interaction_alerts_user_unresolved ON user_interaction_alerts(user_id) WHERE is_resolved = FALSE;
CREATE INDEX idx_effectiveness_user_medication ON medication_effectiveness(user_id, medication_record_id);

-- Row Level Security
ALTER TABLE user_medications ENABLE ROW LEVEL SECURITY;
ALTER TABLE medication_adherence ENABLE ROW LEVEL SECURITY;
ALTER TABLE medication_side_effects ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_interaction_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE medication_effectiveness ENABLE ROW LEVEL SECURITY;

-- Triggers for automated timestamp updates
CREATE TRIGGER update_psychiatric_medications_updated_at
    BEFORE UPDATE ON psychiatric_medications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_medications_updated_at
    BEFORE UPDATE ON user_medications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_medication_adherence_updated_at
    BEFORE UPDATE ON medication_adherence
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_medication_side_effects_updated_at
    BEFORE UPDATE ON medication_side_effects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE psychiatric_medications IS 'Reference database of psychiatric medications with clinical information';
COMMENT ON TABLE user_medications IS 'Individual medication records for users with prescription details';
COMMENT ON TABLE medication_adherence IS 'Daily tracking of medication intake and adherence patterns';
COMMENT ON TABLE medication_side_effects IS 'Tracking and management of medication side effects';
COMMENT ON TABLE drug_interactions IS 'Reference database of drug-drug interactions';
COMMENT ON TABLE user_interaction_alerts IS 'Active interaction alerts for users medication combinations';
COMMENT ON TABLE medication_effectiveness IS 'Longitudinal tracking of medication effectiveness and outcomes';
