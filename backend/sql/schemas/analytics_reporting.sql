-- Analytics and Reporting Schema
-- Handles platform insights, wellness trends, and outcome tracking
-- 
-- IMPORTANT: Analytics are for wellness insights and platform improvement.
-- They do not constitute medical diagnosis or treatment recommendations.
-- Users should consult healthcare providers for medical interpretation.

-- Report types and categories
CREATE TYPE report_type AS ENUM (
    'clinical_outcomes',
    'population_health',
    'quality_metrics',
    'utilization',
    'financial_performance',
    'operational_efficiency',
    'regulatory_compliance',
    'research_analytics',
    'patient_satisfaction',
    'provider_performance',
    'risk_analytics',
    'predictive_modeling'
);

-- Data aggregation levels
CREATE TYPE aggregation_level AS ENUM (
    'individual',
    'provider',
    'department',
    'facility',
    'network',
    'population',
    'regional',
    'national'
);

-- Report frequency
CREATE TYPE report_frequency AS ENUM (
    'real_time',
    'daily',
    'weekly',
    'monthly',
    'quarterly',
    'semi_annual',
    'annual',
    'ad_hoc'
);

-- Clinical outcome metrics
CREATE TABLE clinical_outcome_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Metric identification
    metric_name VARCHAR(200) NOT NULL,
    metric_category VARCHAR(100) NOT NULL, -- 'symptom_reduction', 'functional_improvement', 'quality_of_life'
    measurement_type VARCHAR(50) NOT NULL, -- 'percentage', 'score', 'count', 'ratio'
    
    -- Clinical context
    condition_measured VARCHAR(100), -- 'depression', 'anxiety', 'ptsd', 'general_mental_health'
    assessment_tool VARCHAR(100), -- 'PHQ-9', 'GAD-7', 'custom_scale'
    target_population VARCHAR(100), -- 'all_patients', 'adults', 'adolescents', 'specific_diagnosis'
    
    -- Calculation methodology
    calculation_formula TEXT NOT NULL,
    numerator_definition TEXT,
    denominator_definition TEXT,
    inclusion_criteria TEXT[],
    exclusion_criteria TEXT[],
    
    -- Benchmarking and targets
    target_value DECIMAL(10,4),
    benchmark_source VARCHAR(200),
    industry_benchmark DECIMAL(10,4),
    internal_benchmark DECIMAL(10,4),
    
    -- Measurement period
    measurement_timeframe VARCHAR(100), -- 'episode_of_care', '90_days', '6_months', '1_year'
    minimum_followup_days INTEGER,
    baseline_measurement_required BOOLEAN DEFAULT TRUE,
    
    -- Quality and validity
    evidence_base TEXT,
    validation_studies TEXT[],
    reliability_coefficient DECIMAL(4,3),
    
    -- Administrative
    created_by UUID REFERENCES users(user_id),
    approved_by UUID REFERENCES users(user_id),
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Population health analytics
CREATE TABLE population_health_metrics (
    population_metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Population definition
    population_name VARCHAR(200) NOT NULL,
    population_criteria JSONB NOT NULL, -- Complex criteria for population definition
    total_population_size INTEGER,
    
    -- Time period
    measurement_date DATE NOT NULL,
    measurement_period_start DATE NOT NULL,
    measurement_period_end DATE NOT NULL,
    
    -- Health status indicators
    prevalence_depression DECIMAL(5,2), -- Percentage
    prevalence_anxiety DECIMAL(5,2),
    prevalence_substance_abuse DECIMAL(5,2),
    prevalence_serious_mental_illness DECIMAL(5,2),
    
    -- Access and utilization
    treatment_penetration_rate DECIMAL(5,2), -- % of population receiving treatment
    first_contact_to_treatment_days DECIMAL(6,2), -- Average days
    treatment_completion_rate DECIMAL(5,2),
    crisis_service_utilization_rate DECIMAL(5,2),
    
    -- Outcomes and quality
    improvement_rate DECIMAL(5,2), -- % showing clinical improvement
    recovery_rate DECIMAL(5,2), -- % achieving recovery criteria
    readmission_rate DECIMAL(5,2), -- % requiring re-engagement
    suicide_attempt_rate DECIMAL(8,4), -- Per 100,000 population
    
    -- Social determinants
    employment_rate DECIMAL(5,2),
    housing_stability_rate DECIMAL(5,2),
    educational_attainment_distribution JSONB,
    insurance_coverage_distribution JSONB,
    
    -- Demographic breakdowns
    age_group_distribution JSONB,
    gender_distribution JSONB,
    race_ethnicity_distribution JSONB,
    geographic_distribution JSONB,
    
    -- Risk factors
    trauma_exposure_rate DECIMAL(5,2),
    adverse_childhood_experiences_rate DECIMAL(5,2),
    social_isolation_rate DECIMAL(5,2),
    financial_stress_rate DECIMAL(5,2),
    
    -- Protective factors
    social_support_availability DECIMAL(5,2),
    resilience_score DECIMAL(6,2),
    coping_skills_adequacy DECIMAL(5,2),
    
    -- Healthcare utilization
    primary_care_utilization_rate DECIMAL(5,2),
    emergency_room_visits_mental_health DECIMAL(8,2), -- Per 1,000 population
    hospitalization_rate_mental_health DECIMAL(8,2),
    medication_adherence_rate DECIMAL(5,2),
    
    -- Economic indicators
    total_cost_per_member DECIMAL(12,2),
    cost_per_quality_adjusted_life_year DECIMAL(12,2),
    productivity_loss_estimate DECIMAL(15,2),
    
    -- Data quality indicators
    data_completeness_percentage DECIMAL(5,2),
    data_sources TEXT[],
    calculation_methodology TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Quality improvement initiatives tracking
CREATE TABLE quality_improvement_initiatives (
    initiative_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Initiative details
    initiative_name VARCHAR(200) NOT NULL,
    initiative_type VARCHAR(100), -- 'care_protocol', 'workflow_improvement', 'technology_implementation'
    description TEXT,
    
    -- Objectives and goals
    primary_objective TEXT NOT NULL,
    specific_goals TEXT[],
    target_metrics TEXT[],
    success_criteria TEXT[],
    
    -- Timeline
    planned_start_date DATE NOT NULL,
    actual_start_date DATE,
    planned_end_date DATE,
    actual_end_date DATE,
    
    -- Scope and participants
    scope_description TEXT,
    target_population VARCHAR(200),
    participating_providers UUID[],
    affected_departments TEXT[],
    
    -- Baseline measurements
    baseline_measurement_date DATE,
    baseline_metrics JSONB, -- {"metric_name": value, ...}
    
    -- Implementation tracking
    implementation_phase VARCHAR(50), -- 'planning', 'pilot', 'rollout', 'maintenance', 'completed'
    milestones_achieved TEXT[],
    barriers_encountered TEXT[],
    mitigation_strategies TEXT[],
    
    -- Outcome measurements
    interim_measurements JSONB, -- Array of measurement periods and values
    final_measurements JSONB,
    improvement_achieved BOOLEAN,
    improvement_percentage DECIMAL(6,2),
    
    -- Statistical analysis
    statistical_significance BOOLEAN,
    p_value DECIMAL(6,4),
    confidence_interval JSONB,
    effect_size DECIMAL(6,4),
    
    -- Sustainability
    sustainability_plan TEXT,
    ongoing_monitoring_required BOOLEAN DEFAULT TRUE,
    monitoring_frequency VARCHAR(50),
    
    -- Cost-benefit analysis
    implementation_cost DECIMAL(12,2),
    ongoing_cost DECIMAL(12,2),
    estimated_savings DECIMAL(12,2),
    roi_percentage DECIMAL(6,2),
    
    -- Knowledge sharing
    lessons_learned TEXT,
    best_practices_identified TEXT[],
    replication_recommendations TEXT,
    
    -- Management
    initiative_lead UUID REFERENCES users(user_id),
    sponsor UUID REFERENCES users(user_id),
    status VARCHAR(50) DEFAULT 'planning',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Predictive analytics models
CREATE TABLE predictive_models (
    model_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Model identification
    model_name VARCHAR(200) NOT NULL,
    model_type VARCHAR(100) NOT NULL, -- 'risk_prediction', 'outcome_prediction', 'resource_planning'
    prediction_target VARCHAR(200) NOT NULL, -- 'crisis_risk', 'treatment_response', 'no_show_probability'
    
    -- Model details
    algorithm_type VARCHAR(100), -- 'logistic_regression', 'random_forest', 'neural_network', 'ensemble'
    model_version VARCHAR(20) NOT NULL,
    training_methodology TEXT,
    
    -- Data and features
    training_dataset_size INTEGER,
    feature_count INTEGER,
    key_features TEXT[],
    data_sources TEXT[],
    
    -- Performance metrics
    accuracy DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall_score DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    auc_roc DECIMAL(5,4),
    
    -- Validation and testing
    validation_method VARCHAR(100), -- 'cross_validation', 'holdout', 'temporal_split'
    test_dataset_size INTEGER,
    validation_accuracy DECIMAL(5,4),
    overfitting_indicators TEXT[],
    
    -- Deployment and usage
    deployment_date DATE,
    is_active BOOLEAN DEFAULT FALSE,
    usage_scope VARCHAR(100), -- 'clinical_decision_support', 'population_screening', 'resource_planning'
    
    -- Monitoring and maintenance
    performance_monitoring_frequency VARCHAR(50),
    last_performance_check DATE,
    model_drift_detected BOOLEAN DEFAULT FALSE,
    retrain_required BOOLEAN DEFAULT FALSE,
    
    -- Ethical and bias considerations
    bias_assessment_completed BOOLEAN DEFAULT FALSE,
    fairness_metrics JSONB,
    ethical_review_completed BOOLEAN DEFAULT FALSE,
    bias_mitigation_strategies TEXT[],
    
    -- Regulatory and compliance
    regulatory_approval_required BOOLEAN DEFAULT FALSE,
    regulatory_status VARCHAR(50),
    clinical_validation_required BOOLEAN DEFAULT TRUE,
    
    -- Documentation
    technical_documentation TEXT,
    clinical_documentation TEXT,
    user_guide TEXT,
    
    -- Management
    developed_by UUID REFERENCES users(user_id),
    approved_by UUID REFERENCES users(user_id),
    next_review_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Model predictions and scores
CREATE TABLE model_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_id UUID NOT NULL REFERENCES predictive_models(model_id),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Prediction details
    prediction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    prediction_value DECIMAL(8,6), -- Predicted score/probability
    prediction_category VARCHAR(100), -- 'high_risk', 'medium_risk', 'low_risk'
    confidence_score DECIMAL(5,4),
    
    -- Input features
    input_features JSONB NOT NULL, -- Feature values used for prediction
    feature_importance JSONB, -- Contribution of each feature to prediction
    
    -- Clinical context
    clinical_context VARCHAR(200), -- Context when prediction was made
    triggering_event VARCHAR(100), -- What prompted the prediction
    
    -- Actions and follow-up
    recommended_actions TEXT[],
    action_taken VARCHAR(200),
    action_taken_by UUID REFERENCES users(user_id),
    action_date DATE,
    
    -- Validation and feedback
    actual_outcome BOOLEAN, -- Did the predicted event occur?
    outcome_date DATE,
    prediction_accuracy_feedback DECIMAL(5,4),
    
    -- Usage tracking
    viewed_by_clinician BOOLEAN DEFAULT FALSE,
    incorporated_in_treatment BOOLEAN DEFAULT FALSE,
    patient_notified BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Business intelligence dashboards
CREATE TABLE bi_dashboards (
    dashboard_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Dashboard identification
    dashboard_name VARCHAR(200) NOT NULL,
    dashboard_category VARCHAR(100), -- 'clinical', 'operational', 'financial', 'quality'
    description TEXT,
    
    -- Target audience
    intended_audience VARCHAR(100), -- 'clinicians', 'administrators', 'executives', 'researchers'
    access_level VARCHAR(50), -- 'public', 'internal', 'restricted', 'confidential'
    
    -- Content and layout
    widget_configuration JSONB NOT NULL, -- Dashboard layout and widgets
    data_sources TEXT[],
    refresh_frequency VARCHAR(50), -- 'real_time', 'hourly', 'daily', 'weekly'
    
    -- Filters and parameters
    available_filters JSONB, -- User-configurable filters
    default_filter_values JSONB,
    date_range_options TEXT[],
    
    -- Performance and caching
    cache_duration_minutes INTEGER DEFAULT 60,
    query_complexity_score INTEGER,
    average_load_time_seconds DECIMAL(6,2),
    
    -- Usage analytics
    view_count INTEGER DEFAULT 0,
    unique_viewers INTEGER DEFAULT 0,
    last_accessed TIMESTAMP WITH TIME ZONE,
    most_used_filters JSONB,
    
    -- Maintenance
    created_by UUID REFERENCES users(user_id),
    last_modified_by UUID REFERENCES users(user_id),
    is_active BOOLEAN DEFAULT TRUE,
    version_number INTEGER DEFAULT 1,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Report scheduling and distribution
CREATE TABLE scheduled_reports (
    schedule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Report identification
    report_name VARCHAR(200) NOT NULL,
    report_type report_type NOT NULL,
    report_template TEXT, -- SQL query or report definition
    
    -- Scheduling
    frequency report_frequency NOT NULL,
    schedule_details JSONB, -- Cron-like schedule configuration
    next_run_date TIMESTAMP WITH TIME ZONE NOT NULL,
    last_run_date TIMESTAMP WITH TIME ZONE,
    
    -- Parameters and filters
    report_parameters JSONB, -- Default parameters for the report
    dynamic_filters JSONB, -- Filters that change based on context
    
    -- Distribution
    recipients UUID[], -- User IDs to receive the report
    distribution_groups TEXT[], -- Role-based distribution
    delivery_methods TEXT[], -- 'email', 'portal', 'api', 'file_export'
    
    -- Output format
    output_formats TEXT[], -- 'pdf', 'excel', 'csv', 'json'
    include_visualizations BOOLEAN DEFAULT TRUE,
    include_raw_data BOOLEAN DEFAULT FALSE,
    
    -- Conditional execution
    execution_conditions JSONB, -- Conditions that must be met to run
    minimum_data_requirements JSONB,
    skip_if_no_data BOOLEAN DEFAULT TRUE,
    
    -- Status and monitoring
    is_active BOOLEAN DEFAULT TRUE,
    execution_status VARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'running', 'completed', 'failed'
    last_execution_duration_minutes INTEGER,
    failure_count INTEGER DEFAULT 0,
    max_failures_before_disable INTEGER DEFAULT 3,
    
    -- Retention and cleanup
    retention_days INTEGER DEFAULT 90,
    auto_cleanup_enabled BOOLEAN DEFAULT TRUE,
    
    -- Notifications
    notify_on_success BOOLEAN DEFAULT FALSE,
    notify_on_failure BOOLEAN DEFAULT TRUE,
    notification_recipients UUID[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Data warehouse fact tables for analytics
CREATE TABLE fact_patient_encounters (
    fact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Dimensional keys
    patient_id UUID NOT NULL REFERENCES users(user_id),
    provider_id UUID REFERENCES healthcare_providers(provider_id),
    encounter_date DATE NOT NULL,
    
    -- Encounter characteristics
    encounter_type VARCHAR(50), -- 'initial', 'followup', 'crisis', 'group'
    service_modality VARCHAR(50), -- 'telehealth', 'in_person', 'phone'
    session_duration_minutes INTEGER,
    
    -- Clinical measures
    primary_diagnosis VARCHAR(20), -- ICD-10 code
    severity_score INTEGER,
    functioning_score INTEGER,
    treatment_response VARCHAR(50),
    
    -- Utilization measures
    days_since_last_encounter INTEGER,
    encounter_sequence_number INTEGER, -- 1st, 2nd, 3rd encounter for this episode
    
    -- Outcome measures
    pre_session_mood_rating INTEGER,
    post_session_mood_rating INTEGER,
    session_effectiveness_rating INTEGER,
    homework_completion_rate DECIMAL(5,2),
    
    -- Risk indicators
    crisis_risk_score DECIMAL(5,4),
    suicide_risk_level VARCHAR(20),
    no_show_risk_score DECIMAL(5,4),
    
    -- Financial measures
    billed_amount DECIMAL(10,2),
    collected_amount DECIMAL(10,2),
    insurance_payment DECIMAL(10,2),
    patient_payment DECIMAL(10,2),
    
    -- Quality indicators
    note_completion_timeliness INTEGER, -- Hours to complete note
    patient_satisfaction_score INTEGER,
    treatment_plan_adherence DECIMAL(5,2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Aggregated performance metrics
CREATE TABLE provider_performance_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES healthcare_providers(provider_id),
    
    -- Measurement period
    measurement_date DATE NOT NULL,
    measurement_period VARCHAR(50), -- 'monthly', 'quarterly', 'annual'
    
    -- Volume metrics
    total_encounters INTEGER DEFAULT 0,
    unique_patients INTEGER DEFAULT 0,
    new_patients INTEGER DEFAULT 0,
    average_encounters_per_patient DECIMAL(5,2),
    
    -- Clinical outcomes
    patient_improvement_rate DECIMAL(5,2), -- % showing improvement
    treatment_completion_rate DECIMAL(5,2),
    crisis_prevention_rate DECIMAL(5,2),
    average_symptom_reduction DECIMAL(6,2),
    
    -- Quality measures
    patient_satisfaction_average DECIMAL(3,2),
    note_completion_timeliness_average DECIMAL(6,2), -- Hours
    treatment_plan_adherence_rate DECIMAL(5,2),
    evidence_based_practice_utilization DECIMAL(5,2),
    
    -- Efficiency measures
    no_show_rate DECIMAL(5,2),
    cancellation_rate DECIMAL(5,2),
    schedule_utilization_rate DECIMAL(5,2),
    average_session_duration DECIMAL(5,2),
    
    -- Communication and coordination
    care_coordination_participation DECIMAL(5,2),
    referral_follow_through_rate DECIMAL(5,2),
    interdisciplinary_collaboration_score DECIMAL(3,2),
    
    -- Risk management
    crisis_detection_accuracy DECIMAL(5,4),
    safety_incident_rate DECIMAL(8,4), -- Per 1,000 encounters
    adverse_event_reporting_timeliness DECIMAL(6,2),
    
    -- Professional development
    continuing_education_hours INTEGER DEFAULT 0,
    training_completion_rate DECIMAL(5,2),
    certification_status VARCHAR(50),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for analytics performance
CREATE INDEX idx_clinical_outcome_metrics_category ON clinical_outcome_metrics(metric_category);
CREATE INDEX idx_population_health_metrics_date ON population_health_metrics(measurement_date);
CREATE INDEX idx_model_predictions_user_date ON model_predictions(user_id, prediction_date);
CREATE INDEX idx_fact_patient_encounters_patient_date ON fact_patient_encounters(patient_id, encounter_date);
CREATE INDEX idx_fact_patient_encounters_provider_date ON fact_patient_encounters(provider_id, encounter_date);
CREATE INDEX idx_provider_performance_provider_period ON provider_performance_metrics(provider_id, measurement_date);

-- Materialized views for common analytics queries
CREATE MATERIALIZED VIEW mv_monthly_clinical_outcomes AS
SELECT 
    DATE_TRUNC('month', encounter_date) as month,
    COUNT(*) as total_encounters,
    AVG(session_effectiveness_rating) as avg_effectiveness,
    AVG(post_session_mood_rating - pre_session_mood_rating) as avg_mood_improvement,
    COUNT(DISTINCT patient_id) as unique_patients
FROM fact_patient_encounters 
WHERE encounter_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', encounter_date);

-- Row Level Security for sensitive analytics
ALTER TABLE model_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE fact_patient_encounters ENABLE ROW LEVEL SECURITY;

-- Triggers for automated timestamp updates
CREATE TRIGGER update_clinical_outcome_metrics_updated_at
    BEFORE UPDATE ON clinical_outcome_metrics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quality_improvement_initiatives_updated_at
    BEFORE UPDATE ON quality_improvement_initiatives
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_predictive_models_updated_at
    BEFORE UPDATE ON predictive_models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bi_dashboards_updated_at
    BEFORE UPDATE ON bi_dashboards
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scheduled_reports_updated_at
    BEFORE UPDATE ON scheduled_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE clinical_outcome_metrics IS 'Definition and tracking of clinical outcome measures';
COMMENT ON TABLE population_health_metrics IS 'Population-level health analytics and trends';
COMMENT ON TABLE quality_improvement_initiatives IS 'Quality improvement projects and outcome tracking';
COMMENT ON TABLE predictive_models IS 'Machine learning models for clinical prediction';
COMMENT ON TABLE model_predictions IS 'Individual predictions and outcomes from ML models';
COMMENT ON TABLE bi_dashboards IS 'Business intelligence dashboard configurations';
COMMENT ON TABLE scheduled_reports IS 'Automated report scheduling and distribution';
COMMENT ON TABLE fact_patient_encounters IS 'Data warehouse fact table for encounter analytics';
COMMENT ON TABLE provider_performance_metrics IS 'Provider performance and quality metrics';
