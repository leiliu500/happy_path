-- Care Coordination and Provider Network Schema
-- Handles healthcare provider network, referrals, care teams, and inter-provider communication

-- Provider types
CREATE TYPE provider_type AS ENUM (
    'psychiatrist',
    'psychologist',
    'licensed_therapist',
    'social_worker',
    'psychiatric_nurse',
    'primary_care_physician',
    'peer_support_specialist',
    'case_manager',
    'crisis_counselor',
    'substance_abuse_counselor',
    'marriage_family_therapist',
    'group_therapist',
    'art_music_therapist',
    'occupational_therapist',
    'other_specialist'
);

-- Provider specialties
CREATE TYPE provider_specialty AS ENUM (
    'adult_psychiatry',
    'child_adolescent_psychiatry',
    'geriatric_psychiatry',
    'addiction_psychiatry',
    'forensic_psychiatry',
    'trauma_ptsd',
    'eating_disorders',
    'mood_disorders',
    'anxiety_disorders',
    'personality_disorders',
    'psychotic_disorders',
    'autism_spectrum',
    'adhd',
    'grief_bereavement',
    'couples_therapy',
    'family_therapy',
    'group_therapy',
    'lgbtq_issues',
    'cultural_specific',
    'pain_management',
    'sleep_disorders'
);

-- License status
CREATE TYPE license_status AS ENUM (
    'active',
    'inactive',
    'suspended',
    'revoked',
    'pending',
    'expired'
);

-- Care team roles
CREATE TYPE care_team_role AS ENUM (
    'primary_therapist',
    'psychiatrist',
    'primary_care_physician',
    'case_manager',
    'peer_support',
    'family_member',
    'emergency_contact',
    'supervisor',
    'consultant',
    'other'
);

-- Referral status
CREATE TYPE referral_status AS ENUM (
    'pending',
    'accepted',
    'declined',
    'completed',
    'cancelled',
    'expired'
);

-- Healthcare providers registry
CREATE TABLE healthcare_providers (
    provider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Basic information
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    title VARCHAR(50), -- 'Dr.', 'LCSW', 'LMFT', etc.
    suffix VARCHAR(20), -- 'MD', 'PhD', 'LCSW', etc.
    
    -- Professional identification
    npi_number VARCHAR(20) UNIQUE, -- National Provider Identifier
    state_license_number VARCHAR(50),
    license_state VARCHAR(2),
    license_status license_status NOT NULL DEFAULT 'active',
    license_expiration_date DATE,
    
    -- Contact information
    phone_number VARCHAR(20),
    email VARCHAR(255),
    website_url VARCHAR(500),
    
    -- Professional details
    provider_type provider_type NOT NULL,
    specialties provider_specialty[],
    board_certifications TEXT[],
    years_experience INTEGER,
    education_background TEXT[],
    
    -- Practice information
    practice_name VARCHAR(200),
    practice_type VARCHAR(50), -- 'private_practice', 'hospital', 'clinic', 'telehealth_only'
    
    -- Address information
    address_line1 VARCHAR(200),
    address_line2 VARCHAR(200),
    city VARCHAR(100),
    state_province VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'United States',
    
    -- Service details
    services_offered TEXT[],
    treatment_approaches TEXT[], -- 'CBT', 'DBT', 'EMDR', etc.
    languages_spoken TEXT[] DEFAULT '{"English"}',
    cultural_competencies TEXT[],
    
    -- Availability and logistics
    telehealth_available BOOLEAN DEFAULT TRUE,
    in_person_available BOOLEAN DEFAULT TRUE,
    accepts_new_patients BOOLEAN DEFAULT TRUE,
    wait_list_available BOOLEAN DEFAULT FALSE,
    average_wait_time_days INTEGER,
    
    -- Insurance and billing
    accepts_insurance BOOLEAN DEFAULT TRUE,
    insurance_plans_accepted TEXT[],
    sliding_scale_available BOOLEAN DEFAULT FALSE,
    self_pay_rates JSONB, -- {"initial": 200, "followup": 150}
    
    -- Quality and ratings
    overall_rating DECIMAL(3,2), -- 1-5 stars
    total_reviews INTEGER DEFAULT 0,
    verified_provider BOOLEAN DEFAULT FALSE,
    
    -- Platform integration
    platform_user_id UUID REFERENCES users(user_id), -- If provider is also a platform user
    is_active_on_platform BOOLEAN DEFAULT FALSE,
    integration_level VARCHAR(50), -- 'basic', 'full', 'premium'
    
    -- Compliance and verification
    background_check_date DATE,
    malpractice_insurance BOOLEAN DEFAULT FALSE,
    hipaa_compliant BOOLEAN DEFAULT TRUE,
    last_verification_date DATE,
    verified_by UUID REFERENCES users(user_id),
    
    -- Network participation
    network_status VARCHAR(50) DEFAULT 'in_network', -- 'in_network', 'out_of_network', 'preferred'
    credentialing_date DATE,
    contract_effective_date DATE,
    contract_end_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_years_experience_positive CHECK (years_experience IS NULL OR years_experience >= 0),
    CONSTRAINT chk_wait_time_positive CHECK (average_wait_time_days IS NULL OR average_wait_time_days >= 0),
    CONSTRAINT chk_rating_range CHECK (overall_rating IS NULL OR (overall_rating >= 1 AND overall_rating <= 5))
);

-- Care teams for coordinated care
CREATE TABLE care_teams (
    care_team_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Team metadata
    team_name VARCHAR(200),
    team_description TEXT,
    primary_coordinator_id UUID REFERENCES healthcare_providers(provider_id),
    
    -- Team characteristics
    care_model VARCHAR(50), -- 'collaborative', 'stepped', 'integrated', 'crisis_team'
    specializes_in TEXT[],
    coordination_frequency VARCHAR(50), -- 'weekly', 'biweekly', 'monthly', 'as_needed'
    
    -- Status and management
    is_active BOOLEAN DEFAULT TRUE,
    formation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    last_coordination_meeting DATE,
    next_coordination_meeting DATE,
    
    -- Communication preferences
    preferred_communication_method VARCHAR(50), -- 'secure_message', 'email', 'phone', 'video'
    meeting_platform VARCHAR(100),
    
    -- Patient involvement
    patient_participates BOOLEAN DEFAULT TRUE,
    family_involved BOOLEAN DEFAULT FALSE,
    patient_preferences TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Care team memberships
CREATE TABLE care_team_members (
    member_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    care_team_id UUID NOT NULL REFERENCES care_teams(care_team_id) ON DELETE CASCADE,
    provider_id UUID REFERENCES healthcare_providers(provider_id),
    
    -- Member details
    role care_team_role NOT NULL,
    role_description TEXT,
    is_primary_contact BOOLEAN DEFAULT FALSE,
    
    -- Participation details
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
    leave_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Responsibilities and scope
    responsibilities TEXT[],
    decision_making_authority VARCHAR(50), -- 'full', 'limited', 'advisory'
    emergency_contact BOOLEAN DEFAULT FALSE,
    
    -- Communication settings
    receives_updates BOOLEAN DEFAULT TRUE,
    communication_frequency VARCHAR(50), -- 'immediate', 'daily', 'weekly'
    
    -- Performance tracking
    last_contact_date DATE,
    response_time_hours INTEGER, -- Average response time
    availability_hours JSONB, -- Weekly schedule
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Referrals between providers
CREATE TABLE referrals (
    referral_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    referring_provider_id UUID REFERENCES healthcare_providers(provider_id),
    receiving_provider_id UUID REFERENCES healthcare_providers(provider_id),
    
    -- Referral details
    referral_type VARCHAR(50) NOT NULL, -- 'consultation', 'transfer_care', 'shared_care', 'emergency'
    urgency_level VARCHAR(50) DEFAULT 'routine', -- 'stat', 'urgent', 'routine'
    
    -- Clinical information
    reason_for_referral TEXT NOT NULL,
    clinical_summary TEXT,
    current_diagnoses TEXT[],
    current_medications TEXT[],
    relevant_history TEXT,
    
    -- Specific requests
    services_requested TEXT[],
    questions_for_specialist TEXT,
    preferred_appointment_timeframe VARCHAR(100),
    special_considerations TEXT,
    
    -- Status tracking
    status referral_status NOT NULL DEFAULT 'pending',
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    sent_date DATE,
    received_date DATE,
    appointment_scheduled_date DATE,
    first_appointment_date DATE,
    
    -- Communication
    referral_notes TEXT,
    receiving_provider_response TEXT,
    consultation_summary TEXT,
    recommendations_received TEXT,
    
    -- Follow-up
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    outcome_summary TEXT,
    care_continues_with VARCHAR(50), -- 'referring_provider', 'receiving_provider', 'shared'
    
    -- Patient involvement
    patient_notified BOOLEAN DEFAULT FALSE,
    patient_consent_obtained BOOLEAN DEFAULT FALSE,
    patient_preferences TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Inter-provider communications
CREATE TABLE provider_communications (
    communication_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    sender_provider_id UUID REFERENCES healthcare_providers(provider_id),
    recipient_provider_id UUID REFERENCES healthcare_providers(provider_id),
    
    -- Message details
    subject VARCHAR(200) NOT NULL,
    message_body TEXT NOT NULL,
    message_type VARCHAR(50), -- 'consultation', 'update', 'urgent', 'coordination', 'discharge'
    priority_level VARCHAR(20) DEFAULT 'normal', -- 'low', 'normal', 'high', 'urgent'
    
    -- Clinical context
    related_to_referral_id UUID REFERENCES referrals(referral_id),
    clinical_context VARCHAR(100), -- 'medication_change', 'symptom_change', 'crisis', 'progress_update'
    requires_response BOOLEAN DEFAULT FALSE,
    response_timeframe VARCHAR(50), -- '24_hours', '3_days', '1_week', 'as_convenient'
    
    -- Status and tracking
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP WITH TIME ZONE,
    read_at TIMESTAMP WITH TIME ZONE,
    responded_at TIMESTAMP WITH TIME ZONE,
    
    -- Response and follow-up
    response_message_id UUID REFERENCES provider_communications(communication_id),
    action_required BOOLEAN DEFAULT FALSE,
    action_taken TEXT,
    follow_up_needed BOOLEAN DEFAULT FALSE,
    
    -- Security and compliance
    encrypted BOOLEAN DEFAULT TRUE,
    phi_included BOOLEAN DEFAULT TRUE,
    audit_logged BOOLEAN DEFAULT TRUE,
    
    -- Patient awareness
    patient_copied BOOLEAN DEFAULT FALSE,
    patient_notification_sent BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Care coordination meetings and conferences
CREATE TABLE care_coordination_meetings (
    meeting_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    care_team_id UUID NOT NULL REFERENCES care_teams(care_team_id) ON DELETE CASCADE,
    patient_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Meeting details
    meeting_title VARCHAR(200) NOT NULL,
    meeting_type VARCHAR(50), -- 'routine_review', 'crisis_response', 'treatment_planning', 'discharge_planning'
    meeting_purpose TEXT,
    
    -- Scheduling
    scheduled_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    meeting_platform VARCHAR(100), -- 'in_person', 'zoom', 'teams', 'phone'
    meeting_location VARCHAR(200),
    
    -- Participants
    facilitator_provider_id UUID REFERENCES healthcare_providers(provider_id),
    attendee_provider_ids UUID[],
    patient_attending BOOLEAN DEFAULT TRUE,
    family_attending BOOLEAN DEFAULT FALSE,
    
    -- Agenda and outcomes
    agenda_items TEXT[],
    discussion_points TEXT,
    decisions_made TEXT[],
    action_items TEXT[],
    assigned_responsibilities JSONB, -- {"provider_id": ["action1", "action2"]}
    
    -- Follow-up
    next_meeting_date TIMESTAMP WITH TIME ZONE,
    follow_up_required TEXT[],
    
    -- Documentation
    meeting_notes TEXT,
    confidential_notes TEXT, -- Not shared with patient
    
    -- Status
    meeting_status VARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'completed', 'cancelled', 'rescheduled'
    cancellation_reason TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_duration_positive CHECK (duration_minutes > 0)
);

-- Provider availability and scheduling
CREATE TABLE provider_availability (
    availability_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES healthcare_providers(provider_id) ON DELETE CASCADE,
    
    -- Time slot details
    day_of_week INTEGER NOT NULL, -- 0 = Sunday, 1 = Monday, etc.
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    
    -- Availability type
    appointment_type VARCHAR(50), -- 'new_patient', 'follow_up', 'urgent', 'consultation'
    service_type VARCHAR(50), -- 'telehealth', 'in_person', 'both'
    
    -- Capacity
    max_appointments INTEGER DEFAULT 1,
    appointment_duration_minutes INTEGER DEFAULT 50,
    
    -- Date range
    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    
    -- Special conditions
    is_active BOOLEAN DEFAULT TRUE,
    requires_special_scheduling BOOLEAN DEFAULT FALSE,
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_day_of_week_valid CHECK (day_of_week >= 0 AND day_of_week <= 6),
    CONSTRAINT chk_time_order CHECK (start_time < end_time),
    CONSTRAINT chk_max_appointments_positive CHECK (max_appointments > 0),
    CONSTRAINT chk_duration_positive CHECK (appointment_duration_minutes > 0)
);

-- Network quality metrics
CREATE TABLE provider_quality_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES healthcare_providers(provider_id) ON DELETE CASCADE,
    
    -- Measurement period
    measurement_date DATE NOT NULL,
    measurement_period VARCHAR(50), -- 'monthly', 'quarterly', 'annual'
    
    -- Quality indicators
    patient_satisfaction_score DECIMAL(3,2), -- 1-5 scale
    response_time_hours DECIMAL(6,2),
    appointment_adherence_rate DECIMAL(5,2), -- Percentage
    cancellation_rate DECIMAL(5,2),
    no_show_rate DECIMAL(5,2),
    
    -- Clinical outcomes
    patient_improvement_rate DECIMAL(5,2),
    treatment_completion_rate DECIMAL(5,2),
    crisis_prevention_rate DECIMAL(5,2),
    
    -- Communication metrics
    care_coordination_participation DECIMAL(5,2),
    referral_acceptance_rate DECIMAL(5,2),
    response_to_communications DECIMAL(5,2),
    
    -- Volume metrics
    total_patients_served INTEGER,
    new_patients_this_period INTEGER,
    average_caseload INTEGER,
    
    -- Compliance metrics
    documentation_completeness DECIMAL(5,2),
    billing_accuracy DECIMAL(5,2),
    continuing_education_compliance BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_satisfaction_range CHECK (patient_satisfaction_score IS NULL OR (patient_satisfaction_score >= 1 AND patient_satisfaction_score <= 5)),
    CONSTRAINT chk_percentage_metrics CHECK (
        (appointment_adherence_rate IS NULL OR (appointment_adherence_rate >= 0 AND appointment_adherence_rate <= 100)) AND
        (cancellation_rate IS NULL OR (cancellation_rate >= 0 AND cancellation_rate <= 100)) AND
        (no_show_rate IS NULL OR (no_show_rate >= 0 AND no_show_rate <= 100))
    )
);

-- Indexes for performance
CREATE INDEX idx_healthcare_providers_type_specialty ON healthcare_providers(provider_type, specialties);
CREATE INDEX idx_healthcare_providers_location ON healthcare_providers(city, state_province);
CREATE INDEX idx_care_teams_patient ON care_teams(patient_id);
CREATE INDEX idx_care_team_members_team ON care_team_members(care_team_id);
CREATE INDEX idx_referrals_patient_status ON referrals(patient_id, status);
CREATE INDEX idx_provider_communications_patient ON provider_communications(patient_id);
CREATE INDEX idx_coordination_meetings_team_date ON care_coordination_meetings(care_team_id, scheduled_date_time);
CREATE INDEX idx_provider_availability_provider_day ON provider_availability(provider_id, day_of_week);

-- Row Level Security
ALTER TABLE care_teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE care_team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
ALTER TABLE provider_communications ENABLE ROW LEVEL SECURITY;
ALTER TABLE care_coordination_meetings ENABLE ROW LEVEL SECURITY;

-- Triggers for automated timestamp updates
CREATE TRIGGER update_healthcare_providers_updated_at
    BEFORE UPDATE ON healthcare_providers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_care_teams_updated_at
    BEFORE UPDATE ON care_teams
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_care_team_members_updated_at
    BEFORE UPDATE ON care_team_members
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_referrals_updated_at
    BEFORE UPDATE ON referrals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_care_coordination_meetings_updated_at
    BEFORE UPDATE ON care_coordination_meetings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE healthcare_providers IS 'Registry of healthcare providers in the network';
COMMENT ON TABLE care_teams IS 'Coordinated care teams for comprehensive patient support';
COMMENT ON TABLE care_team_members IS 'Members and roles within care teams';
COMMENT ON TABLE referrals IS 'Referrals between healthcare providers';
COMMENT ON TABLE provider_communications IS 'Secure communications between providers';
COMMENT ON TABLE care_coordination_meetings IS 'Care team meetings and coordination activities';
COMMENT ON TABLE provider_availability IS 'Provider scheduling and availability information';
COMMENT ON TABLE provider_quality_metrics IS 'Quality and performance metrics for providers';
