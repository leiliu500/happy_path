-- Insurance and Billing Schema
-- Handles insurance verification, claims processing, billing, and financial management

-- Insurance types
CREATE TYPE insurance_type AS ENUM (
    'health_maintenance_organization',  -- HMO
    'preferred_provider_organization',  -- PPO
    'exclusive_provider_organization',  -- EPO
    'point_of_service',                -- POS
    'high_deductible_health_plan',     -- HDHP
    'medicare',
    'medicaid',
    'tricare',
    'va_benefits',
    'workers_compensation',
    'self_pay',
    'employee_assistance_program',      -- EAP
    'other'
);

-- Claim status
CREATE TYPE claim_status AS ENUM (
    'draft',
    'submitted',
    'pending',
    'under_review',
    'approved',
    'partially_approved',
    'denied',
    'rejected',
    'resubmitted',
    'paid',
    'write_off'
);

-- Payment status
CREATE TYPE payment_status AS ENUM (
    'pending',
    'processing',
    'completed',
    'failed',
    'refunded',
    'disputed',
    'cancelled'
);

-- Billing status
CREATE TYPE billing_status AS ENUM (
    'not_billed',
    'ready_to_bill',
    'billed',
    'paid',
    'past_due',
    'collections',
    'write_off',
    'adjustment'
);

-- Insurance plans and coverage
CREATE TABLE insurance_plans (
    plan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Plan identification
    plan_name VARCHAR(200) NOT NULL,
    insurance_company VARCHAR(200) NOT NULL,
    plan_type insurance_type NOT NULL,
    group_number VARCHAR(100),
    
    -- Plan details
    effective_date DATE NOT NULL,
    termination_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Coverage details
    mental_health_coverage BOOLEAN DEFAULT TRUE,
    substance_abuse_coverage BOOLEAN DEFAULT TRUE,
    telehealth_coverage BOOLEAN DEFAULT TRUE,
    
    -- Benefit structure
    annual_deductible DECIMAL(10,2),
    annual_out_of_pocket_max DECIMAL(10,2),
    copay_amount DECIMAL(8,2),
    coinsurance_percentage DECIMAL(5,2),
    
    -- Session limits
    annual_session_limit INTEGER,
    lifetime_session_limit INTEGER,
    session_rollover_allowed BOOLEAN DEFAULT FALSE,
    
    -- Authorization requirements
    requires_prior_authorization BOOLEAN DEFAULT FALSE,
    requires_referral BOOLEAN DEFAULT FALSE,
    pre_certification_required BOOLEAN DEFAULT FALSE,
    
    -- Provider network
    network_name VARCHAR(200),
    out_of_network_benefits BOOLEAN DEFAULT FALSE,
    out_of_network_deductible DECIMAL(10,2),
    out_of_network_coinsurance DECIMAL(5,2),
    
    -- Billing and claims
    claims_submission_method VARCHAR(50), -- 'electronic', 'paper', 'portal'
    claims_address TEXT,
    electronic_payer_id VARCHAR(50),
    
    -- Contact information
    customer_service_phone VARCHAR(20),
    provider_services_phone VARCHAR(20),
    website_url VARCHAR(500),
    
    -- Administrative
    created_by UUID REFERENCES users(user_id),
    last_verified_date DATE,
    verification_source VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_deductible_positive CHECK (annual_deductible IS NULL OR annual_deductible >= 0),
    CONSTRAINT chk_out_of_pocket_positive CHECK (annual_out_of_pocket_max IS NULL OR annual_out_of_pocket_max >= 0),
    CONSTRAINT chk_coinsurance_range CHECK (coinsurance_percentage IS NULL OR (coinsurance_percentage >= 0 AND coinsurance_percentage <= 100))
);

-- User insurance information
CREATE TABLE user_insurance (
    user_insurance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES insurance_plans(plan_id),
    
    -- Member information
    member_id VARCHAR(100) NOT NULL,
    group_id VARCHAR(100),
    subscriber_name VARCHAR(200),
    relationship_to_subscriber VARCHAR(50), -- 'self', 'spouse', 'child', 'dependent'
    
    -- Coverage dates
    coverage_start_date DATE NOT NULL,
    coverage_end_date DATE,
    is_primary_insurance BOOLEAN DEFAULT TRUE,
    
    -- Benefit details (user-specific)
    annual_deductible_remaining DECIMAL(10,2),
    annual_out_of_pocket_remaining DECIMAL(10,2),
    sessions_used_current_year INTEGER DEFAULT 0,
    sessions_remaining_current_year INTEGER,
    
    -- Authorization information
    current_authorization_number VARCHAR(100),
    authorization_start_date DATE,
    authorization_end_date DATE,
    authorized_sessions_remaining INTEGER,
    
    -- Eligibility verification
    last_eligibility_check DATE,
    eligibility_status VARCHAR(50), -- 'active', 'inactive', 'unknown'
    eligibility_notes TEXT,
    
    -- Co-payments and financial responsibility
    copay_amount DECIMAL(8,2),
    coinsurance_percentage DECIMAL(5,2),
    patient_responsibility_percentage DECIMAL(5,2),
    
    -- Claims and billing preferences
    send_eob_to_patient BOOLEAN DEFAULT TRUE,
    patient_billing_address TEXT,
    billing_contact_phone VARCHAR(20),
    
    -- Status and management
    is_active BOOLEAN DEFAULT TRUE,
    verification_required BOOLEAN DEFAULT FALSE,
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_sessions_positive CHECK (
        (sessions_used_current_year IS NULL OR sessions_used_current_year >= 0) AND
        (sessions_remaining_current_year IS NULL OR sessions_remaining_current_year >= 0) AND
        (authorized_sessions_remaining IS NULL OR authorized_sessions_remaining >= 0)
    )
);

-- Service codes and pricing
CREATE TABLE service_codes (
    service_code_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Code identification
    cpt_code VARCHAR(10) NOT NULL UNIQUE, -- Current Procedural Terminology
    hcpcs_code VARCHAR(10), -- Healthcare Common Procedure Coding System
    description TEXT NOT NULL,
    
    -- Service details
    service_category VARCHAR(100), -- 'psychotherapy', 'evaluation', 'testing', 'consultation'
    service_type VARCHAR(100), -- 'individual', 'group', 'family', 'crisis'
    typical_duration_minutes INTEGER,
    
    -- Billing information
    default_charge_amount DECIMAL(10,2) NOT NULL,
    Medicare_allowable_amount DECIMAL(10,2),
    medicaid_allowable_amount DECIMAL(10,2),
    
    -- Usage and requirements
    requires_diagnosis BOOLEAN DEFAULT TRUE,
    requires_prior_authorization BOOLEAN DEFAULT FALSE,
    billable_to_insurance BOOLEAN DEFAULT TRUE,
    
    -- Modifiers and add-ons
    common_modifiers TEXT[], -- ['-GT', '-95', '-HQ']
    add_on_codes TEXT[], -- Additional codes that can be billed with this service
    
    -- Validity
    effective_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Administrative
    created_by UUID REFERENCES users(user_id),
    last_reviewed_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_charge_amount_positive CHECK (default_charge_amount > 0),
    CONSTRAINT chk_duration_positive CHECK (typical_duration_minutes IS NULL OR typical_duration_minutes > 0)
);

-- Billing encounters/sessions
CREATE TABLE billing_encounters (
    encounter_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    provider_id UUID REFERENCES healthcare_providers(provider_id),
    
    -- Encounter details
    service_date DATE NOT NULL,
    service_start_time TIME,
    service_end_time TIME,
    service_code_id UUID NOT NULL REFERENCES service_codes(service_code_id),
    
    -- Clinical information
    primary_diagnosis_code VARCHAR(20), -- ICD-10
    secondary_diagnosis_codes TEXT[],
    treatment_notes TEXT,
    
    -- Service specifics
    session_type VARCHAR(50), -- 'initial', 'followup', 'crisis', 'group'
    session_duration_minutes INTEGER,
    service_location VARCHAR(100), -- 'office', 'telehealth', 'home', 'hospital'
    
    -- Billing information
    charge_amount DECIMAL(10,2) NOT NULL,
    allowed_amount DECIMAL(10,2),
    copay_collected DECIMAL(8,2) DEFAULT 0,
    patient_responsibility DECIMAL(10,2),
    
    -- Insurance and authorization
    user_insurance_id UUID REFERENCES user_insurance(user_insurance_id),
    authorization_number VARCHAR(100),
    requires_prior_auth BOOLEAN DEFAULT FALSE,
    prior_auth_obtained BOOLEAN DEFAULT FALSE,
    
    -- Status tracking
    billing_status billing_status NOT NULL DEFAULT 'not_billed',
    billed_date DATE,
    claim_submission_date DATE,
    
    -- Modifiers and adjustments
    service_modifiers TEXT[],
    billing_notes TEXT,
    write_off_amount DECIMAL(10,2) DEFAULT 0,
    adjustment_amount DECIMAL(10,2) DEFAULT 0,
    adjustment_reason TEXT,
    
    -- Quality assurance
    reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by UUID REFERENCES users(user_id),
    review_date DATE,
    review_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_charge_amount_positive CHECK (charge_amount > 0),
    CONSTRAINT chk_copay_non_negative CHECK (copay_collected >= 0),
    CONSTRAINT chk_session_times CHECK (service_end_time IS NULL OR service_start_time IS NULL OR service_start_time < service_end_time)
);

-- Insurance claims
CREATE TABLE insurance_claims (
    claim_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    encounter_id UUID NOT NULL REFERENCES billing_encounters(encounter_id),
    user_insurance_id UUID NOT NULL REFERENCES user_insurance(user_insurance_id),
    
    -- Claim identification
    claim_number VARCHAR(100) UNIQUE,
    original_claim_id UUID REFERENCES insurance_claims(claim_id), -- For resubmissions
    
    -- Submission details
    submission_date DATE NOT NULL,
    submission_method VARCHAR(50), -- 'electronic', 'paper', 'portal'
    clearinghouse VARCHAR(100),
    batch_number VARCHAR(50),
    
    -- Claim amounts
    billed_amount DECIMAL(10,2) NOT NULL,
    allowed_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    adjustment_amount DECIMAL(10,2) DEFAULT 0,
    patient_responsibility DECIMAL(10,2),
    
    -- Status and processing
    claim_status claim_status NOT NULL DEFAULT 'submitted',
    status_date DATE DEFAULT CURRENT_DATE,
    processing_time_days INTEGER,
    
    -- Insurance response
    explanation_of_benefits TEXT,
    denial_reason TEXT,
    denial_code VARCHAR(20),
    appeal_deadline DATE,
    
    -- Resubmission tracking
    resubmission_count INTEGER DEFAULT 0,
    last_resubmission_date DATE,
    max_resubmissions_reached BOOLEAN DEFAULT FALSE,
    
    -- Payment information
    check_number VARCHAR(100),
    payment_date DATE,
    remittance_advice TEXT,
    
    -- Appeals and disputes
    appeal_filed BOOLEAN DEFAULT FALSE,
    appeal_date DATE,
    appeal_outcome VARCHAR(50),
    appeal_notes TEXT,
    
    -- Administrative
    processed_by UUID REFERENCES users(user_id),
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_billed_amount_positive CHECK (billed_amount > 0),
    CONSTRAINT chk_amounts_non_negative CHECK (
        (allowed_amount IS NULL OR allowed_amount >= 0) AND
        (paid_amount IS NULL OR paid_amount >= 0) AND
        (adjustment_amount >= 0) AND
        (patient_responsibility IS NULL OR patient_responsibility >= 0)
    ),
    CONSTRAINT chk_resubmission_count_non_negative CHECK (resubmission_count >= 0)
);

-- Patient payments and billing
CREATE TABLE patient_billing (
    billing_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    encounter_id UUID REFERENCES billing_encounters(encounter_id),
    
    -- Billing details
    billing_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    amount_owed DECIMAL(10,2) NOT NULL,
    
    -- Billing breakdown
    service_charges DECIMAL(10,2) NOT NULL,
    copay_amount DECIMAL(8,2) DEFAULT 0,
    coinsurance_amount DECIMAL(10,2) DEFAULT 0,
    deductible_amount DECIMAL(10,2) DEFAULT 0,
    previous_balance DECIMAL(10,2) DEFAULT 0,
    
    -- Payment tracking
    amount_paid DECIMAL(10,2) DEFAULT 0,
    balance_remaining DECIMAL(10,2) NOT NULL,
    last_payment_date DATE,
    payment_plan_id UUID, -- Reference to payment plans if implemented
    
    -- Status
    billing_status billing_status NOT NULL DEFAULT 'not_billed',
    payment_status payment_status DEFAULT 'pending',
    is_overdue BOOLEAN DEFAULT FALSE,
    days_overdue INTEGER DEFAULT 0,
    
    -- Collection and financial assistance
    sent_to_collections BOOLEAN DEFAULT FALSE,
    collections_date DATE,
    financial_assistance_applied BOOLEAN DEFAULT FALSE,
    hardship_discount_percentage DECIMAL(5,2),
    
    -- Communication
    statements_sent INTEGER DEFAULT 0,
    last_statement_date DATE,
    patient_contacted BOOLEAN DEFAULT FALSE,
    contact_attempts INTEGER DEFAULT 0,
    
    -- Administrative
    notes TEXT,
    created_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_billing_amounts_positive CHECK (
        amount_owed >= 0 AND
        service_charges >= 0 AND
        copay_amount >= 0 AND
        coinsurance_amount >= 0 AND
        deductible_amount >= 0 AND
        amount_paid >= 0 AND
        balance_remaining >= 0
    ),
    CONSTRAINT chk_hardship_discount_range CHECK (hardship_discount_percentage IS NULL OR (hardship_discount_percentage >= 0 AND hardship_discount_percentage <= 100))
);

-- Payment transactions
CREATE TABLE payment_transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    billing_id UUID REFERENCES patient_billing(billing_id),
    
    -- Transaction details
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
    transaction_time TIME DEFAULT CURRENT_TIME,
    amount DECIMAL(10,2) NOT NULL,
    
    -- Payment method
    payment_method VARCHAR(50) NOT NULL, -- 'credit_card', 'debit_card', 'bank_transfer', 'check', 'cash', 'money_order'
    payment_processor VARCHAR(100), -- 'stripe', 'square', 'paypal', etc.
    
    -- Transaction identification
    transaction_reference VARCHAR(200),
    confirmation_number VARCHAR(100),
    authorization_code VARCHAR(50),
    
    -- Payment details
    card_last_four VARCHAR(4),
    payment_source_type VARCHAR(50), -- 'visa', 'mastercard', 'checking', 'savings'
    
    -- Status
    payment_status payment_status NOT NULL DEFAULT 'processing',
    processing_fee DECIMAL(8,2) DEFAULT 0,
    net_amount DECIMAL(10,2),
    
    -- Refunds and reversals
    refunded BOOLEAN DEFAULT FALSE,
    refund_amount DECIMAL(10,2),
    refund_date DATE,
    refund_reason TEXT,
    
    -- Failure handling
    failure_reason TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Administrative
    processed_by UUID REFERENCES users(user_id),
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_payment_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_processing_fee_non_negative CHECK (processing_fee >= 0),
    CONSTRAINT chk_refund_amount_valid CHECK (refund_amount IS NULL OR (refund_amount >= 0 AND refund_amount <= amount))
);

-- Financial reporting and analytics
CREATE TABLE financial_reporting (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Report details
    report_name VARCHAR(200) NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- 'revenue', 'collections', 'aging', 'payer_mix', 'productivity'
    report_period_start DATE NOT NULL,
    report_period_end DATE NOT NULL,
    
    -- Financial metrics
    total_charges DECIMAL(12,2),
    total_payments DECIMAL(12,2),
    total_adjustments DECIMAL(12,2),
    net_revenue DECIMAL(12,2),
    accounts_receivable DECIMAL(12,2),
    
    -- Performance indicators
    collection_rate DECIMAL(5,2), -- Percentage
    days_in_ar DECIMAL(6,2), -- Average days in accounts receivable
    denial_rate DECIMAL(5,2),
    bad_debt_rate DECIMAL(5,2),
    
    -- Volume metrics
    total_encounters INTEGER,
    unique_patients INTEGER,
    average_charge_per_encounter DECIMAL(10,2),
    
    -- Payer mix
    commercial_percentage DECIMAL(5,2),
    medicare_percentage DECIMAL(5,2),
    medicaid_percentage DECIMAL(5,2),
    self_pay_percentage DECIMAL(5,2),
    
    -- Report generation
    generated_by UUID REFERENCES users(user_id),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    report_data JSONB, -- Detailed breakdown data
    
    -- Distribution
    distributed_to UUID[],
    distribution_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_user_insurance_user_id ON user_insurance(user_id);
CREATE INDEX idx_billing_encounters_user_date ON billing_encounters(user_id, service_date);
CREATE INDEX idx_billing_encounters_provider ON billing_encounters(provider_id);
CREATE INDEX idx_insurance_claims_status ON insurance_claims(claim_status);
CREATE INDEX idx_patient_billing_user_status ON patient_billing(user_id, billing_status);
CREATE INDEX idx_payment_transactions_user_date ON payment_transactions(user_id, transaction_date);

-- Row Level Security
ALTER TABLE user_insurance ENABLE ROW LEVEL SECURITY;
ALTER TABLE billing_encounters ENABLE ROW LEVEL SECURITY;
ALTER TABLE insurance_claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE patient_billing ENABLE ROW LEVEL SECURITY;
ALTER TABLE payment_transactions ENABLE ROW LEVEL SECURITY;

-- Triggers for automated timestamp updates
CREATE TRIGGER update_insurance_plans_updated_at
    BEFORE UPDATE ON insurance_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_insurance_updated_at
    BEFORE UPDATE ON user_insurance
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_service_codes_updated_at
    BEFORE UPDATE ON service_codes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_billing_encounters_updated_at
    BEFORE UPDATE ON billing_encounters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_insurance_claims_updated_at
    BEFORE UPDATE ON insurance_claims
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_billing_updated_at
    BEFORE UPDATE ON patient_billing
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payment_transactions_updated_at
    BEFORE UPDATE ON payment_transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE insurance_plans IS 'Insurance plan details and coverage information';
COMMENT ON TABLE user_insurance IS 'User-specific insurance coverage and benefit tracking';
COMMENT ON TABLE service_codes IS 'CPT/HCPCS codes and pricing for billable services';
COMMENT ON TABLE billing_encounters IS 'Individual service encounters and billing information';
COMMENT ON TABLE insurance_claims IS 'Insurance claim submissions and processing';
COMMENT ON TABLE patient_billing IS 'Patient billing statements and account management';
COMMENT ON TABLE payment_transactions IS 'Payment processing and transaction records';
COMMENT ON TABLE financial_reporting IS 'Financial reports and analytics';
