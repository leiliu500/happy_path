-- Subscription and Payment Management Schema
-- Handles user subscriptions, credit card payments, and billing cycles
-- 
-- IMPORTANT: This system processes payments for platform access only.
-- Payment processing must comply with PCI DSS standards for credit card data.

-- Subscription types
CREATE TYPE subscription_type AS ENUM (
    'basic',
    'premium',
    'professional',
    'enterprise',
    'trial'
);

-- Subscription status
CREATE TYPE subscription_status AS ENUM (
    'active',
    'inactive',
    'cancelled',
    'expired',
    'suspended',
    'trial',
    'pending_payment',
    'past_due'
);

-- Payment method types
CREATE TYPE payment_method_type AS ENUM (
    'credit_card',
    'debit_card',
    'paypal',
    'apple_pay',
    'google_pay',
    'bank_transfer'
);

-- Card types
CREATE TYPE card_type AS ENUM (
    'visa',
    'mastercard',
    'american_express',
    'discover',
    'diners_club',
    'jcb',
    'unionpay'
);

-- Billing intervals
CREATE TYPE billing_interval AS ENUM (
    'monthly',
    'quarterly',
    'semi_annual',
    'annual'
);

-- Subscription plans
CREATE TABLE subscription_plans (
    plan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_name VARCHAR(100) NOT NULL UNIQUE,
    plan_type subscription_type NOT NULL,
    description TEXT,
    
    -- Pricing
    monthly_price DECIMAL(10,2) NOT NULL,
    quarterly_price DECIMAL(10,2),
    semi_annual_price DECIMAL(10,2),
    annual_price DECIMAL(10,2),
    
    -- Trial settings
    trial_days INTEGER DEFAULT 0,
    trial_price DECIMAL(10,2) DEFAULT 0.00,
    
    -- Features and limits
    max_journal_entries INTEGER,
    max_mood_entries_per_day INTEGER,
    max_assessment_frequency_days INTEGER, -- minimum days between assessments
    provider_coordination_included BOOLEAN DEFAULT FALSE,
    premium_analytics_included BOOLEAN DEFAULT FALSE,
    priority_support_included BOOLEAN DEFAULT FALSE,
    ai_insights_included BOOLEAN DEFAULT FALSE,
    
    -- Plan status
    is_active BOOLEAN DEFAULT TRUE,
    is_visible BOOLEAN DEFAULT TRUE, -- whether shown to new subscribers
    sort_order INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_pricing_positive CHECK (
        monthly_price >= 0 AND
        (quarterly_price IS NULL OR quarterly_price >= 0) AND
        (semi_annual_price IS NULL OR semi_annual_price >= 0) AND
        (annual_price IS NULL OR annual_price >= 0)
    ),
    CONSTRAINT chk_trial_days_positive CHECK (trial_days >= 0),
    CONSTRAINT chk_trial_price_positive CHECK (trial_price >= 0)
);

-- User payment methods (tokenized for PCI compliance)
CREATE TABLE user_payment_methods (
    payment_method_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Payment method details
    method_type payment_method_type NOT NULL,
    
    -- Credit card information (tokenized)
    card_token VARCHAR(500), -- Encrypted token from payment processor
    card_type card_type,
    last_four_digits CHAR(4),
    expiry_month INTEGER,
    expiry_year INTEGER,
    cardholder_name VARCHAR(200),
    
    -- Billing address
    billing_address_line1 VARCHAR(255),
    billing_address_line2 VARCHAR(255),
    billing_city VARCHAR(100),
    billing_state VARCHAR(100),
    billing_postal_code VARCHAR(20),
    billing_country CHAR(2) DEFAULT 'US',
    
    -- Payment processor information
    processor_name VARCHAR(50), -- 'stripe', 'square', 'paypal', etc.
    processor_customer_id VARCHAR(255),
    processor_payment_method_id VARCHAR(255),
    
    -- Status and verification
    is_default BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_date TIMESTAMP WITH TIME ZONE,
    last_used_date TIMESTAMP WITH TIME ZONE,
    
    -- Security
    fingerprint VARCHAR(255), -- unique identifier for duplicate detection
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_expiry_month CHECK (expiry_month >= 1 AND expiry_month <= 12),
    CONSTRAINT chk_expiry_year CHECK (expiry_year >= EXTRACT(YEAR FROM CURRENT_DATE)),
    CONSTRAINT chk_last_four_digits CHECK (last_four_digits ~ '^\d{4}$')
);

-- User subscriptions
CREATE TABLE user_subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES subscription_plans(plan_id),
    payment_method_id UUID REFERENCES user_payment_methods(payment_method_id),
    
    -- Subscription details
    status subscription_status NOT NULL DEFAULT 'trial',
    billing_interval billing_interval NOT NULL DEFAULT 'monthly',
    
    -- Pricing (locked in at subscription time)
    current_price DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    
    -- Dates
    start_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    trial_end_date TIMESTAMP WITH TIME ZONE,
    current_period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    current_period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE,
    
    -- Billing
    next_billing_date TIMESTAMP WITH TIME ZONE,
    last_payment_date TIMESTAMP WITH TIME ZONE,
    failed_payment_count INTEGER DEFAULT 0,
    
    -- Processor integration
    processor_subscription_id VARCHAR(255), -- External subscription ID
    processor_customer_id VARCHAR(255),
    
    -- Metadata
    subscription_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_current_price_positive CHECK (current_price >= 0),
    CONSTRAINT chk_period_dates CHECK (current_period_end > current_period_start),
    CONSTRAINT chk_trial_end_after_start CHECK (trial_end_date IS NULL OR trial_end_date > start_date),
    CONSTRAINT chk_failed_payment_count CHECK (failed_payment_count >= 0)
);

-- Subscription payments and invoices
CREATE TABLE subscription_invoices (
    invoice_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID NOT NULL REFERENCES user_subscriptions(subscription_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Invoice details
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    status payment_status NOT NULL DEFAULT 'pending',
    
    -- Amounts
    subtotal DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    
    -- Billing period
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Dates
    invoice_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    paid_date TIMESTAMP WITH TIME ZONE,
    
    -- Payment processing
    payment_method_id UUID REFERENCES user_payment_methods(payment_method_id),
    processor_invoice_id VARCHAR(255),
    processor_payment_intent_id VARCHAR(255),
    
    -- Metadata
    invoice_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_amounts_positive CHECK (
        subtotal >= 0 AND 
        tax_amount >= 0 AND 
        discount_amount >= 0 AND 
        total_amount >= 0
    ),
    CONSTRAINT chk_period_valid CHECK (period_end > period_start),
    CONSTRAINT chk_due_after_invoice CHECK (due_date >= invoice_date)
);

-- Subscription payment transactions
CREATE TABLE subscription_payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES subscription_invoices(invoice_id) ON DELETE CASCADE,
    subscription_id UUID NOT NULL REFERENCES user_subscriptions(subscription_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    payment_method_id UUID REFERENCES user_payment_methods(payment_method_id),
    
    -- Payment details
    amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    status payment_status NOT NULL DEFAULT 'pending',
    
    -- Processor information
    processor_name VARCHAR(50) NOT NULL,
    processor_transaction_id VARCHAR(255),
    processor_charge_id VARCHAR(255),
    
    -- Transaction details
    attempted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE,
    failed_at TIMESTAMP WITH TIME ZONE,
    
    -- Error handling
    failure_code VARCHAR(100),
    failure_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Metadata
    payment_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_retry_count CHECK (retry_count >= 0)
);

-- Subscription usage tracking
CREATE TABLE subscription_usage (
    usage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID NOT NULL REFERENCES user_subscriptions(subscription_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Usage period
    usage_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Feature usage counts
    journal_entries_created INTEGER DEFAULT 0,
    mood_entries_created INTEGER DEFAULT 0,
    assessments_completed INTEGER DEFAULT 0,
    provider_messages_sent INTEGER DEFAULT 0,
    ai_insights_generated INTEGER DEFAULT 0,
    
    -- Session tracking
    login_count INTEGER DEFAULT 0,
    session_duration_minutes INTEGER DEFAULT 0,
    
    -- API usage (if applicable)
    api_calls_made INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(subscription_id, usage_date),
    
    CONSTRAINT chk_usage_counts_positive CHECK (
        journal_entries_created >= 0 AND
        mood_entries_created >= 0 AND
        assessments_completed >= 0 AND
        provider_messages_sent >= 0 AND
        ai_insights_generated >= 0 AND
        login_count >= 0 AND
        session_duration_minutes >= 0 AND
        api_calls_made >= 0
    )
);

-- Subscription coupons and discounts
CREATE TABLE subscription_coupons (
    coupon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Coupon details
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Discount configuration
    discount_type VARCHAR(20) NOT NULL, -- 'percentage', 'fixed_amount', 'free_trial'
    discount_value DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    
    -- Usage limits
    max_redemptions INTEGER, -- NULL for unlimited
    times_redeemed INTEGER DEFAULT 0,
    max_redemptions_per_user INTEGER DEFAULT 1,
    
    -- Validity period
    valid_from TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP WITH TIME ZONE,
    
    -- Restrictions
    minimum_amount DECIMAL(10,2),
    applicable_plans UUID[], -- Array of plan_ids, NULL for all plans
    first_time_customers_only BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_discount_value_positive CHECK (discount_value >= 0),
    CONSTRAINT chk_redemption_counts CHECK (
        (max_redemptions IS NULL OR max_redemptions >= times_redeemed) AND
        max_redemptions_per_user >= 1
    ),
    CONSTRAINT chk_validity_period CHECK (valid_until IS NULL OR valid_until > valid_from),
    CONSTRAINT chk_discount_type CHECK (discount_type IN ('percentage', 'fixed_amount', 'free_trial'))
);

-- User coupon redemptions
CREATE TABLE user_coupon_redemptions (
    redemption_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    coupon_id UUID NOT NULL REFERENCES subscription_coupons(coupon_id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES user_subscriptions(subscription_id) ON DELETE SET NULL,
    
    -- Redemption details
    discount_amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    
    -- Dates
    redeemed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, coupon_id),
    
    CONSTRAINT chk_discount_amount_positive CHECK (discount_amount >= 0)
);

-- =============================================================================
-- INDEXES
-- =============================================================================

-- Subscription plans
CREATE INDEX idx_subscription_plans_type_active ON subscription_plans(plan_type, is_active);
CREATE INDEX idx_subscription_plans_visible_sort ON subscription_plans(is_visible, sort_order);

-- User payment methods
CREATE INDEX idx_user_payment_methods_user_id ON user_payment_methods(user_id);
CREATE INDEX idx_user_payment_methods_default ON user_payment_methods(user_id, is_default) WHERE is_default = TRUE;
CREATE INDEX idx_user_payment_methods_processor ON user_payment_methods(processor_name, processor_customer_id);

-- User subscriptions
CREATE INDEX idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX idx_user_subscriptions_status ON user_subscriptions(status);
CREATE INDEX idx_user_subscriptions_next_billing ON user_subscriptions(next_billing_date) WHERE status = 'active';
CREATE INDEX idx_user_subscriptions_processor ON user_subscriptions(processor_subscription_id);

-- Subscription invoices
CREATE INDEX idx_subscription_invoices_subscription_id ON subscription_invoices(subscription_id);
CREATE INDEX idx_subscription_invoices_user_id ON subscription_invoices(user_id);
CREATE INDEX idx_subscription_invoices_status ON subscription_invoices(status);
CREATE INDEX idx_subscription_invoices_due_date ON subscription_invoices(due_date) WHERE status IN ('pending', 'processing');
CREATE INDEX idx_subscription_invoices_number ON subscription_invoices(invoice_number);

-- Subscription payments
CREATE INDEX idx_subscription_payments_invoice_id ON subscription_payments(invoice_id);
CREATE INDEX idx_subscription_payments_subscription_id ON subscription_payments(subscription_id);
CREATE INDEX idx_subscription_payments_user_id ON subscription_payments(user_id);
CREATE INDEX idx_subscription_payments_status ON subscription_payments(status);
CREATE INDEX idx_subscription_payments_processor ON subscription_payments(processor_name, processor_transaction_id);

-- Subscription usage
CREATE INDEX idx_subscription_usage_subscription_date ON subscription_usage(subscription_id, usage_date);
CREATE INDEX idx_subscription_usage_user_date ON subscription_usage(user_id, usage_date);

-- Subscription coupons
CREATE INDEX idx_subscription_coupons_code ON subscription_coupons(code) WHERE is_active = TRUE;
CREATE INDEX idx_subscription_coupons_validity ON subscription_coupons(valid_from, valid_until) WHERE is_active = TRUE;

-- User coupon redemptions
CREATE INDEX idx_user_coupon_redemptions_user_id ON user_coupon_redemptions(user_id);
CREATE INDEX idx_user_coupon_redemptions_coupon_id ON user_coupon_redemptions(coupon_id);

-- =============================================================================
-- ROW LEVEL SECURITY
-- =============================================================================

-- Enable RLS on all tables
ALTER TABLE subscription_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_payment_methods ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_coupons ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_coupon_redemptions ENABLE ROW LEVEL SECURITY;

-- =============================================================================
-- TRIGGERS
-- =============================================================================

-- Update timestamps
CREATE TRIGGER update_subscription_plans_updated_at
    BEFORE UPDATE ON subscription_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_payment_methods_updated_at
    BEFORE UPDATE ON user_payment_methods
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_subscriptions_updated_at
    BEFORE UPDATE ON user_subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscription_invoices_updated_at
    BEFORE UPDATE ON subscription_invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscription_payments_updated_at
    BEFORE UPDATE ON subscription_payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscription_usage_updated_at
    BEFORE UPDATE ON subscription_usage
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscription_coupons_updated_at
    BEFORE UPDATE ON subscription_coupons
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- FUNCTIONS
-- =============================================================================

-- Function to get user's current active subscription
CREATE OR REPLACE FUNCTION get_user_active_subscription(p_user_id UUID)
RETURNS TABLE (
    subscription_id UUID,
    plan_name VARCHAR,
    status subscription_status,
    current_price DECIMAL,
    current_period_end TIMESTAMP WITH TIME ZONE,
    features JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        us.subscription_id,
        sp.plan_name,
        us.status,
        us.current_price,
        us.current_period_end,
        jsonb_build_object(
            'max_journal_entries', sp.max_journal_entries,
            'max_mood_entries_per_day', sp.max_mood_entries_per_day,
            'provider_coordination_included', sp.provider_coordination_included,
            'premium_analytics_included', sp.premium_analytics_included,
            'priority_support_included', sp.priority_support_included,
            'ai_insights_included', sp.ai_insights_included
        ) as features
    FROM user_subscriptions us
    JOIN subscription_plans sp ON us.plan_id = sp.plan_id
    WHERE us.user_id = p_user_id 
      AND us.status IN ('active', 'trial')
      AND us.current_period_end > CURRENT_TIMESTAMP
    ORDER BY us.created_at DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to check if user has access to a feature
CREATE OR REPLACE FUNCTION user_has_feature_access(
    p_user_id UUID,
    p_feature_name VARCHAR
) RETURNS BOOLEAN AS $$
DECLARE
    v_subscription_record RECORD;
    v_has_access BOOLEAN DEFAULT FALSE;
BEGIN
    -- Get user's active subscription with plan details
    SELECT 
        sp.plan_type,
        sp.provider_coordination_included,
        sp.premium_analytics_included,
        sp.priority_support_included,
        sp.ai_insights_included,
        us.status
    INTO v_subscription_record
    FROM user_subscriptions us
    JOIN subscription_plans sp ON us.plan_id = sp.plan_id
    WHERE us.user_id = p_user_id 
      AND us.status IN ('active', 'trial')
      AND us.current_period_end > CURRENT_TIMESTAMP
    ORDER BY us.created_at DESC
    LIMIT 1;
    
    -- If no active subscription, deny access
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Check feature access based on subscription
    CASE p_feature_name
        WHEN 'provider_coordination' THEN
            v_has_access := v_subscription_record.provider_coordination_included;
        WHEN 'premium_analytics' THEN
            v_has_access := v_subscription_record.premium_analytics_included;
        WHEN 'priority_support' THEN
            v_has_access := v_subscription_record.priority_support_included;
        WHEN 'ai_insights' THEN
            v_has_access := v_subscription_record.ai_insights_included;
        WHEN 'basic_features' THEN
            v_has_access := TRUE; -- All subscriptions have basic features
        ELSE
            v_has_access := FALSE;
    END CASE;
    
    RETURN v_has_access;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
-- COMMENTS
-- =============================================================================

COMMENT ON TABLE subscription_plans IS 'Available subscription plans with pricing and features';
COMMENT ON TABLE user_payment_methods IS 'Tokenized payment methods for PCI compliance';
COMMENT ON TABLE user_subscriptions IS 'User subscription records and billing cycles';
COMMENT ON TABLE subscription_invoices IS 'Billing invoices for subscription payments';
COMMENT ON TABLE subscription_payments IS 'Payment transaction records for subscriptions';
COMMENT ON TABLE subscription_usage IS 'Daily usage tracking for subscription features';
COMMENT ON TABLE subscription_coupons IS 'Discount coupons and promotional codes';
COMMENT ON TABLE user_coupon_redemptions IS 'User coupon usage history';

COMMENT ON FUNCTION get_user_active_subscription(UUID) IS 'Get user''s current active subscription details';
COMMENT ON FUNCTION user_has_feature_access(UUID, VARCHAR) IS 'Check if user has access to a specific platform feature';
