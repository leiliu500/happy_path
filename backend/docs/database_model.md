# Happy Path Mental Health Application - Database Model Documentation

## 📋 Overview

This document provides a comprehensive overview of the database model for the Happy Path Mental Health Application. The database is designed to support a professional-grade mental health platform with mood tracking, journaling, crisis management, AI-powered conversations, and clinical therapy integration.

## 🏗️ Architecture Overview

### **Database Technology**
- **Platform**: PostgreSQL 12+
- **Extensions**: uuid-ossp, pgcrypto, pg_trgm, btree_gin, unaccent
- **Security**: Row-Level Security (RLS) enabled
- **Performance**: Optimized indexes and query patterns

### **Design Principles**
- **HIPAA Compliance**: Privacy-first design with audit trails
- **Scalability**: Optimized for high user volumes
- **Modularity**: Clear separation of concerns across schemas
- **Security**: Multi-layered security with encryption and RLS

## 📊 Schema Overview

The database consists of 8 main schema modules:

| Schema | Tables | Primary Purpose |
|--------|--------|----------------|
| **User Management** | 5 tables | Authentication, profiles, consent |
| **Mood Tracking** | 5 tables | Daily mood logging and analytics |
| **Journaling** | 4 tables | CBT-guided journaling system |
| **Crisis Management** | 5 tables | Crisis detection and intervention |
| **Conversational Agent** | 4 tables | AI chat functionality |
| **Clinical Therapy** | 6 tables | Therapist-patient relationships |
| **System Administration** | 4 tables | Monitoring and compliance |
| **Initial Data** | 6 tables | Essential application data |

---

## 🔐 User Management Schema

### **Core Tables**

#### `users` - Primary User Accounts
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'patient',
    account_status account_status_enum NOT NULL DEFAULT 'pending_verification',
    email_verified BOOLEAN DEFAULT FALSE,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- UUID primary keys for security
- Role-based access (patient, therapist, admin, system)
- Account status tracking
- Two-factor authentication support

#### `user_profiles` - Extended User Information
- Personal demographics and preferences
- Timezone and language settings
- Emergency contact information
- Privacy preferences

#### `user_sessions` - Authentication Management
- Active session tracking
- Device and location logging
- Session expiration management
- Security monitoring

#### `consent_tracking` - HIPAA Compliance
- Consent version tracking
- Withdrawal management
- Audit trail for legal compliance

#### `user_preferences` - Application Settings
- Notification preferences
- Privacy settings
- Customization options

---

## 📈 Mood Tracking Schema

### **Core Tables**

#### `mood_entries` - Daily Mood Logs
```sql
CREATE TABLE mood_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    entry_date DATE NOT NULL,
    overall_mood mood_scale_domain NOT NULL, -- 1-10 scale
    energy_level mood_scale_domain,
    anxiety_level mood_scale_domain,
    stress_level mood_scale_domain,
    sleep_hours DECIMAL(3,1),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- 1-10 scale mood tracking
- Multiple mood dimensions
- Sleep tracking integration
- Daily entry constraints

#### `mood_patterns` - Analytics and Insights
- Automated pattern detection
- Trend analysis
- Correlation insights
- Predictive analytics

#### `mood_goals` - Goal Setting and Tracking
- Personal mood targets
- Progress tracking
- Achievement celebrations
- Adaptive goal adjustment

#### `mood_insights` - AI-Generated Analysis
- Weekly/monthly summaries
- Pattern recognition
- Recommendation generation
- Trend predictions

#### `mood_analytics` - Aggregated Statistics
- Population-level insights
- Anonymized benchmarks
- Research data support
- Quality metrics

---

## 📝 Journaling Schema

### **Core Tables**

#### `journal_entries` - CBT-Guided Entries
```sql
CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content TEXT NOT NULL,
    mood_before mood_scale_domain,
    mood_after mood_scale_domain,
    cbt_technique cbt_technique_enum,
    privacy_level privacy_level_enum DEFAULT 'private',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- Before/after mood tracking
- CBT technique integration
- Privacy level controls
- Rich text content support

#### `journal_prompts` - Therapeutic Prompts
- Curated therapeutic questions
- CBT-based exercises
- Daily reflection starters
- Crisis-specific prompts

#### `gratitude_entries` - Positive Psychology
- Daily gratitude practice
- Appreciation tracking
- Positive memory collection
- Mindfulness exercises

#### `thought_records` - CBT Thought Analysis
- Automatic thought capture
- Cognitive distortion identification
- Balanced thought development
- Evidence examination

---

## 🚨 Crisis Management Schema

### **Core Tables**

#### `crisis_detections` - AI-Powered Detection
```sql
CREATE TABLE crisis_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_source crisis_source_enum NOT NULL,
    content_text TEXT NOT NULL,
    crisis_score normalized_score_domain NOT NULL,
    detected_keywords JSONB,
    risk_level crisis_level_enum NOT NULL,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- Multi-source crisis detection
- AI-powered risk scoring
- Keyword analysis
- Real-time alerting

#### `crisis_keywords` - Detection Library
- Suicide risk indicators
- Self-harm language patterns
- Emotional distress signals
- Contextual modifiers

#### `crisis_escalations` - Intervention Workflow
- Human review process
- Escalation protocols
- Response tracking
- Outcome monitoring

#### `safety_plans` - Crisis Preparation
- Personalized safety strategies
- Emergency contacts
- Coping mechanism lists
- Warning sign identification

#### `crisis_resources` - Support Network
- Hotline information
- Local resources
- Emergency services
- Professional contacts

---

## 🤖 Conversational Agent Schema

### **Core Tables**

#### `chat_sessions` - AI Conversation Management
```sql
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES ai_agent_configurations(id),
    session_name VARCHAR(255),
    session_mood mood_scale_domain,
    session_goal TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- Multi-agent support
- Session context management
- Mood-aware conversations
- Goal-oriented interactions

#### `chat_messages` - Conversation History
- Message threading
- Sentiment analysis
- Response timing
- Context preservation

#### `ai_agent_configurations` - Agent Personalities
- Therapeutic approach customization
- Response style settings
- Specialty focus areas
- Interaction boundaries

#### `conversation_analytics` - Usage Insights
- Engagement metrics
- Effectiveness tracking
- User satisfaction
- Improvement recommendations

---

## 🏥 Clinical Therapy Schema

### **Core Tables**

#### `therapeutic_relationships` - Therapist-Patient Connections
```sql
CREATE TABLE therapeutic_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    therapist_id UUID NOT NULL REFERENCES users(id),
    patient_id UUID NOT NULL REFERENCES users(id),
    relationship_type therapy_type_enum NOT NULL,
    status relationship_status_enum DEFAULT 'active',
    start_date DATE NOT NULL,
    end_date DATE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- Multiple therapy types
- Relationship lifecycle management
- Professional boundaries
- Progress tracking

#### `treatment_plans` - Structured Care Plans
- Goal-oriented treatment
- Progress milestones
- Intervention strategies
- Outcome measurements

#### `clinical_sessions` - Session Management
- Appointment scheduling
- Session documentation
- Progress notes
- Billing integration

#### `clinical_assessments` - Standardized Evaluations
- PHQ-9, GAD-7 integration
- Custom assessment tools
- Progress monitoring
- Risk assessment

#### `therapist_notes` - Professional Documentation
- Session summaries
- Treatment observations
- Intervention notes
- Care coordination

#### `clinical_outcomes` - Treatment Effectiveness
- Goal achievement tracking
- Symptom improvement
- Quality of life measures
- Treatment satisfaction

---

## ⚙️ System Administration Schema

### **Core Tables**

#### `audit_logs` - Comprehensive Activity Tracking
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- Complete audit trail
- HIPAA compliance support
- Data change tracking
- Security monitoring

#### `performance_metrics` - System Monitoring
- Response time tracking
- Resource utilization
- Error rate monitoring
- User experience metrics

#### `data_retention_policies` - Compliance Management
- Automated data lifecycle
- Privacy law compliance
- Retention scheduling
- Secure deletion

#### `privacy_compliance` - Regulatory Adherence
- HIPAA audit support
- Privacy breach tracking
- Consent management
- Data protection monitoring

---

## 📋 Initial Data Schema

### **Reference Tables**

#### `system_configurations` - Application Settings
- Feature flags
- System parameters
- Integration settings
- Maintenance windows

#### `crisis_resources` - Emergency Information
- National hotlines
- Local resources
- Emergency contacts
- Crisis protocols

#### `journal_prompts` - Therapeutic Content
- Daily reflection questions
- CBT exercises
- Mindfulness prompts
- Crisis-specific guidance

#### `ai_agent_configurations` - Chatbot Personalities
- Therapeutic styles
- Response patterns
- Specialty areas
- Interaction rules

## 🔧 Technical Implementation

### **Performance Optimizations**

#### **Strategic Indexing**
```sql
-- User lookup optimization
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Time-based queries
CREATE INDEX idx_mood_entries_user_date ON mood_entries(user_id, entry_date DESC);
CREATE INDEX idx_journal_entries_user_date ON journal_entries(user_id, created_at DESC);

-- Crisis detection optimization
CREATE INDEX idx_crisis_detections_score ON crisis_detections(crisis_score DESC);
CREATE INDEX idx_crisis_escalations_status ON crisis_escalations(status);
```

#### **Database Configuration**
- Connection pooling optimization
- Query plan caching
- Statistics collection
- Maintenance automation

### **Security Implementation**

#### **Row-Level Security (RLS)**
```sql
-- User data isolation
ALTER TABLE mood_entries ENABLE ROW LEVEL SECURITY;
CREATE POLICY mood_entries_user_policy ON mood_entries
    FOR ALL TO authenticated_user
    USING (user_id = current_user_id());

-- Therapist access controls
CREATE POLICY therapeutic_access_policy ON journal_entries
    FOR SELECT TO therapist_role
    USING (user_id IN (
        SELECT patient_id FROM therapeutic_relationships 
        WHERE therapist_id = current_user_id() AND status = 'active'
    ));
```

#### **Data Encryption**
- Column-level encryption for sensitive data
- Transport layer security
- At-rest encryption
- Key management integration

### **Compliance Features**

#### **HIPAA Compliance**
- Complete audit logging
- Data access controls
- Breach detection
- Privacy impact assessments

#### **Data Retention**
```sql
-- Automated cleanup procedures
CREATE OR REPLACE FUNCTION cleanup_expired_data()
RETURNS VOID AS $$
BEGIN
    -- Remove old session data
    DELETE FROM user_sessions 
    WHERE expires_at < CURRENT_TIMESTAMP - INTERVAL '30 days';
    
    -- Archive old audit logs
    INSERT INTO audit_logs_archive 
    SELECT * FROM audit_logs 
    WHERE timestamp < CURRENT_TIMESTAMP - INTERVAL '7 years';
END;
$$ LANGUAGE plpgsql;
```

## 📈 Scalability Considerations

### **Database Partitioning**
- Time-based partitioning for logs
- User-based partitioning for large tables
- Automatic partition management

### **Caching Strategy**
- Redis integration for session data
- Query result caching
- Static data caching

### **Monitoring and Alerting**
- Real-time performance monitoring
- Automated alerting systems
- Capacity planning metrics

## 🚀 Future Enhancements

### **Planned Features**
- Machine learning model integration
- Advanced analytics dashboards
- Wearable device integration
- Telemedicine platform support

### **Scalability Roadmap**
- Microservices architecture support
- Multi-tenant capabilities
- Global deployment optimization
- Advanced caching layers

---

## 📚 Related Documentation

- [Database Setup Guide](./database_setup.md)
- [API Documentation](./api_documentation.md)
- [Security Guidelines](./security_guidelines.md)
- [Compliance Manual](./compliance_manual.md)

---

*This documentation is maintained as part of the Happy Path Mental Health Application project. For questions or updates, please contact the development team.*
