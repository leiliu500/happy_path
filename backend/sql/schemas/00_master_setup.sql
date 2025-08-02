-- Master Database Schema Setup
-- This file creates all necessary extensions, types, and base functions
-- Run this FIRST before running any other schema files

-- Enable necessary PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Create custom functions for common operations

-- Function to update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to validate email format
CREATE OR REPLACE FUNCTION is_valid_email(email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
END;
$$ LANGUAGE plpgsql;

-- Function to generate secure random passwords
CREATE OR REPLACE FUNCTION generate_secure_password(length INTEGER DEFAULT 16)
RETURNS TEXT AS $$
DECLARE
    chars TEXT := 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    result TEXT := '';
    i INTEGER;
BEGIN
    FOR i IN 1..length LOOP
        result := result || substr(chars, floor(random() * length(chars) + 1)::INTEGER, 1);
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function to anonymize sensitive data
CREATE OR REPLACE FUNCTION anonymize_text(input_text TEXT, preserve_length BOOLEAN DEFAULT TRUE)
RETURNS TEXT AS $$
BEGIN
    IF input_text IS NULL THEN
        RETURN NULL;
    END IF;
    
    IF preserve_length THEN
        RETURN repeat('*', length(input_text));
    ELSE
        RETURN '[REDACTED]';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate age from date of birth
CREATE OR REPLACE FUNCTION calculate_age(birth_date DATE)
RETURNS INTEGER AS $$
BEGIN
    IF birth_date IS NULL THEN
        RETURN NULL;
    END IF;
    
    RETURN EXTRACT(YEAR FROM age(CURRENT_DATE, birth_date))::INTEGER;
END;
$$ LANGUAGE plpgsql;

-- Function to mask sensitive data for logging
CREATE OR REPLACE FUNCTION mask_sensitive_data(data JSONB, sensitive_fields TEXT[])
RETURNS JSONB AS $$
DECLARE
    result JSONB := data;
    field TEXT;
BEGIN
    FOREACH field IN ARRAY sensitive_fields LOOP
        IF result ? field THEN
            result := jsonb_set(result, ARRAY[field], '"[MASKED]"'::jsonb);
        END IF;
    END LOOP;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function to validate phone numbers (basic US format)
CREATE OR REPLACE FUNCTION is_valid_phone(phone TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    IF phone IS NULL THEN
        RETURN TRUE; -- Allow NULL
    END IF;
    
    -- Remove all non-digits
    phone := regexp_replace(phone, '[^0-9]', '', 'g');
    
    -- Check if it's 10 or 11 digits (with or without country code)
    RETURN length(phone) IN (10, 11);
END;
$$ LANGUAGE plpgsql;

-- Function to generate crisis detection score
CREATE OR REPLACE FUNCTION calculate_crisis_score(
    keyword_scores JSONB,
    sentiment_score DECIMAL DEFAULT NULL,
    context_factors TEXT[] DEFAULT NULL
)
RETURNS DECIMAL AS $$
DECLARE
    base_score DECIMAL := 0;
    sentiment_weight DECIMAL := 0.3;
    context_weight DECIMAL := 0.2;
    final_score DECIMAL;
BEGIN
    -- Calculate base score from keywords
    IF keyword_scores IS NOT NULL THEN
        SELECT COALESCE(AVG((value::TEXT)::DECIMAL), 0)
        INTO base_score
        FROM jsonb_each(keyword_scores);
    END IF;
    
    -- Adjust for sentiment
    IF sentiment_score IS NOT NULL AND sentiment_score < 0 THEN
        base_score := base_score + (ABS(sentiment_score) * sentiment_weight);
    END IF;
    
    -- Adjust for context factors
    IF context_factors IS NOT NULL THEN
        base_score := base_score + (array_length(context_factors, 1) * context_weight * 0.1);
    END IF;
    
    -- Normalize to 0-1 range
    final_score := LEAST(base_score, 1.0);
    
    RETURN final_score;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate mood trend
CREATE OR REPLACE FUNCTION calculate_mood_trend(
    user_id_param UUID,
    days_back INTEGER DEFAULT 30
)
RETURNS TEXT AS $$
DECLARE
    recent_avg DECIMAL;
    older_avg DECIMAL;
    trend TEXT;
BEGIN
    -- Get recent average (last 7 days)
    SELECT AVG(overall_mood::INTEGER)
    INTO recent_avg
    FROM mood_entries
    WHERE user_id = user_id_param
      AND entry_date >= CURRENT_DATE - INTERVAL '7 days'
      AND entry_date >= CURRENT_DATE - INTERVAL (days_back || ' days');
    
    -- Get older average (8-30 days back)
    SELECT AVG(overall_mood::INTEGER)
    INTO older_avg
    FROM mood_entries
    WHERE user_id = user_id_param
      AND entry_date < CURRENT_DATE - INTERVAL '7 days'
      AND entry_date >= CURRENT_DATE - INTERVAL (days_back || ' days');
    
    -- Determine trend
    IF recent_avg IS NULL OR older_avg IS NULL THEN
        RETURN 'insufficient_data';
    ELSIF recent_avg > older_avg + 0.5 THEN
        RETURN 'improving';
    ELSIF recent_avg < older_avg - 0.5 THEN
        RETURN 'declining';
    ELSE
        RETURN 'stable';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to check data retention eligibility
CREATE OR REPLACE FUNCTION is_eligible_for_deletion(
    table_name_param TEXT,
    record_date DATE,
    retention_days INTEGER
)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN record_date < CURRENT_DATE - INTERVAL (retention_days || ' days');
END;
$$ LANGUAGE plpgsql;

-- Function to generate anonymized user identifier
CREATE OR REPLACE FUNCTION generate_anonymous_id(user_id_param UUID)
RETURNS TEXT AS $$
BEGIN
    RETURN 'USER_' || encode(digest(user_id_param::TEXT, 'sha256'), 'hex')::TEXT;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate business days between dates
CREATE OR REPLACE FUNCTION calculate_business_days(start_date DATE, end_date DATE)
RETURNS INTEGER AS $$
BEGIN
    IF start_date IS NULL OR end_date IS NULL THEN
        RETURN NULL;
    END IF;
    
    RETURN (
        SELECT COUNT(*)::INTEGER
        FROM generate_series(start_date, end_date, '1 day'::interval) AS d
        WHERE EXTRACT(DOW FROM d) BETWEEN 1 AND 5
    );
END;
$$ LANGUAGE plpgsql;

-- Function to validate appointment scheduling conflicts
CREATE OR REPLACE FUNCTION check_appointment_conflict(
    provider_id_param UUID,
    appointment_date DATE,
    start_time TIME,
    end_time TIME,
    exclude_appointment_id UUID DEFAULT NULL
)
RETURNS BOOLEAN AS $$
DECLARE
    conflict_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO conflict_count
    FROM appointments
    WHERE provider_id = provider_id_param
      AND scheduled_date = appointment_date
      AND appointment_status NOT IN ('cancelled_by_patient', 'cancelled_by_provider', 'no_show')
      AND (appointment_id != exclude_appointment_id OR exclude_appointment_id IS NULL)
      AND (
          (scheduled_start_time <= start_time AND scheduled_end_time > start_time) OR
          (scheduled_start_time < end_time AND scheduled_end_time >= end_time) OR
          (scheduled_start_time >= start_time AND scheduled_end_time <= end_time)
      );
    
    RETURN conflict_count > 0;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate medication adherence percentage
CREATE OR REPLACE FUNCTION calculate_medication_adherence(
    user_id_param UUID,
    medication_record_id_param UUID,
    start_date DATE,
    end_date DATE
)
RETURNS DECIMAL AS $$
DECLARE
    total_scheduled INTEGER;
    total_taken INTEGER;
    adherence_rate DECIMAL;
BEGIN
    SELECT 
        COUNT(*) AS scheduled,
        COUNT(*) FILTER (WHERE was_taken = TRUE) AS taken
    INTO total_scheduled, total_taken
    FROM medication_adherence
    WHERE user_id = user_id_param
      AND medication_record_id = medication_record_id_param
      AND scheduled_date BETWEEN start_date AND end_date;
    
    IF total_scheduled = 0 THEN
        RETURN NULL;
    END IF;
    
    adherence_rate := (total_taken::DECIMAL / total_scheduled::DECIMAL) * 100;
    RETURN ROUND(adherence_rate, 2);
END;
$$ LANGUAGE plpgsql;

-- Function to generate secure session tokens
CREATE OR REPLACE FUNCTION generate_session_token()
RETURNS TEXT AS $$
BEGIN
    RETURN encode(gen_random_bytes(32), 'base64');
END;
$$ LANGUAGE plpgsql;

-- Function to validate and normalize phone numbers
CREATE OR REPLACE FUNCTION normalize_phone_number(phone_input TEXT)
RETURNS TEXT AS $$
DECLARE
    cleaned_phone TEXT;
BEGIN
    IF phone_input IS NULL THEN
        RETURN NULL;
    END IF;
    
    -- Remove all non-digits
    cleaned_phone := regexp_replace(phone_input, '[^0-9]', '', 'g');
    
    -- Handle US numbers with country code
    IF length(cleaned_phone) = 11 AND left(cleaned_phone, 1) = '1' THEN
        cleaned_phone := right(cleaned_phone, 10);
    END IF;
    
    -- Validate length (US numbers)
    IF length(cleaned_phone) != 10 THEN
        RETURN NULL;
    END IF;
    
    -- Format as (XXX) XXX-XXXX
    RETURN '(' || left(cleaned_phone, 3) || ') ' || 
           substring(cleaned_phone, 4, 3) || '-' || 
           right(cleaned_phone, 4);
END;
$$ LANGUAGE plpgsql;

-- Function to calculate financial year-to-date totals
CREATE OR REPLACE FUNCTION calculate_ytd_financial_metrics(
    metric_type TEXT,
    as_of_date DATE DEFAULT CURRENT_DATE
)
RETURNS DECIMAL AS $$
DECLARE
    year_start DATE;
    total_amount DECIMAL := 0;
BEGIN
    year_start := DATE_TRUNC('year', as_of_date)::DATE;
    
    CASE metric_type
        WHEN 'revenue' THEN
            SELECT COALESCE(SUM(net_amount), 0)
            INTO total_amount
            FROM payment_transactions
            WHERE payment_status = 'completed'
              AND transaction_date BETWEEN year_start AND as_of_date;
        
        WHEN 'charges' THEN
            SELECT COALESCE(SUM(charge_amount), 0)
            INTO total_amount
            FROM billing_encounters
            WHERE service_date BETWEEN year_start AND as_of_date;
        
        WHEN 'collections' THEN
            SELECT COALESCE(SUM(amount_paid), 0)
            INTO total_amount
            FROM patient_billing
            WHERE billing_date BETWEEN year_start AND as_of_date;
        
        ELSE
            RETURN NULL;
    END CASE;
    
    RETURN total_amount;
END;
$$ LANGUAGE plpgsql;

-- Create custom domain types for common patterns

-- Domain for mood scales (1-10)
CREATE DOMAIN mood_scale_domain AS INTEGER
    CHECK (VALUE >= 1 AND VALUE <= 10);

-- Domain for percentage values
CREATE DOMAIN percentage_domain AS DECIMAL(5,2)
    CHECK (VALUE >= 0 AND VALUE <= 100);

-- Domain for normalized scores (0-1)
CREATE DOMAIN normalized_score_domain AS DECIMAL(5,4)
    CHECK (VALUE >= 0 AND VALUE <= 1);

-- Domain for positive integers
CREATE DOMAIN positive_integer_domain AS INTEGER
    CHECK (VALUE > 0);

-- Domain for email addresses
CREATE DOMAIN email_domain AS TEXT
    CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Domain for phone numbers
CREATE DOMAIN phone_domain AS TEXT
    CHECK (VALUE ~* '^[\+]?[1-9][\d]{0,15}$' OR VALUE IS NULL);

-- Domain for currency amounts
CREATE DOMAIN currency_domain AS DECIMAL(10,2)
    CHECK (VALUE >= 0);

-- Domain for rating scores (1-5)
CREATE DOMAIN rating_scale_domain AS DECIMAL(3,2)
    CHECK (VALUE >= 1 AND VALUE <= 5);

-- Create indexes for common UUID lookups (will be created after tables)
-- These will be referenced in individual schema files

-- Create a view for commonly used user information
-- (This will be created after user tables exist)

-- Database-level settings for performance and security
ALTER DATABASE postgres SET timezone TO 'UTC';
ALTER DATABASE postgres SET log_statement TO 'mod';
ALTER DATABASE postgres SET log_min_duration_statement TO 1000; -- Log slow queries

-- Row Level Security policies will be defined in each schema file
-- Enable RLS by default on sensitive tables

-- =============================================================================
-- SCHEMA SETUP COMPLETE
-- =============================================================================
-- This completes the master schema setup.
-- Next steps:
-- 1. Run all schema files in order (see README_SETUP.sql)
-- 2. Run initial_data.sql to populate essential data
-- 3. Configure application-specific settings
-- 4. Set up monitoring and maintenance procedures

COMMENT ON FUNCTION update_updated_at_column() IS 'Trigger function to automatically update updated_at timestamps';
COMMENT ON FUNCTION is_valid_email(TEXT) IS 'Validates email address format using regex';
COMMENT ON FUNCTION generate_secure_password(INTEGER) IS 'Generates cryptographically secure random password';
COMMENT ON FUNCTION anonymize_text(TEXT, BOOLEAN) IS 'Anonymizes text data for privacy compliance';
COMMENT ON FUNCTION calculate_age(DATE) IS 'Calculates age in years from date of birth';
COMMENT ON FUNCTION mask_sensitive_data(JSONB, TEXT[]) IS 'Masks sensitive fields in JSONB data for logging';
COMMENT ON FUNCTION is_valid_phone(TEXT) IS 'Validates phone number format (US)';
COMMENT ON FUNCTION calculate_crisis_score(JSONB, DECIMAL, TEXT[]) IS 'Calculates crisis detection score from multiple factors';
COMMENT ON FUNCTION calculate_mood_trend(UUID, INTEGER) IS 'Calculates mood trend for a user over specified time period';
COMMENT ON FUNCTION is_eligible_for_deletion(TEXT, DATE, INTEGER) IS 'Checks if a record is eligible for deletion based on retention policy';
COMMENT ON FUNCTION generate_anonymous_id(UUID) IS 'Generates anonymized identifier for user data';

COMMENT ON SCHEMA public IS 'Happy Path Mental Health Application - Master Schema Setup with Extensions, Functions, and Utilities';
