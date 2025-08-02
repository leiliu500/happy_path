-- =============================================================================
-- HAPPY PATH MENTAL HEALTH APPLICATION - COMPLETE DATABASE SETUP
-- =============================================================================
-- This file sets up the entire database schema and initial data
-- Run this file to create a complete, production-ready mental health database
--
-- Usage: psql -d your_database -f setup.sql
-- =============================================================================

\echo 'Starting Happy Path Mental Health Database Setup...'
\echo ''

-- =============================================================================
-- STEP 1: MASTER SETUP (Extensions, Functions, and Utilities)
-- =============================================================================

\echo '🔧 Setting up PostgreSQL extensions and utility functions...'

\i schemas/00_master_setup.sql

\echo '✅ Master setup completed'
\echo ''

-- =============================================================================
-- STEP 2: CORE SCHEMA FILES (User Management First)
-- =============================================================================

\echo '👥 Setting up user management and authentication...'

\i schemas/user_management.sql

\echo '✅ User management schema completed'
\echo ''

-- =============================================================================
-- STEP 3: USER DATA SCHEMAS (Mood, Journaling, Crisis)
-- =============================================================================

\echo '📊 Setting up mood tracking system...'

\i schemas/mood_tracking.sql

\echo '✅ Mood tracking schema completed'
\echo ''

\echo '📝 Setting up journaling and CBT features...'

\i schemas/journaling.sql

\echo '✅ Journaling schema completed'
\echo ''

\echo '🚨 Setting up crisis management system...'

\i schemas/crisis_management.sql

\echo '✅ Crisis management schema completed'
\echo ''

-- =============================================================================
-- STEP 4: AI AND THERAPY FEATURES
-- =============================================================================

\echo '🤖 Setting up conversational AI agent...'

\i schemas/conversational_agent.sql

\echo '✅ Conversational agent schema completed'
\echo ''

\echo '🏥 Setting up clinical therapy features...'

\i schemas/clinical_therapy.sql

\echo '✅ Clinical therapy schema completed'
\echo ''

-- =============================================================================
-- STEP 5: SYSTEM ADMINISTRATION AND MONITORING
-- =============================================================================

\echo '⚙️ Setting up system administration and monitoring...'

\i schemas/system_administration.sql

\echo '✅ System administration schema completed'
\echo ''

-- =============================================================================
-- STEP 6: INITIAL DATA POPULATION
-- =============================================================================

\echo '📋 Populating initial system data...'

\i schemas/initial_data.sql

\echo '✅ Initial data population completed'
\echo ''

-- =============================================================================
-- STEP 7: POST-SETUP VERIFICATION AND OPTIMIZATION
-- =============================================================================

\echo '🔍 Running post-setup verification...'

-- Verify table creation
DO $$
DECLARE
    table_count INTEGER;
    function_count INTEGER;
    extension_count INTEGER;
BEGIN
    -- Count tables
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    
    -- Count functions
    SELECT COUNT(*) INTO function_count
    FROM information_schema.routines 
    WHERE routine_schema = 'public' AND routine_type = 'FUNCTION';
    
    -- Count extensions
    SELECT COUNT(*) INTO extension_count
    FROM pg_extension 
    WHERE extname IN ('uuid-ossp', 'pgcrypto', 'pg_trgm', 'btree_gin', 'unaccent');
    
    RAISE NOTICE 'Database Setup Verification:';
    RAISE NOTICE '  📊 Tables created: %', table_count;
    RAISE NOTICE '  ⚙️ Functions created: %', function_count;
    RAISE NOTICE '  🔧 Extensions installed: %', extension_count;
    
    IF table_count >= 20 THEN
        RAISE NOTICE '  ✅ Table creation: PASSED';
    ELSE
        RAISE NOTICE '  ❌ Table creation: FAILED (Expected 20+, got %)', table_count;
    END IF;
    
    IF function_count >= 10 THEN
        RAISE NOTICE '  ✅ Function creation: PASSED';
    ELSE
        RAISE NOTICE '  ❌ Function creation: FAILED (Expected 10+, got %)', function_count;
    END IF;
    
    IF extension_count = 5 THEN
        RAISE NOTICE '  ✅ Extension installation: PASSED';
    ELSE
        RAISE NOTICE '  ❌ Extension installation: FAILED (Expected 5, got %)', extension_count;
    END IF;
END;
$$;

-- Verify initial data population
DO $$
DECLARE
    config_count INTEGER;
    resource_count INTEGER;
    prompt_count INTEGER;
    agent_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO config_count FROM system_configurations;
    SELECT COUNT(*) INTO resource_count FROM crisis_resources;
    SELECT COUNT(*) INTO prompt_count FROM journal_prompts;
    SELECT COUNT(*) INTO agent_count FROM ai_agent_configurations;
    
    RAISE NOTICE '';
    RAISE NOTICE 'Initial Data Verification:';
    RAISE NOTICE '  ⚙️ System configurations: %', config_count;
    RAISE NOTICE '  🚨 Crisis resources: %', resource_count;
    RAISE NOTICE '  📝 Journal prompts: %', prompt_count;
    RAISE NOTICE '  🤖 AI agent configs: %', agent_count;
    
    IF config_count > 0 AND resource_count > 0 AND prompt_count > 0 AND agent_count > 0 THEN
        RAISE NOTICE '  ✅ Initial data population: PASSED';
    ELSE
        RAISE NOTICE '  ❌ Initial data population: FAILED';
    END IF;
END;
$$;

-- Create database-wide indexes for performance
\echo '🚀 Creating performance indexes...'

-- User-related indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(account_status);
CREATE INDEX IF NOT EXISTS idx_users_created ON users(created_at);

-- Mood tracking indexes
CREATE INDEX IF NOT EXISTS idx_mood_entries_user_date ON mood_entries(user_id, entry_date DESC);
CREATE INDEX IF NOT EXISTS idx_mood_entries_overall ON mood_entries(overall_mood);
CREATE INDEX IF NOT EXISTS idx_mood_goals_user_active ON mood_goals(user_id, is_active);

-- Journal indexes
CREATE INDEX IF NOT EXISTS idx_journal_entries_user_date ON journal_entries(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_journal_entries_mood ON journal_entries(mood_before, mood_after);

-- Crisis management indexes
CREATE INDEX IF NOT EXISTS idx_crisis_detections_user_date ON crisis_detections(user_id, detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_crisis_detections_score ON crisis_detections(crisis_score DESC);
CREATE INDEX IF NOT EXISTS idx_crisis_escalations_status ON crisis_escalations(status);

-- Conversation indexes
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_date ON chat_sessions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_time ON chat_messages(session_id, sent_at);

-- Clinical therapy indexes
CREATE INDEX IF NOT EXISTS idx_therapeutic_relationships_therapist ON therapeutic_relationships(therapist_id);
CREATE INDEX IF NOT EXISTS idx_therapeutic_relationships_patient ON therapeutic_relationships(patient_id);
CREATE INDEX IF NOT EXISTS idx_clinical_sessions_date ON clinical_sessions(session_date DESC);

-- System administration indexes
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_action ON audit_logs(user_id, action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp DESC);

\echo '✅ Performance indexes created'

-- Set up row-level security policies
\echo '🔒 Configuring row-level security...'

-- Enable RLS on sensitive tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE mood_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE journal_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE crisis_detections ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE therapeutic_relationships ENABLE ROW LEVEL SECURITY;

\echo '✅ Row-level security configured'

-- Final database optimization
\echo '⚡ Running database optimization...'

-- Update table statistics
ANALYZE;

-- Set optimal configuration parameters
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET track_activity_query_size = 2048;
ALTER SYSTEM SET log_min_duration_statement = 1000;
ALTER SYSTEM SET log_checkpoints = on;
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;

\echo '✅ Database optimization completed'
\echo ''

-- =============================================================================
-- SETUP COMPLETION SUMMARY
-- =============================================================================

\echo '🎉 HAPPY PATH DATABASE SETUP COMPLETED SUCCESSFULLY!'
\echo ''
\echo '📋 Setup Summary:'
\echo '   ✅ PostgreSQL extensions installed'
\echo '   ✅ Utility functions created'
\echo '   ✅ User management system ready'
\echo '   ✅ Mood tracking system configured'
\echo '   ✅ Journaling and CBT features active'
\echo '   ✅ Crisis management system enabled'
\echo '   ✅ AI conversational agent ready'
\echo '   ✅ Clinical therapy features available'
\echo '   ✅ System monitoring configured'
\echo '   ✅ Initial data populated'
\echo '   ✅ Performance indexes created'
\echo '   ✅ Security policies enabled'
\echo ''
\echo '🚀 Your mental health application database is ready for production use!'
\echo ''
\echo '📚 Next Steps:'
\echo '   1. Configure your application connection strings'
\echo '   2. Set up backup and monitoring procedures'
\echo '   3. Create your first admin user account'
\echo '   4. Review and customize AI agent personalities'
\echo '   5. Configure crisis escalation contacts'
\echo ''
\echo '🔍 To verify the setup, run:'
\echo '   SELECT COUNT(*) FROM users; -- Should allow user creation'
\echo '   SELECT * FROM system_configurations; -- Should show config data'
\echo '   SELECT name FROM ai_agent_configurations; -- Should show AI agents'
\echo ''

-- =============================================================================
-- END OF SETUP
-- =============================================================================
