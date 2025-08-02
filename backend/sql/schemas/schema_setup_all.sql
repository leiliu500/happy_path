-- Complete Database Setup Script
-- Run this script from the schemas directory to set up the entire Happy Path database
-- This script executes all schema files in the correct dependency order

-- =============================================================================
-- HAPPY PATH MENTAL HEALTH APPLICATION - COMPLETE DATABASE SETUP
-- =============================================================================

\echo 'Starting Happy Path database setup...'
\echo ''

-- 1. Master Setup (Extensions, Functions, Utilities) - In schemas directory
\echo 'Step 1/14: Setting up extensions and base functions...'
\i 00_master_setup.sql
\echo 'Master setup completed.'
\echo ''

-- 2. User Management (Core dependency for all other schemas)
\echo 'Step 2/14: Creating user management tables...'
\i user_management.sql
\echo 'User management schema completed.'
\echo ''

-- 3. Care Coordination (Provider network - needed before clinical schemas)
\echo 'Step 3/14: Creating care coordination and provider network...'
\i care_coordination.sql
\echo 'Care coordination schema completed.'
\echo ''

-- 4. Insurance and Billing (Core financial infrastructure)
\echo 'Step 4/15: Creating insurance and billing tables...'
\i insurance_billing.sql
\echo 'Insurance and billing schema completed.'
\echo ''

-- 5. Subscription and Payment Management (User billing and subscriptions)
\echo 'Step 5/15: Creating subscription and payment tables...'
\i subscription_billing.sql
\echo 'Subscription billing schema completed.'
\echo ''

-- 6. Appointment and Scheduling (Core operational functionality)
\echo 'Step 6/15: Creating appointment and scheduling tables...'
\i appointment_scheduling.sql
\echo 'Appointment scheduling schema completed.'
\echo ''

-- 7. Assessment and Screening Tools
\echo 'Step 7/15: Creating assessment and screening tables...'
\i assessments_screening.sql
\echo 'Assessment and screening schema completed.'
\echo ''

-- 8. Medication Management
\echo 'Step 8/15: Creating medication management tables...'
\i medication_management.sql
\echo 'Medication management schema completed.'
\echo ''

-- 9. Mood Tracking (Depends on users)
\echo 'Step 9/15: Creating mood tracking tables...'
\i mood_tracking.sql
\echo 'Mood tracking schema completed.'
\echo ''

-- 10. Journaling (Depends on users)
\echo 'Step 10/15: Creating journaling tables...'
\i journaling.sql
\echo 'Journaling schema completed.'
\echo ''

-- 11. Crisis Management (Depends on users and may reference mood/journal data)
\echo 'Step 11/15: Creating crisis management tables...'
\i crisis_management.sql
\echo 'Crisis management schema completed.'
\echo ''

-- 12. Conversational Agent (Depends on users and references other user data)
\echo 'Step 12/15: Creating conversational agent tables...'
\i conversational_agent.sql
\echo 'Conversational agent schema completed.'
\echo ''

-- 13. Clinical Therapy (Depends on users and therapeutic relationships)
\echo 'Step 13/15: Creating clinical therapy tables...'
\i clinical_therapy.sql
\echo 'Clinical therapy schema completed.'
\echo ''

-- 14. Compliance and Privacy Management
\echo 'Step 14/15: Creating compliance and privacy tables...'
\i compliance_privacy.sql
\echo 'Compliance and privacy schema completed.'
\echo ''

-- 15. Analytics and Reporting (Depends on most other schemas for data)
\echo 'Step 15/15: Creating analytics and reporting tables...'
\i analytics_reporting.sql
\echo 'Analytics and reporting schema completed.'
\echo ''

-- 16. System Administration (Always last)
\echo 'Step 16/16: Creating system administration tables...'
\i system_administration.sql
\echo 'System administration schema completed.'
\echo ''

-- 17. Initial Data Setup
\echo 'Step 17/17: Loading initial data...'
\i initial_data.sql
\echo 'Initial data loading completed.'
\echo ''

-- =============================================================================
-- POST-SETUP VERIFICATION
-- =============================================================================

\echo 'Running post-setup verification...'

-- Count tables created
\echo 'Tables created:'
SELECT COUNT(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE';

-- Count functions created
\echo 'Functions created:'
SELECT COUNT(*) as function_count 
FROM information_schema.routines 
WHERE routine_schema = 'public' 
  AND routine_type = 'FUNCTION';

-- Count custom types created
\echo 'Custom types created:'
SELECT COUNT(*) as type_count 
FROM pg_type 
WHERE typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
  AND typtype = 'e';

\echo ''
\echo '============================================================================='
\echo 'Happy Path database setup completed successfully!'
\echo '============================================================================='
\echo ''
\echo 'Next steps:'
\echo '1. Configure application connection settings'
\echo '2. Set up SSL/TLS certificates for secure connections'
\echo '3. Configure backup and monitoring procedures'
\echo '4. Review and adjust system configurations as needed'
\echo '5. Set up row-level security policies if multi-tenant deployment'
\echo ''
\echo 'Database now includes:'
\echo '- Comprehensive mental health and wellness platform'
\echo '- User subscription and credit card payment processing'
\echo '- Professional provider coordination capabilities'
\echo '- Privacy protection and data security infrastructure'
\echo '- Payment processing and service management'
\echo '- Personal wellness tracking and insights'
\echo '- Crisis support resource connections'
\echo ''
\echo 'Note: This platform provides wellness support and does not'
\echo 'constitute medical diagnosis or treatment. Users should consult'
\echo 'with licensed healthcare professionals for medical care.'
\echo ''
\echo 'For detailed information, see docs/database_model.md'
\echo '============================================================================='
