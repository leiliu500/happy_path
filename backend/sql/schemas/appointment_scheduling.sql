-- Appointment and Scheduling Management Schema
-- Handles appointment booking, scheduling, reminders, and calendar management

-- Appointment types
CREATE TYPE appointment_type AS ENUM (
    'initial_consultation',
    'follow_up',
    'therapy_session',
    'psychiatric_evaluation',
    'medication_management',
    'crisis_intervention',
    'group_therapy',
    'family_therapy',
    'couples_therapy',
    'psychological_testing',
    'telehealth',
    'phone_consultation',
    'check_in',
    'administrative'
);

-- Appointment status
CREATE TYPE appointment_status AS ENUM (
    'scheduled',
    'confirmed',
    'arrived',
    'in_progress',
    'completed',
    'cancelled_by_patient',
    'cancelled_by_provider',
    'no_show',
    'rescheduled',
    'late_cancellation'
);

-- Scheduling preferences
CREATE TYPE scheduling_preference AS ENUM (
    'morning',
    'afternoon',
    'evening',
    'weekend',
    'weekday',
    'flexible'
);

-- Appointment modality
CREATE TYPE appointment_modality AS ENUM (
    'in_person',
    'telehealth',
    'phone',
    'hybrid'
);

-- Reminder types
CREATE TYPE reminder_type AS ENUM (
    'email',
    'sms',
    'phone_call',
    'push_notification',
    'postal_mail'
);

-- Provider calendars and availability
CREATE TABLE provider_calendars (
    calendar_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES healthcare_providers(provider_id) ON DELETE CASCADE,
    
    -- Calendar settings
    calendar_name VARCHAR(200) NOT NULL,
    time_zone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    default_appointment_duration INTEGER DEFAULT 50, -- minutes
    
    -- Availability preferences
    monday_start_time TIME,
    monday_end_time TIME,
    tuesday_start_time TIME,
    tuesday_end_time TIME,
    wednesday_start_time TIME,
    wednesday_end_time TIME,
    thursday_start_time TIME,
    thursday_end_time TIME,
    friday_start_time TIME,
    friday_end_time TIME,
    saturday_start_time TIME,
    saturday_end_time TIME,
    sunday_start_time TIME,
    sunday_end_time TIME,
    
    -- Booking settings
    advance_booking_days INTEGER DEFAULT 30, -- How far in advance patients can book
    minimum_notice_hours INTEGER DEFAULT 24, -- Minimum notice for booking
    buffer_time_minutes INTEGER DEFAULT 10, -- Buffer between appointments
    
    -- Cancellation policy
    cancellation_notice_hours INTEGER DEFAULT 24,
    late_cancellation_fee DECIMAL(8,2),
    no_show_fee DECIMAL(8,2),
    
    -- Auto-scheduling settings
    auto_confirm_appointments BOOLEAN DEFAULT FALSE,
    allow_online_booking BOOLEAN DEFAULT TRUE,
    require_deposit BOOLEAN DEFAULT FALSE,
    deposit_amount DECIMAL(8,2),
    
    -- Telehealth settings
    telehealth_platform VARCHAR(100), -- 'zoom', 'teams', 'doxy', 'custom'
    telehealth_room_url VARCHAR(500),
    telehealth_instructions TEXT,
    
    -- Administrative
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_default_duration_positive CHECK (default_appointment_duration > 0),
    CONSTRAINT chk_advance_booking_positive CHECK (advance_booking_days > 0),
    CONSTRAINT chk_minimum_notice_positive CHECK (minimum_notice_hours >= 0)
);

-- Provider schedule blocks and exceptions
CREATE TABLE provider_schedule_blocks (
    block_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    calendar_id UUID NOT NULL REFERENCES provider_calendars(calendar_id) ON DELETE CASCADE,
    
    -- Block details
    block_title VARCHAR(200) NOT NULL,
    block_type VARCHAR(50) NOT NULL, -- 'available', 'unavailable', 'break', 'meeting', 'vacation', 'holiday'
    
    -- Timing
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    all_day BOOLEAN DEFAULT FALSE,
    
    -- Recurrence pattern
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50), -- 'daily', 'weekly', 'monthly', 'yearly'
    recurrence_interval INTEGER DEFAULT 1,
    days_of_week INTEGER[], -- [1,2,3,4,5] for weekdays
    end_recurrence_date DATE,
    
    -- Appointment settings for available blocks
    appointment_types_allowed appointment_type[],
    max_appointments INTEGER,
    appointment_duration_minutes INTEGER,
    modality_preference appointment_modality,
    
    -- Notes and description
    notes TEXT,
    internal_notes TEXT, -- Not visible to patients
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    cancellation_reason TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_date_order CHECK (start_date <= end_date),
    CONSTRAINT chk_time_order CHECK (all_day = TRUE OR start_time IS NULL OR end_time IS NULL OR start_time < end_time)
);

-- Appointments
CREATE TABLE appointments (
    appointment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    provider_id UUID NOT NULL REFERENCES healthcare_providers(provider_id),
    calendar_id UUID NOT NULL REFERENCES provider_calendars(calendar_id),
    
    -- Appointment details
    appointment_type appointment_type NOT NULL,
    appointment_status appointment_status NOT NULL DEFAULT 'scheduled',
    
    -- Scheduling
    scheduled_date DATE NOT NULL,
    scheduled_start_time TIME NOT NULL,
    scheduled_end_time TIME NOT NULL,
    actual_start_time TIME,
    actual_end_time TIME,
    duration_minutes INTEGER NOT NULL,
    
    -- Modality and location
    modality appointment_modality NOT NULL DEFAULT 'in_person',
    location_name VARCHAR(200),
    room_number VARCHAR(50),
    telehealth_link VARCHAR(500),
    telehealth_meeting_id VARCHAR(200),
    
    -- Clinical context
    chief_complaint TEXT,
    appointment_purpose TEXT,
    treatment_focus TEXT[],
    is_urgent BOOLEAN DEFAULT FALSE,
    clinical_priority VARCHAR(20) DEFAULT 'routine', -- 'routine', 'urgent', 'emergency'
    
    -- Booking information
    booked_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    booked_by UUID REFERENCES users(user_id), -- Who booked the appointment
    booking_method VARCHAR(50), -- 'online', 'phone', 'in_person', 'staff'
    
    -- Series information for recurring appointments
    series_id UUID, -- Groups recurring appointments
    series_instance INTEGER, -- 1st, 2nd, 3rd in series
    
    -- Cancellation and rescheduling
    cancelled_date TIMESTAMP WITH TIME ZONE,
    cancelled_by UUID REFERENCES users(user_id),
    cancellation_reason TEXT,
    cancellation_notice_hours INTEGER,
    
    rescheduled_from_appointment_id UUID REFERENCES appointments(appointment_id),
    rescheduled_to_appointment_id UUID REFERENCES appointments(appointment_id),
    reschedule_count INTEGER DEFAULT 0,
    
    -- No-show tracking
    no_show_date TIMESTAMP WITH TIME ZONE,
    no_show_follow_up_required BOOLEAN DEFAULT FALSE,
    no_show_fee_applied BOOLEAN DEFAULT FALSE,
    
    -- Confirmation and reminders
    confirmation_requested BOOLEAN DEFAULT FALSE,
    confirmation_received BOOLEAN DEFAULT FALSE,
    confirmation_date TIMESTAMP WITH TIME ZONE,
    
    -- Financial information
    copay_amount DECIMAL(8,2),
    copay_collected BOOLEAN DEFAULT FALSE,
    insurance_authorization_required BOOLEAN DEFAULT FALSE,
    authorization_number VARCHAR(100),
    
    -- Special requirements
    interpreter_needed BOOLEAN DEFAULT FALSE,
    interpreter_language VARCHAR(50),
    accessibility_requirements TEXT,
    special_instructions TEXT,
    
    -- Follow-up
    follow_up_appointment_needed BOOLEAN DEFAULT FALSE,
    recommended_follow_up_timeframe VARCHAR(100),
    next_appointment_scheduled BOOLEAN DEFAULT FALSE,
    
    -- Documentation
    appointment_notes TEXT,
    internal_notes TEXT, -- Staff notes not visible to patient
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_scheduled_times CHECK (scheduled_start_time < scheduled_end_time),
    CONSTRAINT chk_duration_positive CHECK (duration_minutes > 0),
    CONSTRAINT chk_actual_times CHECK (actual_start_time IS NULL OR actual_end_time IS NULL OR actual_start_time <= actual_end_time)
);

-- Appointment reminders
CREATE TABLE appointment_reminders (
    reminder_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    
    -- Reminder configuration
    reminder_type reminder_type NOT NULL,
    reminder_timing_hours INTEGER NOT NULL, -- Hours before appointment
    
    -- Content
    reminder_subject VARCHAR(200),
    reminder_message TEXT NOT NULL,
    custom_message TEXT,
    
    -- Delivery details
    scheduled_send_time TIMESTAMP WITH TIME ZONE NOT NULL,
    actual_send_time TIMESTAMP WITH TIME ZONE,
    delivery_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'sent', 'delivered', 'failed', 'bounced'
    
    -- Recipient information
    recipient_contact VARCHAR(500), -- Email, phone, etc.
    delivery_method_details JSONB, -- Provider-specific delivery details
    
    -- Response tracking
    opened BOOLEAN DEFAULT FALSE,
    opened_date TIMESTAMP WITH TIME ZONE,
    clicked BOOLEAN DEFAULT FALSE,
    clicked_date TIMESTAMP WITH TIME ZONE,
    responded BOOLEAN DEFAULT FALSE,
    response_date TIMESTAMP WITH TIME ZONE,
    response_content TEXT,
    
    -- Delivery attempt tracking
    attempt_count INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    last_attempt_time TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    
    -- Administrative
    created_by UUID REFERENCES users(user_id),
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_reminder_timing_positive CHECK (reminder_timing_hours > 0),
    CONSTRAINT chk_attempt_count_non_negative CHECK (attempt_count >= 0)
);

-- Waiting list for appointments
CREATE TABLE appointment_waiting_list (
    waiting_list_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    provider_id UUID REFERENCES healthcare_providers(provider_id),
    
    -- Request details
    requested_appointment_type appointment_type NOT NULL,
    preferred_modality appointment_modality,
    urgency_level VARCHAR(20) DEFAULT 'routine', -- 'routine', 'urgent', 'emergency'
    
    -- Timing preferences
    earliest_acceptable_date DATE,
    latest_acceptable_date DATE,
    preferred_times_of_day scheduling_preference[],
    preferred_days_of_week INTEGER[], -- 1=Monday, 7=Sunday
    
    -- Flexibility
    flexible_with_provider BOOLEAN DEFAULT FALSE,
    flexible_with_modality BOOLEAN DEFAULT TRUE,
    flexible_with_timing BOOLEAN DEFAULT TRUE,
    willing_to_take_cancellation BOOLEAN DEFAULT TRUE,
    
    -- Contact preferences
    contact_methods reminder_type[],
    preferred_contact_method reminder_type,
    contact_hours_start TIME DEFAULT '09:00',
    contact_hours_end TIME DEFAULT '17:00',
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'matched', 'expired', 'cancelled'
    added_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expiration_date DATE,
    position_in_queue INTEGER,
    
    -- Matching and notification
    last_offer_date DATE,
    offers_declined INTEGER DEFAULT 0,
    max_offers INTEGER DEFAULT 5,
    
    -- Clinical context
    clinical_summary TEXT,
    special_requirements TEXT,
    
    -- Administrative
    notes TEXT,
    created_by UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Appointment templates for recurring schedules
CREATE TABLE appointment_templates (
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES healthcare_providers(provider_id),
    
    -- Template details
    template_name VARCHAR(200) NOT NULL,
    appointment_type appointment_type NOT NULL,
    
    -- Standard settings
    default_duration_minutes INTEGER NOT NULL,
    default_modality appointment_modality,
    buffer_time_minutes INTEGER DEFAULT 0,
    
    -- Scheduling rules
    days_of_week INTEGER[] NOT NULL, -- Which days this template applies
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    
    -- Availability
    max_slots_per_day INTEGER,
    advance_booking_limit_days INTEGER,
    minimum_notice_hours INTEGER DEFAULT 24,
    
    -- Patient selection criteria
    patient_types TEXT[], -- 'new_patient', 'returning_patient', 'urgent'
    required_authorizations TEXT[],
    
    -- Automation settings
    auto_confirm BOOLEAN DEFAULT FALSE,
    send_reminders BOOLEAN DEFAULT TRUE,
    reminder_schedule INTEGER[] DEFAULT '{24, 2}', -- Hours before appointment
    
    -- Pricing and billing
    standard_fee DECIMAL(10,2),
    insurance_billable BOOLEAN DEFAULT TRUE,
    requires_copay BOOLEAN DEFAULT TRUE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_template_duration_positive CHECK (default_duration_minutes > 0),
    CONSTRAINT chk_template_times CHECK (start_time < end_time)
);

-- Group appointment sessions
CREATE TABLE group_appointments (
    group_appointment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES healthcare_providers(provider_id),
    
    -- Group details
    group_name VARCHAR(200) NOT NULL,
    group_type VARCHAR(100), -- 'therapy_group', 'psychoeducation', 'support_group', 'skills_training'
    group_topic VARCHAR(200),
    target_population VARCHAR(200),
    
    -- Session details
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL,
    
    -- Capacity
    min_participants INTEGER DEFAULT 3,
    max_participants INTEGER DEFAULT 12,
    current_participants INTEGER DEFAULT 0,
    
    -- Location and modality
    modality appointment_modality NOT NULL DEFAULT 'in_person',
    location_name VARCHAR(200),
    room_number VARCHAR(50),
    telehealth_link VARCHAR(500),
    
    -- Content and structure
    session_objectives TEXT[],
    session_agenda TEXT,
    materials_needed TEXT[],
    homework_assigned TEXT,
    
    -- Status
    status VARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'in_progress', 'completed', 'cancelled'
    cancellation_reason TEXT,
    
    -- Follow-up
    next_session_date DATE,
    series_id UUID, -- Links sessions in a series
    session_number INTEGER, -- Which session in the series
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_group_times CHECK (start_time < end_time),
    CONSTRAINT chk_group_duration_positive CHECK (duration_minutes > 0),
    CONSTRAINT chk_group_capacity CHECK (min_participants <= max_participants)
);

-- Group appointment participants
CREATE TABLE group_appointment_participants (
    participant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_appointment_id UUID NOT NULL REFERENCES group_appointments(group_appointment_id) ON DELETE CASCADE,
    patient_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Participation details
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    participation_status VARCHAR(50) DEFAULT 'enrolled', -- 'enrolled', 'attended', 'absent', 'dropped'
    
    -- Attendance tracking
    checked_in BOOLEAN DEFAULT FALSE,
    check_in_time TIME,
    check_out_time TIME,
    attendance_notes TEXT,
    
    -- Participation quality
    participation_level VARCHAR(50), -- 'active', 'moderate', 'minimal', 'disruptive'
    engagement_score INTEGER, -- 1-10 scale
    homework_completion BOOLEAN DEFAULT FALSE,
    
    -- Special considerations
    accommodations_needed TEXT,
    safety_concerns TEXT,
    group_dynamics_notes TEXT,
    
    -- Billing
    insurance_coverage BOOLEAN DEFAULT TRUE,
    copay_amount DECIMAL(8,2),
    copay_collected BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure unique participation per group session
    CONSTRAINT unique_group_participant UNIQUE(group_appointment_id, patient_id)
);

-- Indexes for performance
CREATE INDEX idx_provider_calendars_provider ON provider_calendars(provider_id);
CREATE INDEX idx_appointments_patient_date ON appointments(patient_id, scheduled_date);
CREATE INDEX idx_appointments_provider_date ON appointments(provider_id, scheduled_date);
CREATE INDEX idx_appointments_status ON appointments(appointment_status);
CREATE INDEX idx_appointment_reminders_send_time ON appointment_reminders(scheduled_send_time);
CREATE INDEX idx_waiting_list_status_urgency ON appointment_waiting_list(status, urgency_level);
CREATE INDEX idx_group_appointments_date ON group_appointments(session_date);

-- Row Level Security
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointment_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointment_waiting_list ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_appointment_participants ENABLE ROW LEVEL SECURITY;

-- Triggers for automated timestamp updates
CREATE TRIGGER update_provider_calendars_updated_at
    BEFORE UPDATE ON provider_calendars
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_provider_schedule_blocks_updated_at
    BEFORE UPDATE ON provider_schedule_blocks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at
    BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointment_reminders_updated_at
    BEFORE UPDATE ON appointment_reminders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointment_waiting_list_updated_at
    BEFORE UPDATE ON appointment_waiting_list
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointment_templates_updated_at
    BEFORE UPDATE ON appointment_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_group_appointments_updated_at
    BEFORE UPDATE ON group_appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_group_appointment_participants_updated_at
    BEFORE UPDATE ON group_appointment_participants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE provider_calendars IS 'Provider calendar settings and availability preferences';
COMMENT ON TABLE provider_schedule_blocks IS 'Provider availability blocks, exceptions, and time-off';
COMMENT ON TABLE appointments IS 'Individual appointment bookings and scheduling';
COMMENT ON TABLE appointment_reminders IS 'Automated reminder system for appointments';
COMMENT ON TABLE appointment_waiting_list IS 'Patient waiting list for appointment availability';
COMMENT ON TABLE appointment_templates IS 'Reusable templates for recurring appointment types';
COMMENT ON TABLE group_appointments IS 'Group therapy and educational sessions';
COMMENT ON TABLE group_appointment_participants IS 'Participants in group appointments and their attendance';
