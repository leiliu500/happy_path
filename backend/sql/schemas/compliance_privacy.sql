-- Compliance and Privacy Management Schema
-- Handles HIPAA compliance, data retention, consent management, and regulatory requirements

-- Consent types for different data uses
CREATE TYPE consent_type AS ENUM (
    'treatment',
    'payment',
    'healthcare_operations',
    'research',
    'marketing',
    'data_sharing',
    'telehealth',
    'crisis_intervention',
    'family_involvement',
    'photography_recording',
    'ai_analysis',
    'quality_improvement',
    'training_education',
    'legal_proceedings'
);

-- Consent status
CREATE TYPE consent_status AS ENUM (
    'granted',
    'denied',
    'withdrawn',
    'expired',
    'pending',
    'conditional'
);

-- Data classification levels
CREATE TYPE data_classification AS ENUM (
    'public',
    'internal',
    'confidential',
    'restricted',
    'phi',              -- Protected Health Information
    'psychotherapy_notes', -- Special protection under HIPAA
    'substance_abuse',  -- 42 CFR Part 2 protected
    'minor_records',    -- Additional protections for minors
    'genetic_data'      -- GINA protections
);

-- Privacy request types
CREATE TYPE privacy_request_type AS ENUM (
    'access',           -- Right to access personal data
    'portability',      -- Right to data portability
    'rectification',    -- Right to correct data
    'erasure',          -- Right to deletion/forgetting
    'restriction',      -- Restriction of processing
    'objection',        -- Object to processing
    'accounting',       -- Accounting of disclosures
    'amendment',        -- Amendment to medical records
    'complaint'         -- Privacy complaints
);

-- Retention schedules and policies
CREATE TABLE data_retention_policies (
    policy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Policy identification
    policy_name VARCHAR(200) NOT NULL,
    policy_version VARCHAR(20) DEFAULT '1.0',
    data_category VARCHAR(100) NOT NULL,
    data_classification data_classification NOT NULL,
    
    -- Retention requirements
    retention_period_years INTEGER,
    retention_period_months INTEGER,
    retention_trigger VARCHAR(100), -- 'creation_date', 'last_access', 'last_treatment', 'account_closure'
    
    -- Legal and regulatory basis
    legal_basis TEXT[], -- HIPAA, state law, research requirements, etc.
    regulatory_requirements TEXT[],
    business_justification TEXT,
    
    -- Disposal requirements
    disposal_method VARCHAR(100), -- 'secure_deletion', 'physical_destruction', 'anonymization'
    disposal_certification_required BOOLEAN DEFAULT TRUE,
    disposal_notification_required BOOLEAN DEFAULT FALSE,
    
    -- Exceptions and holds
    litigation_hold_exempt BOOLEAN DEFAULT FALSE,
    research_extension_allowed BOOLEAN DEFAULT FALSE,
    patient_request_override BOOLEAN DEFAULT FALSE,
    
    -- Administrative
    effective_date DATE NOT NULL,
    expiration_date DATE,
    approved_by UUID REFERENCES users(user_id),
    approval_date DATE,
    
    -- Review and maintenance
    review_frequency_months INTEGER DEFAULT 12,
    last_review_date DATE,
    next_review_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_retention_period_positive CHECK (
        (retention_period_years IS NULL OR retention_period_years > 0) AND
        (retention_period_months IS NULL OR retention_period_months > 0)
    ),
    CONSTRAINT chk_retention_period_specified CHECK (retention_period_years IS NOT NULL OR retention_period_months IS NOT NULL)
);

-- User consent management
CREATE TABLE user_consents (
    consent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Consent details
    consent_type consent_type NOT NULL,
    consent_status consent_status NOT NULL DEFAULT 'pending',
    
    -- Consent content
    consent_text TEXT NOT NULL,
    consent_version VARCHAR(20) NOT NULL,
    purpose_description TEXT NOT NULL,
    data_types_covered TEXT[],
    
    -- Legal basis
    legal_basis VARCHAR(100), -- 'consent', 'legitimate_interest', 'vital_interest', 'legal_obligation'
    regulatory_framework VARCHAR(100), -- 'HIPAA', 'GDPR', 'CCPA', '42_CFR_Part_2'
    
    -- Consent lifecycle
    granted_date TIMESTAMP WITH TIME ZONE,
    effective_date DATE,
    expiration_date DATE,
    withdrawn_date TIMESTAMP WITH TIME ZONE,
    withdrawal_reason TEXT,
    
    -- Consent conditions
    conditions_applied TEXT[],
    restrictions TEXT[],
    special_requirements TEXT,
    
    -- Third party involvement
    third_parties_involved TEXT[],
    data_sharing_scope TEXT,
    
    -- Documentation
    consent_method VARCHAR(50), -- 'electronic_signature', 'verbal', 'written', 'implied'
    witness_name VARCHAR(200),
    witness_signature_date DATE,
    
    -- Verification
    identity_verified BOOLEAN DEFAULT TRUE,
    verification_method VARCHAR(100),
    guardian_consent_required BOOLEAN DEFAULT FALSE,
    guardian_consent_obtained BOOLEAN DEFAULT FALSE,
    
    -- Administrative
    obtained_by UUID REFERENCES users(user_id),
    location_obtained VARCHAR(200),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Privacy and data requests
CREATE TABLE privacy_requests (
    request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Request details
    request_type privacy_request_type NOT NULL,
    request_description TEXT NOT NULL,
    specific_data_requested TEXT[],
    date_range_start DATE,
    date_range_end DATE,
    
    -- Request processing
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'denied', 'partially_fulfilled'
    submitted_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    completed_date DATE,
    
    -- Verification
    identity_verification_method VARCHAR(100),
    identity_verified BOOLEAN DEFAULT FALSE,
    verification_documents TEXT[],
    
    -- Processing details
    assigned_to UUID REFERENCES users(user_id),
    complexity_level VARCHAR(20) DEFAULT 'standard', -- 'simple', 'standard', 'complex'
    estimated_hours DECIMAL(6,2),
    actual_hours DECIMAL(6,2),
    
    -- Response information
    response_method VARCHAR(50), -- 'secure_email', 'portal', 'mail', 'in_person'
    response_delivered BOOLEAN DEFAULT FALSE,
    delivery_confirmation TEXT,
    
    -- Denial or restrictions
    denial_reason TEXT,
    legal_basis_for_denial TEXT,
    partial_fulfillment_reason TEXT,
    
    -- Fee information
    fees_applicable BOOLEAN DEFAULT FALSE,
    estimated_fee DECIMAL(10,2),
    fee_waived BOOLEAN DEFAULT FALSE,
    fee_waiver_reason TEXT,
    
    -- Follow-up
    requires_follow_up BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    follow_up_notes TEXT,
    
    -- Compliance tracking
    regulatory_deadline DATE,
    escalation_required BOOLEAN DEFAULT FALSE,
    escalation_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- HIPAA disclosures accounting
CREATE TABLE hipaa_disclosures (
    disclosure_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Disclosure details
    disclosure_date DATE NOT NULL,
    recipient_name VARCHAR(200) NOT NULL,
    recipient_organization VARCHAR(200),
    recipient_address TEXT,
    
    -- Information disclosed
    information_disclosed TEXT NOT NULL,
    data_categories TEXT[],
    purpose_of_disclosure TEXT NOT NULL,
    
    -- Legal basis
    legal_basis VARCHAR(100) NOT NULL, -- 'patient_consent', 'treatment', 'payment', 'healthcare_operations', 'legal_requirement'
    authorization_number VARCHAR(100),
    court_order_number VARCHAR(100),
    
    -- Scope and limitations
    date_range_start DATE,
    date_range_end DATE,
    specific_restrictions TEXT,
    
    -- Method of disclosure
    disclosure_method VARCHAR(50), -- 'secure_email', 'fax', 'mail', 'portal', 'in_person', 'phone'
    encryption_used BOOLEAN DEFAULT TRUE,
    tracking_number VARCHAR(100),
    
    -- Requester information
    requester_name VARCHAR(200),
    requester_title VARCHAR(100),
    request_date DATE,
    urgency_level VARCHAR(20) DEFAULT 'routine',
    
    -- Authorization details
    authorized_by UUID REFERENCES users(user_id),
    authorization_date DATE,
    patient_authorization_obtained BOOLEAN DEFAULT FALSE,
    
    -- Compliance and follow-up
    minimum_necessary_standard_applied BOOLEAN DEFAULT TRUE,
    patient_notification_required BOOLEAN DEFAULT FALSE,
    patient_notified BOOLEAN DEFAULT FALSE,
    notification_date DATE,
    
    -- Record keeping
    retention_period_years INTEGER DEFAULT 6,
    disposal_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Security incidents and breach management
CREATE TABLE security_incidents (
    incident_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Incident identification
    incident_number VARCHAR(100) UNIQUE NOT NULL,
    incident_type VARCHAR(50) NOT NULL, -- 'breach', 'unauthorized_access', 'system_failure', 'malware', 'phishing'
    severity_level VARCHAR(20) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    
    -- Discovery and reporting
    discovered_date TIMESTAMP WITH TIME ZONE NOT NULL,
    discovered_by UUID REFERENCES users(user_id),
    discovery_method VARCHAR(100),
    reported_date TIMESTAMP WITH TIME ZONE,
    reported_by UUID REFERENCES users(user_id),
    
    -- Incident details
    description TEXT NOT NULL,
    affected_systems TEXT[],
    attack_vector VARCHAR(100),
    suspected_cause TEXT,
    
    -- Impact assessment
    users_affected INTEGER DEFAULT 0,
    records_affected INTEGER DEFAULT 0,
    data_types_affected TEXT[],
    phi_involved BOOLEAN DEFAULT FALSE,
    financial_impact DECIMAL(12,2),
    
    -- Timeline
    incident_start_time TIMESTAMP WITH TIME ZONE,
    incident_end_time TIMESTAMP WITH TIME ZONE,
    containment_time TIMESTAMP WITH TIME ZONE,
    resolution_time TIMESTAMP WITH TIME ZONE,
    
    -- Response actions
    immediate_actions_taken TEXT[],
    containment_measures TEXT[],
    eradication_steps TEXT[],
    recovery_procedures TEXT[],
    
    -- Investigation
    investigation_assigned_to UUID REFERENCES users(user_id),
    investigation_status VARCHAR(50) DEFAULT 'open',
    forensic_analysis_required BOOLEAN DEFAULT FALSE,
    external_investigators_involved BOOLEAN DEFAULT FALSE,
    
    -- Notifications and reporting
    regulatory_notification_required BOOLEAN DEFAULT FALSE,
    regulatory_notification_date DATE,
    patient_notification_required BOOLEAN DEFAULT FALSE,
    patient_notification_date DATE,
    media_attention BOOLEAN DEFAULT FALSE,
    law_enforcement_contacted BOOLEAN DEFAULT FALSE,
    
    -- Risk assessment
    likelihood_of_compromise VARCHAR(20), -- 'low', 'medium', 'high'
    risk_to_individuals VARCHAR(20),
    nature_of_information TEXT,
    
    -- Lessons learned
    lessons_learned TEXT,
    preventive_measures TEXT[],
    policy_changes_needed TEXT[],
    training_requirements TEXT[],
    
    -- Case management
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'investigating', 'contained', 'resolved', 'closed'
    assigned_investigator UUID REFERENCES users(user_id),
    case_closed_date DATE,
    case_closure_reason TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_users_affected_non_negative CHECK (users_affected >= 0),
    CONSTRAINT chk_records_affected_non_negative CHECK (records_affected >= 0)
);

-- Compliance assessments and audits
CREATE TABLE compliance_assessments (
    assessment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Assessment details
    assessment_name VARCHAR(200) NOT NULL,
    assessment_type VARCHAR(50) NOT NULL, -- 'internal_audit', 'external_audit', 'self_assessment', 'regulatory_review'
    regulatory_framework VARCHAR(100) NOT NULL, -- 'HIPAA', 'GDPR', 'SOC2', 'HITECH', 'state_regulations'
    
    -- Scope and timing
    scope_description TEXT,
    assessment_period_start DATE NOT NULL,
    assessment_period_end DATE NOT NULL,
    areas_assessed TEXT[],
    
    -- Conducting party
    conducted_by VARCHAR(200), -- Internal team or external auditor
    lead_assessor VARCHAR(200),
    assessment_team TEXT[],
    
    -- Methodology
    assessment_methodology VARCHAR(100),
    standards_used TEXT[],
    testing_procedures TEXT[],
    sample_size INTEGER,
    
    -- Findings
    total_findings INTEGER DEFAULT 0,
    critical_findings INTEGER DEFAULT 0,
    high_findings INTEGER DEFAULT 0,
    medium_findings INTEGER DEFAULT 0,
    low_findings INTEGER DEFAULT 0,
    
    -- Overall results
    overall_compliance_rating VARCHAR(50), -- 'compliant', 'substantially_compliant', 'non_compliant'
    compliance_percentage DECIMAL(5,2),
    risk_rating VARCHAR(20), -- 'low', 'medium', 'high', 'critical'
    
    -- Reporting
    final_report_date DATE,
    report_delivered_date DATE,
    report_recipients TEXT[],
    executive_summary TEXT,
    
    -- Follow-up
    corrective_action_plan_required BOOLEAN DEFAULT FALSE,
    corrective_action_deadline DATE,
    follow_up_assessment_scheduled BOOLEAN DEFAULT FALSE,
    follow_up_assessment_date DATE,
    
    -- Administrative
    initiated_by UUID REFERENCES users(user_id),
    approved_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Data access logs for compliance monitoring
CREATE TABLE data_access_logs (
    access_log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Access details
    user_id UUID REFERENCES users(user_id),
    accessed_user_id UUID REFERENCES users(user_id), -- Whose data was accessed
    access_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    session_id UUID,
    
    -- System information
    ip_address INET,
    user_agent TEXT,
    access_method VARCHAR(50), -- 'web', 'mobile_app', 'api', 'direct_database'
    
    -- Data accessed
    table_name VARCHAR(100),
    record_id UUID,
    data_categories TEXT[],
    phi_accessed BOOLEAN DEFAULT FALSE,
    sensitive_data_accessed BOOLEAN DEFAULT FALSE,
    
    -- Access type
    action_type VARCHAR(50), -- 'view', 'create', 'update', 'delete', 'export', 'print'
    access_purpose VARCHAR(100), -- 'treatment', 'payment', 'operations', 'research', 'quality_improvement'
    
    -- Authorization
    authorization_level VARCHAR(50),
    minimum_necessary_applied BOOLEAN DEFAULT TRUE,
    supervisor_approval UUID REFERENCES users(user_id),
    
    -- Context
    business_justification TEXT,
    patient_relationship VARCHAR(50), -- 'assigned_patient', 'emergency_access', 'covering_provider'
    emergency_access BOOLEAN DEFAULT FALSE,
    
    -- Break glass access
    break_glass_access BOOLEAN DEFAULT FALSE,
    break_glass_reason TEXT,
    break_glass_approved_by UUID REFERENCES users(user_id),
    
    -- Geographic information
    access_location VARCHAR(200),
    country_code VARCHAR(2),
    
    -- Compliance flags
    suspicious_activity BOOLEAN DEFAULT FALSE,
    policy_violation BOOLEAN DEFAULT FALSE,
    requires_review BOOLEAN DEFAULT FALSE,
    reviewed BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Training and awareness tracking
CREATE TABLE compliance_training (
    training_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Training details
    training_name VARCHAR(200) NOT NULL,
    training_type VARCHAR(50), -- 'hipaa', 'privacy', 'security', 'breach_response', 'data_handling'
    training_provider VARCHAR(200),
    training_format VARCHAR(50), -- 'online', 'in_person', 'video', 'document'
    
    -- Content information
    training_version VARCHAR(20),
    training_content_summary TEXT,
    learning_objectives TEXT[],
    
    -- Completion tracking
    assigned_date DATE NOT NULL,
    due_date DATE NOT NULL,
    started_date DATE,
    completed_date DATE,
    status VARCHAR(50) DEFAULT 'assigned', -- 'assigned', 'in_progress', 'completed', 'overdue', 'exempted'
    
    -- Assessment results
    assessment_required BOOLEAN DEFAULT TRUE,
    assessment_score INTEGER, -- Percentage
    passing_score INTEGER DEFAULT 80,
    assessment_passed BOOLEAN DEFAULT FALSE,
    attempts_allowed INTEGER DEFAULT 3,
    attempts_used INTEGER DEFAULT 0,
    
    -- Certification
    certificate_issued BOOLEAN DEFAULT FALSE,
    certificate_number VARCHAR(100),
    certificate_expiration_date DATE,
    
    -- Compliance requirements
    mandatory BOOLEAN DEFAULT TRUE,
    regulatory_requirement BOOLEAN DEFAULT TRUE,
    recurring_training BOOLEAN DEFAULT TRUE,
    recurrence_interval_months INTEGER DEFAULT 12,
    
    -- Administrative
    assigned_by UUID REFERENCES users(user_id),
    completion_verified_by UUID REFERENCES users(user_id),
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance and compliance queries
CREATE INDEX idx_user_consents_user_type ON user_consents(user_id, consent_type);
CREATE INDEX idx_user_consents_status ON user_consents(consent_status);
CREATE INDEX idx_privacy_requests_user_type ON privacy_requests(user_id, request_type);
CREATE INDEX idx_hipaa_disclosures_user_date ON hipaa_disclosures(user_id, disclosure_date);
CREATE INDEX idx_security_incidents_severity ON security_incidents(severity_level, status);
CREATE INDEX idx_data_access_logs_user_timestamp ON data_access_logs(accessed_user_id, access_timestamp);
CREATE INDEX idx_data_access_logs_phi ON data_access_logs(phi_accessed, access_timestamp) WHERE phi_accessed = TRUE;
CREATE INDEX idx_compliance_training_user_status ON compliance_training(user_id, status);

-- Row Level Security
ALTER TABLE user_consents ENABLE ROW LEVEL SECURITY;
ALTER TABLE privacy_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE hipaa_disclosures ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_access_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_training ENABLE ROW LEVEL SECURITY;

-- Triggers for automated timestamp updates
CREATE TRIGGER update_data_retention_policies_updated_at
    BEFORE UPDATE ON data_retention_policies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_consents_updated_at
    BEFORE UPDATE ON user_consents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_privacy_requests_updated_at
    BEFORE UPDATE ON privacy_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_hipaa_disclosures_updated_at
    BEFORE UPDATE ON hipaa_disclosures
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_security_incidents_updated_at
    BEFORE UPDATE ON security_incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_compliance_assessments_updated_at
    BEFORE UPDATE ON compliance_assessments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_compliance_training_updated_at
    BEFORE UPDATE ON compliance_training
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE data_retention_policies IS 'Data retention policies and disposal schedules for regulatory compliance';
COMMENT ON TABLE user_consents IS 'User consent management for various data uses and treatments';
COMMENT ON TABLE privacy_requests IS 'Privacy rights requests including access, deletion, and rectification';
COMMENT ON TABLE hipaa_disclosures IS 'Accounting of disclosures for HIPAA compliance';
COMMENT ON TABLE security_incidents IS 'Security incident and breach management';
COMMENT ON TABLE compliance_assessments IS 'Compliance audits and assessment tracking';
COMMENT ON TABLE data_access_logs IS 'Detailed logs of data access for audit and compliance';
COMMENT ON TABLE compliance_training IS 'Training and awareness programs for compliance requirements';
