-- Complete Database Setup Script
-- Run this script from the schemas directory to set up the entire Happy Path database
-- This script executes all schema files in the correct dependency order

-- =============================================================================
-- HAPPY PATH MENTAL HEALTH APPLICATION - COMPLETE DATABASE SETUP
-- =============================================================================

\echo 'Starting Happy Path database setup...'
\echo ''

-- 1. Master Setup (Extensions, Functions, Utilities) - In schemas directory
\echo 'Step 1/9: Setting up extensions and base functions...'
\i 00_master_setup.sql
\echo 'Master setup completed.'
\echo ''

-- 2. User Management (Core dependency for all other schemas)
\echo 'Step 2/9: Creating user management tables...'
\i user_management.sql
\echo 'User management schema completed.'
\echo ''

-- 3. Mood Tracking (Depends on users)
\echo 'Step 3/9: Creating mood tracking tables...'
\i mood_tracking.sql
\echo 'Mood tracking schema completed.'
\echo ''

-- 4. Journaling (Depends on users)
\echo 'Step 4/9: Creating journaling tables...'
\i journaling.sql
\echo 'Journaling schema completed.'
\echo ''

-- 5. Crisis Management (Depends on users and may reference mood/journal data)
\echo 'Step 5/9: Creating crisis management tables...'
\i crisis_management.sql
\echo 'Crisis management schema completed.'
\echo ''

-- 6. Conversational Agent (Depends on users and references other user data)
\echo 'Step 6/9: Creating conversational agent tables...'
\i conversational_agent.sql
\echo 'Conversational agent schema completed.'
\echo ''

-- 7. Clinical Therapy (Depends on users and therapeutic relationships)
\echo 'Step 7/9: Creating clinical therapy tables...'
\i clinical_therapy.sql
\echo 'Clinical therapy schema completed.'
\echo ''

-- 8. System Administration (Can reference all other tables for auditing)
\echo 'Step 8/9: Creating system administration tables...'
\i system_administration.sql
\echo 'System administration schema completed.'
\echo ''

-- 9. Initial Data (MUST BE LAST - populates essential application data)
\echo 'Step 9/9: Loading initial application data...'
\i initial_data.sql
\echo 'Initial data loaded successfully.'
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

-- Count initial data records
\echo 'Initial data records:'
SELECT 
    'System Configurations' as data_type,
    COUNT(*) as record_count
FROM system_configurations
UNION ALL
SELECT 
    'Crisis Resources' as data_type,
    COUNT(*) as record_count
FROM crisis_resources
UNION ALL
SELECT 
    'Crisis Keywords' as data_type,
    COUNT(*) as record_count
FROM crisis_keywords
UNION ALL
SELECT 
    'AI Agent Configs' as data_type,
    COUNT(*) as record_count
FROM ai_agent_configs
UNION ALL
SELECT 
    'Journal Prompts' as data_type,
    COUNT(*) as record_count
FROM journal_prompts;

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
\echo 'For detailed verification, run the queries in README_SETUP.sql'
\echo '============================================================================='
