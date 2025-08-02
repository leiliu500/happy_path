-- System Administration and Auditing Schema
-- Handles system monitoring, audit logs, analytics, and administrative functions

-- Log levels for system events
CREATE TYPE log_level AS ENUM (
    'debug',
    'info',
    'warning',
    'error',
    'critical'
);

-- Event categories for auditing
CREATE TYPE event_category AS ENUM (
    'authentication',
    'authorization',
    'data_access',
    'data_modification',
    'crisis_detection',
    'ai_interaction',
    'system_admin',
    'privacy_compliance',
    'security_incident',
    'performance'
);

-- System audit logs
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event identification
    event_category event_category NOT NULL,
    event_type VARCHAR(100) NOT NULL, -- Specific event within category
    event_description TEXT NOT NULL,
    
    -- User and session context
    user_id UUID REFERENCES users(user_id),
    session_id UUID,
    impersonated_user_id UUID REFERENCES users(user_id), -- For admin actions
    
    -- Request context
    ip_address INET,
    user_agent TEXT,
    request_method VARCHAR(10),
    request_url TEXT,
    request_headers JSONB,
    
    -- Data context
    affected_table VARCHAR(100),
    affected_record_id UUID,
    old_values JSONB,
    new_values JSONB,
    
    -- Security context
    authentication_method VARCHAR(50),
    authorization_level VARCHAR(50),
    permission_checked VARCHAR(100),
    access_granted BOOLEAN,
    
    -- System context
    application_version VARCHAR(50),
    server_instance VARCHAR(100),
    processing_time_ms INTEGER,
    
    -- Compliance and privacy
    phi_accessed BOOLEAN DEFAULT FALSE, -- Protected Health Information
    consent_verified BOOLEAN,
    data_retention_rule VARCHAR(100),
    
    -- Severity and alerting
    log_level log_level NOT NULL DEFAULT 'info',
    requires_review BOOLEAN DEFAULT FALSE,
    alert_sent BOOLEAN DEFAULT FALSE,
    
    -- Correlation
    correlation_id UUID, -- Groups related events
    parent_event_id UUID REFERENCES audit_logs(log_id),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_processing_time_positive CHECK (processing_time_ms IS NULL OR processing_time_ms >= 0)
);

-- System configuration and settings
CREATE TABLE system_configurations (
    config_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_key VARCHAR(200) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    
    -- Configuration metadata
    config_category VARCHAR(100) NOT NULL,
    config_description TEXT,
    data_type VARCHAR(50) NOT NULL, -- 'string', 'integer', 'boolean', 'json', 'float'
    
    -- Validation
    validation_rules JSONB, -- {"min": 0, "max": 100, "required": true}
    default_value TEXT,
    
    -- Environment and deployment
    environment VARCHAR(50) DEFAULT 'production', -- 'development', 'staging', 'production'
    deployment_version VARCHAR(50),
    
    -- Change management
    changed_by UUID REFERENCES users(user_id),
    change_reason TEXT,
    previous_value TEXT,
    
    -- Security
    is_sensitive BOOLEAN DEFAULT FALSE, -- Contains sensitive data
    encryption_required BOOLEAN DEFAULT FALSE,
    access_level VARCHAR(50) DEFAULT 'admin', -- Who can modify
    
    -- Lifecycle
    is_active BOOLEAN DEFAULT TRUE,
    effective_from TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    effective_until TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System performance monitoring
CREATE TABLE system_performance (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Time and measurement
    measurement_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metric_name VARCHAR(100) NOT NULL,
    metric_category VARCHAR(50) NOT NULL, -- 'database', 'api', 'ai_model', 'system'
    
    -- Metric values
    metric_value DECIMAL(15,6) NOT NULL,
    metric_unit VARCHAR(20), -- 'ms', 'seconds', 'percentage', 'count', 'bytes'
    
    -- Context
    server_instance VARCHAR(100),
    application_component VARCHAR(100),
    user_id UUID REFERENCES users(user_id), -- For user-specific metrics
    
    -- Thresholds and alerting
    warning_threshold DECIMAL(15,6),
    critical_threshold DECIMAL(15,6),
    is_alert BOOLEAN DEFAULT FALSE,
    alert_level VARCHAR(20), -- 'warning', 'critical'
    
    -- Additional metadata
    metadata JSONB,
    
    CONSTRAINT chk_thresholds CHECK (
        warning_threshold IS NULL OR 
        critical_threshold IS NULL OR 
        warning_threshold <= critical_threshold
    )
);

-- Data privacy and compliance tracking
CREATE TABLE privacy_compliance (
    compliance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Subject of compliance
    user_id UUID REFERENCES users(user_id),
    data_subject_type VARCHAR(50) DEFAULT 'user', -- 'user', 'patient', 'minor'
    
    -- Compliance action
    action_type VARCHAR(100) NOT NULL, -- 'data_export', 'data_deletion', 'consent_update'
    action_description TEXT NOT NULL,
    
    -- Legal basis
    legal_basis VARCHAR(100), -- 'consent', 'legitimate_interest', 'vital_interest'
    regulation_reference VARCHAR(100), -- 'GDPR', 'HIPAA', 'CCPA'
    
    -- Request details
    requested_by UUID REFERENCES users(user_id),
    request_date TIMESTAMP WITH TIME ZONE,
    request_reason TEXT,
    
    -- Processing details
    data_categories TEXT[], -- 'personal_data', 'health_data', 'usage_data'
    data_sources TEXT[], -- Tables/systems affected
    retention_period_days INTEGER,
    
    -- Completion tracking
    processing_started TIMESTAMP WITH TIME ZONE,
    processing_completed TIMESTAMP WITH TIME ZONE,
    verification_completed TIMESTAMP WITH TIME ZONE,
    
    -- Results
    records_affected INTEGER DEFAULT 0,
    data_exported_location TEXT,
    deletion_confirmation TEXT,
    
    -- Quality assurance
    processed_by UUID REFERENCES users(user_id),
    reviewed_by UUID REFERENCES users(user_id),
    compliance_notes TEXT,
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_retention_period_positive CHECK (retention_period_days IS NULL OR retention_period_days >= 0),
    CONSTRAINT chk_records_affected_positive CHECK (records_affected >= 0)
);

-- System health checks and monitoring
CREATE TABLE system_health_checks (
    check_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Check identification
    check_name VARCHAR(100) NOT NULL,
    check_category VARCHAR(50) NOT NULL, -- 'database', 'api', 'ai_service', 'external_service'
    check_description TEXT,
    
    -- Check execution
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    execution_duration_ms INTEGER,
    
    -- Results
    status VARCHAR(20) NOT NULL, -- 'healthy', 'warning', 'critical', 'down'
    success BOOLEAN NOT NULL,
    response_time_ms INTEGER,
    
    -- Detailed results
    check_results JSONB,
    error_message TEXT,
    stack_trace TEXT,
    
    -- Thresholds
    warning_threshold_ms INTEGER,
    critical_threshold_ms INTEGER,
    
    -- Dependencies
    depends_on_services TEXT[],
    
    -- Alerting
    alert_triggered BOOLEAN DEFAULT FALSE,
    alert_recipients TEXT[],
    
    -- Remediation
    auto_remediation_attempted BOOLEAN DEFAULT FALSE,
    remediation_actions TEXT[],
    
    CONSTRAINT chk_execution_duration_positive CHECK (execution_duration_ms IS NULL OR execution_duration_ms >= 0),
    CONSTRAINT chk_response_time_positive CHECK (response_time_ms IS NULL OR response_time_ms >= 0)
);

-- AI model performance and monitoring
CREATE TABLE ai_model_monitoring (
    monitoring_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Model identification
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    model_type VARCHAR(50) NOT NULL, -- 'crisis_detection', 'mood_analysis', 'chat_response'
    
    -- Performance metrics
    measurement_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    accuracy_score DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall_score DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    
    -- Usage metrics
    total_predictions INTEGER DEFAULT 0,
    successful_predictions INTEGER DEFAULT 0,
    failed_predictions INTEGER DEFAULT 0,
    average_response_time_ms DECIMAL(10,2),
    
    -- Quality metrics
    user_satisfaction_score DECIMAL(3,2), -- 1-5 scale
    false_positive_rate DECIMAL(5,4),
    false_negative_rate DECIMAL(5,4),
    
    -- Bias and fairness metrics
    demographic_parity DECIMAL(5,4),
    equalized_odds DECIMAL(5,4),
    bias_detected BOOLEAN DEFAULT FALSE,
    bias_categories TEXT[],
    
    -- Data quality
    data_drift_detected BOOLEAN DEFAULT FALSE,
    concept_drift_detected BOOLEAN DEFAULT FALSE,
    data_quality_score DECIMAL(3,2),
    
    -- Resource utilization
    cpu_usage_percentage DECIMAL(5,2),
    memory_usage_mb INTEGER,
    gpu_usage_percentage DECIMAL(5,2),
    storage_usage_mb INTEGER,
    
    -- Cost tracking
    compute_cost_usd DECIMAL(10,4),
    api_calls_count INTEGER DEFAULT 0,
    token_usage INTEGER DEFAULT 0,
    
    -- Alerts and thresholds
    performance_alert BOOLEAN DEFAULT FALSE,
    bias_alert BOOLEAN DEFAULT FALSE,
    drift_alert BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    monitoring_source VARCHAR(50) DEFAULT 'automated',
    notes TEXT,
    
    CONSTRAINT chk_scores_range CHECK (
        (accuracy_score IS NULL OR (accuracy_score >= 0 AND accuracy_score <= 1)) AND
        (precision_score IS NULL OR (precision_score >= 0 AND precision_score <= 1)) AND
        (recall_score IS NULL OR (recall_score >= 0 AND recall_score <= 1)) AND
        (f1_score IS NULL OR (f1_score >= 0 AND f1_score <= 1))
    ),
    CONSTRAINT chk_prediction_counts CHECK (
        total_predictions >= 0 AND 
        successful_predictions >= 0 AND 
        failed_predictions >= 0 AND
        successful_predictions + failed_predictions <= total_predictions
    )
);

-- Data retention and cleanup tracking
CREATE TABLE data_retention_tracking (
    tracking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Retention policy
    policy_name VARCHAR(100) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    retention_period_days INTEGER NOT NULL,
    
    -- Cleanup execution
    cleanup_date DATE NOT NULL,
    cutoff_date DATE NOT NULL, -- Data older than this was cleaned
    
    -- Results
    records_identified INTEGER DEFAULT 0,
    records_deleted INTEGER DEFAULT 0,
    records_archived INTEGER DEFAULT 0,
    data_size_freed_mb DECIMAL(15,2),
    
    -- Execution details
    execution_started TIMESTAMP WITH TIME ZONE,
    execution_completed TIMESTAMP WITH TIME ZONE,
    execution_duration_minutes INTEGER,
    
    -- Verification
    verification_completed BOOLEAN DEFAULT FALSE,
    verification_notes TEXT,
    
    -- Next scheduled cleanup
    next_cleanup_date DATE,
    
    -- Status and errors
    status VARCHAR(50) DEFAULT 'completed', -- 'scheduled', 'running', 'completed', 'failed'
    error_details TEXT,
    
    performed_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_retention_period_positive CHECK (retention_period_days > 0),
    CONSTRAINT chk_cleanup_dates CHECK (cutoff_date <= cleanup_date),
    CONSTRAINT chk_record_counts CHECK (
        records_identified >= 0 AND 
        records_deleted >= 0 AND 
        records_archived >= 0 AND
        (records_deleted + records_archived) <= records_identified
    )
);

-- System analytics and reporting
CREATE TABLE system_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Reporting period
    report_date DATE NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- 'daily', 'weekly', 'monthly', 'quarterly'
    
    -- User metrics
    total_users INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    new_registrations INTEGER DEFAULT 0,
    user_retention_rate DECIMAL(5,2),
    
    -- Engagement metrics
    total_sessions INTEGER DEFAULT 0,
    average_session_duration DECIMAL(10,2),
    total_messages INTEGER DEFAULT 0,
    total_journal_entries INTEGER DEFAULT 0,
    total_mood_entries INTEGER DEFAULT 0,
    
    -- Crisis and safety metrics
    crisis_detections INTEGER DEFAULT 0,
    escalations_triggered INTEGER DEFAULT 0,
    safety_interventions INTEGER DEFAULT 0,
    false_positives INTEGER DEFAULT 0,
    
    -- Clinical metrics
    therapy_sessions INTEGER DEFAULT 0,
    treatment_plans_created INTEGER DEFAULT 0,
    assessments_completed INTEGER DEFAULT 0,
    
    -- System performance
    average_response_time_ms DECIMAL(10,2),
    system_uptime_percentage DECIMAL(5,2),
    error_rate_percentage DECIMAL(5,2),
    
    -- AI metrics
    ai_responses_generated INTEGER DEFAULT 0,
    ai_accuracy_score DECIMAL(5,4),
    user_satisfaction_ai DECIMAL(3,2),
    
    -- Business metrics
    subscription_revenue DECIMAL(12,2),
    churn_rate DECIMAL(5,2),
    customer_acquisition_cost DECIMAL(10,2),
    
    -- Compliance metrics
    privacy_requests INTEGER DEFAULT 0,
    data_breaches INTEGER DEFAULT 0,
    audit_findings INTEGER DEFAULT 0,
    
    -- Generated metadata
    generated_by VARCHAR(50) DEFAULT 'automated',
    data_freshness_hours INTEGER, -- How old is the data
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_user_counts CHECK (
        total_users >= 0 AND 
        active_users >= 0 AND 
        new_registrations >= 0 AND
        active_users <= total_users
    ),
    CONSTRAINT chk_percentage_ranges CHECK (
        (user_retention_rate IS NULL OR (user_retention_rate >= 0 AND user_retention_rate <= 100)) AND
        (system_uptime_percentage IS NULL OR (system_uptime_percentage >= 0 AND system_uptime_percentage <= 100)) AND
        (error_rate_percentage IS NULL OR (error_rate_percentage >= 0 AND error_rate_percentage <= 100))
    )
);

-- Indexes for performance
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_category ON audit_logs(event_category);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_level ON audit_logs(log_level);
CREATE INDEX idx_audit_logs_requires_review ON audit_logs(requires_review);
CREATE INDEX idx_system_configurations_key ON system_configurations(config_key);
CREATE INDEX idx_system_configurations_category ON system_configurations(config_category);
CREATE INDEX idx_system_configurations_active ON system_configurations(is_active);
CREATE INDEX idx_system_performance_timestamp ON system_performance(measurement_timestamp);
CREATE INDEX idx_system_performance_metric ON system_performance(metric_name);
CREATE INDEX idx_system_performance_alert ON system_performance(is_alert);
CREATE INDEX idx_privacy_compliance_user_id ON privacy_compliance(user_id);
CREATE INDEX idx_privacy_compliance_action ON privacy_compliance(action_type);
CREATE INDEX idx_privacy_compliance_status ON privacy_compliance(status);
CREATE INDEX idx_system_health_checks_executed_at ON system_health_checks(executed_at);
CREATE INDEX idx_system_health_checks_status ON system_health_checks(status);
CREATE INDEX idx_ai_model_monitoring_timestamp ON ai_model_monitoring(measurement_timestamp);
CREATE INDEX idx_ai_model_monitoring_model ON ai_model_monitoring(model_name, model_version);
CREATE INDEX idx_data_retention_tracking_table ON data_retention_tracking(table_name);
CREATE INDEX idx_data_retention_tracking_date ON data_retention_tracking(cleanup_date);
CREATE INDEX idx_system_analytics_date ON system_analytics(report_date);
CREATE INDEX idx_system_analytics_type ON system_analytics(report_type);

-- Triggers for updated_at
CREATE TRIGGER update_system_configurations_updated_at BEFORE UPDATE ON system_configurations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_privacy_compliance_updated_at BEFORE UPDATE ON privacy_compliance
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
