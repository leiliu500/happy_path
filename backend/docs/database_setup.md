# Happy Path Mental Health Application - Database Setup Guide

## 📋 Quick Start

This guide provides step-by-step instructions for setting up the Happy Path Mental Health Application database. The setup process is designed to be simple, reliable, and production-ready.

## ⚡ One-Command Setup (Recommended)

### **Prerequisites**
- PostgreSQL 12+ installed and running
- Database created and accessible
- Appropriate user permissions

### **Simple Setup**
```bash
# Navigate to the SQL directory
cd /path/to/happy_path/backend/sql

# Run the complete setup
psql -d your_database_name -f setup.sql
```

**That's it!** The setup script will:
- ✅ Install all required PostgreSQL extensions
- ✅ Create all database tables and relationships
- ✅ Set up utility functions and triggers
- ✅ Configure security policies
- ✅ Populate initial data
- ✅ Create performance indexes
- ✅ Verify the installation

---

## 🔧 Detailed Setup Instructions

### **Step 1: Environment Preparation**

#### **PostgreSQL Installation**
```bash
# macOS (using Homebrew)
brew install postgresql@14
brew services start postgresql@14

# Ubuntu/Debian
sudo apt update
sudo apt install postgresql-14 postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql14-server postgresql14-contrib
sudo postgresql-14-setup initdb
sudo systemctl start postgresql-14
```

#### **Database Creation**
```sql
-- Connect as superuser
psql -U postgres

-- Create database
CREATE DATABASE happy_path_mental_health;

-- Create application user
CREATE USER happy_path_user WITH PASSWORD 'secure_password_here';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE happy_path_mental_health TO happy_path_user;

-- Connect to the new database
\c happy_path_mental_health

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO happy_path_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO happy_path_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO happy_path_user;
```

### **Step 2: File Structure Overview**

```
backend/sql/
├── setup.sql                       # 🚀 Complete automated setup
└── schemas/                        # Individual schema files
    ├── 00_master_setup.sql         # Extensions and utilities
    ├── user_management.sql         # User accounts and auth
    ├── mood_tracking.sql           # Mood logging system
    ├── journaling.sql              # CBT journaling features
    ├── crisis_management.sql       # Crisis detection system
    ├── conversational_agent.sql    # AI chat functionality
    ├── clinical_therapy.sql        # Therapist integration
    ├── system_administration.sql   # Monitoring and auditing
    └── initial_data.sql            # Essential app data
```

### **Step 3: Manual Setup (Alternative)**

If you prefer to run individual files:

```bash
# Navigate to SQL directory
cd /path/to/happy_path/backend/sql

# Run files in order
psql -d happy_path_mental_health -f schemas/00_master_setup.sql
psql -d happy_path_mental_health -f schemas/user_management.sql
psql -d happy_path_mental_health -f schemas/mood_tracking.sql
psql -d happy_path_mental_health -f schemas/journaling.sql
psql -d happy_path_mental_health -f schemas/crisis_management.sql
psql -d happy_path_mental_health -f schemas/conversational_agent.sql
psql -d happy_path_mental_health -f schemas/clinical_therapy.sql
psql -d happy_path_mental_health -f schemas/system_administration.sql
psql -d happy_path_mental_health -f schemas/initial_data.sql
```

---

## 🔍 Setup Verification

### **Automated Verification**
The setup script includes built-in verification that checks:

- ✅ **Table Count**: Verifies all 20+ tables are created
- ✅ **Function Count**: Confirms all utility functions exist
- ✅ **Extension Check**: Validates PostgreSQL extensions
- ✅ **Initial Data**: Ensures reference data is populated
- ✅ **Index Creation**: Confirms performance indexes
- ✅ **Security Setup**: Validates RLS policies

### **Manual Verification Commands**

#### **Check Table Creation**
```sql
-- Count all tables
SELECT COUNT(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
-- Expected: 20+ tables

-- List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

#### **Verify Extensions**
```sql
-- Check installed extensions
SELECT extname, extversion 
FROM pg_extension 
WHERE extname IN ('uuid-ossp', 'pgcrypto', 'pg_trgm', 'btree_gin', 'unaccent');
-- Expected: 5 extensions
```

#### **Test Core Functions**
```sql
-- Test UUID generation
SELECT uuid_generate_v4();

-- Test email validation
SELECT is_valid_email('test@example.com'); -- Should return true
SELECT is_valid_email('invalid-email');    -- Should return false

-- Test mood trend calculation (after creating test data)
SELECT calculate_mood_trend(uuid_generate_v4(), 30);
```

#### **Check Initial Data**
```sql
-- Verify system configurations
SELECT COUNT(*) FROM system_configurations;
-- Expected: 10+ configurations

-- Check crisis resources
SELECT name, contact_info FROM crisis_resources LIMIT 5;

-- Verify AI agent configurations
SELECT name, personality_type FROM ai_agent_configurations;

-- Check journal prompts
SELECT COUNT(*) FROM journal_prompts;
-- Expected: 50+ prompts
```

#### **Test User Creation**
```sql
-- Test user insertion
INSERT INTO users (email, password_hash, role) 
VALUES ('test@example.com', 'hashed_password_here', 'patient');

-- Verify user was created
SELECT id, email, role, created_at FROM users WHERE email = 'test@example.com';

-- Clean up test user
DELETE FROM users WHERE email = 'test@example.com';
```

---

## 🚀 Performance Optimization

### **Recommended PostgreSQL Settings**

Add these settings to your `postgresql.conf`:

```ini
# Memory settings
shared_buffers = 256MB                    # 25% of RAM for dedicated server
effective_cache_size = 1GB                # 75% of RAM
work_mem = 4MB                            # Per operation memory
maintenance_work_mem = 64MB               # Maintenance operations

# Connection settings
max_connections = 200                     # Adjust based on application needs
shared_preload_libraries = 'pg_stat_statements'

# Logging settings
log_statement = 'mod'                     # Log modifications
log_min_duration_statement = 1000         # Log slow queries (1 second)
log_checkpoints = on
log_connections = on
log_disconnections = on

# Performance settings
random_page_cost = 1.1                    # SSD optimization
effective_io_concurrency = 200            # SSD concurrent I/O
```

### **Index Monitoring**
```sql
-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;
```

---

## 🔒 Security Configuration

### **Row-Level Security Setup**

The setup automatically enables RLS on sensitive tables:

```sql
-- Verify RLS is enabled
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables 
WHERE schemaname = 'public' AND rowsecurity = true;
```

### **User Role Configuration**

```sql
-- Create application roles
CREATE ROLE patient_role;
CREATE ROLE therapist_role;
CREATE ROLE admin_role;
CREATE ROLE system_role;

-- Grant appropriate permissions
GRANT SELECT, INSERT, UPDATE ON mood_entries TO patient_role;
GRANT SELECT, INSERT, UPDATE ON journal_entries TO patient_role;
GRANT SELECT ON crisis_resources TO patient_role;

-- Therapist permissions
GRANT patient_role TO therapist_role;
GRANT SELECT ON therapeutic_relationships TO therapist_role;
GRANT SELECT, INSERT, UPDATE ON clinical_sessions TO therapist_role;

-- Admin permissions
GRANT therapist_role TO admin_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin_role;
```

### **SSL Configuration**

Enable SSL in `postgresql.conf`:
```ini
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'ca.crt'
ssl_crl_file = 'server.crl'
```

---

## 🛠️ Maintenance and Monitoring

### **Regular Maintenance Tasks**

#### **Daily Tasks**
```sql
-- Update table statistics
ANALYZE;

-- Check for long-running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query 
FROM pg_stat_activity 
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';
```

#### **Weekly Tasks**
```sql
-- Vacuum and analyze all tables
VACUUM ANALYZE;

-- Check database size
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database;

-- Monitor index bloat
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

#### **Monthly Tasks**
```sql
-- Full vacuum (if needed)
VACUUM FULL;

-- Reindex if necessary
REINDEX DATABASE happy_path_mental_health;

-- Archive old audit logs
SELECT cleanup_expired_data();
```

### **Monitoring Queries**

#### **Performance Monitoring**
```sql
-- Top 10 slowest queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Database connections
SELECT 
    count(*) as active_connections,
    state
FROM pg_stat_activity 
GROUP BY state;

-- Table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY size_bytes DESC;
```

---

## 🚨 Troubleshooting

### **Common Issues and Solutions**

#### **Issue: Extension Installation Fails**
```sql
-- Check if extensions are available
SELECT name FROM pg_available_extensions WHERE name IN 
    ('uuid-ossp', 'pgcrypto', 'pg_trgm', 'btree_gin', 'unaccent');

-- Install as superuser if needed
\c postgres postgres
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Repeat for other extensions
```

#### **Issue: Permission Denied**
```sql
-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE happy_path_mental_health TO happy_path_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO happy_path_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO happy_path_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO happy_path_user;
```

#### **Issue: Function Dependencies**
If you encounter function dependency issues:
```bash
# Run setup in correct order
psql -d happy_path_mental_health -f schemas/00_master_setup.sql  # FIRST
psql -d happy_path_mental_health -f schemas/user_management.sql  # SECOND
# Then other files...
```

#### **Issue: Table Already Exists**
```sql
-- Drop and recreate if needed (CAUTION: Data loss)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- Re-run setup
```

### **Log Analysis**

#### **Check PostgreSQL Logs**
```bash
# Find log location
sudo -u postgres psql -c "SHOW log_directory;"
sudo -u postgres psql -c "SHOW log_filename;"

# View recent logs
tail -f /var/log/postgresql/postgresql-14-main.log
```

#### **Application Error Patterns**
```sql
-- Check for recent errors in audit logs
SELECT 
    action,
    table_name,
    timestamp,
    new_values
FROM audit_logs 
WHERE action LIKE '%ERROR%' 
ORDER BY timestamp DESC 
LIMIT 10;
```

---

## 🔄 Backup and Recovery

### **Backup Strategy**

#### **Daily Backups**
```bash
#!/bin/bash
# daily_backup.sh

DB_NAME="happy_path_mental_health"
BACKUP_DIR="/backups/daily"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump -h localhost -U happy_path_user -d $DB_NAME > \
    $BACKUP_DIR/happy_path_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/happy_path_backup_$DATE.sql

# Remove backups older than 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
```

#### **Full System Backup**
```bash
# Physical backup
pg_basebackup -h localhost -U postgres -D /backups/physical -Ft -z -P

# Logical backup with data
pg_dump -h localhost -U happy_path_user -d happy_path_mental_health \
    --format=custom --compress=9 > happy_path_full.backup
```

### **Recovery Procedures**

#### **Restore from Backup**
```bash
# Drop and recreate database
dropdb happy_path_mental_health
createdb happy_path_mental_health

# Restore from SQL backup
psql -d happy_path_mental_health < backup_file.sql

# Restore from custom format
pg_restore -d happy_path_mental_health backup_file.backup
```

---

## 📞 Support and Resources

### **Documentation References**
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [HIPAA Compliance Guidelines](https://www.hhs.gov/hipaa/)
- [Database Security Best Practices](https://www.postgresql.org/docs/current/security.html)

### **Development Team Contacts**
- **Database Team**: db-team@happypath.com
- **DevOps Team**: devops@happypath.com
- **Security Team**: security@happypath.com

### **Emergency Procedures**
For critical database issues:
1. Contact the on-call database administrator
2. Check the monitoring dashboard
3. Review recent logs for error patterns
4. Follow the incident response protocol

---

*This setup guide is maintained as part of the Happy Path Mental Health Application project. For questions, updates, or issues, please contact the development team or create an issue in the project repository.*
