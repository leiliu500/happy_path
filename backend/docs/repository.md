# Mental Health Wellness Platform Repository Documentation

## Overview

The Mental Health Wellness Platform Repository system provides a comprehensive data access layer for a professional mental health platform. It implements the repository pattern to provide clean separation between business logic and data access, with specialized repositories for clinical workflows, patient engagement, crisis management, and care coordination.

## Architecture

### Repository Pattern Benefits

- **Separation of Concerns**: Clean separation between business logic and data access
- **Testability**: Easy mocking and unit testing
- **Consistency**: Standardized interface across all data operations
- **Maintainability**: Centralized data access logic
- **Flexibility**: Easy to switch between different data sources

### Base Repository Classes

#### `BaseRepository<T, K>`
Generic base repository providing common CRUD operations:
- `create(entity: T) -> T`
- `get_by_id(id: K) -> Optional[T]`
- `update(entity: T) -> T`
- `delete(id: K) -> bool`
- `list_all(options: QueryOptions) -> QueryResult[T]`

#### `AsyncBaseRepository<T, K>`
Asynchronous version for high-performance scenarios.

## Clinical Repositories

### Therapeutic Relationship Repository

Manages the relationship between patients and therapists.

```python
from backend.happypath.repository import create_therapeutic_relationship_repository

# Create repository
repo = create_therapeutic_relationship_repository(db_manager, logger)

# Establish therapeutic relationship
relationship = TherapeuticRelationship(
    patient_id="patient_123",
    therapist_id="therapist_456",
    therapy_modality=TherapyModality.CBT,
    relationship_status="active",
    start_date=date.today(),
    treatment_focus=["Depression", "Anxiety"]
)
relationship = repo.create(relationship)
```

**Key Features:**
- Therapy modality tracking (CBT, DBT, Psychodynamic, etc.)
- Session frequency management
- Treatment focus areas
- Relationship status monitoring
- Professional boundaries documentation

### Treatment Plan Repository

Manages comprehensive treatment planning and progress tracking.

```python
# Create treatment plan
treatment_plan = TreatmentPlan(
    patient_id="patient_123",
    therapist_id="therapist_456",
    plan_name="CBT for Depression",
    primary_diagnosis="Major Depressive Disorder",
    treatment_goals=["Reduce depressive symptoms", "Improve coping skills"],
    interventions=["Cognitive restructuring", "Behavioral activation"],
    estimated_duration_weeks=16,
    phase=TreatmentPhase.ACTIVE
)
plan = repo.create(treatment_plan)

# Track progress
progress = repo.update_treatment_progress(
    plan_id=plan.plan_id,
    goals_progress={"goal_1": 75, "goal_2": 60},
    phase_notes="Good progress on cognitive techniques"
)
```

**Key Features:**
- Evidence-based treatment planning
- Goal setting and progress tracking
- Intervention documentation
- Outcome measurement
- Treatment phase management

### Therapy Session Repository

Documents individual therapy sessions with clinical notes and assessments.

```python
# Document therapy session
session = TherapySession(
    relationship_id=relationship.relationship_id,
    patient_id="patient_123",
    therapist_id="therapist_456",
    session_date=date.today(),
    session_type="individual",
    duration_minutes=50,
    session_notes="Patient showed significant progress in thought challenging",
    interventions_used=["Cognitive restructuring", "Homework review"],
    patient_mood_start=4,
    patient_mood_end=7,
    risk_assessment="low",
    homework_assigned=["Daily thought record", "Mood tracking"]
)
session = repo.create(session)
```

**Key Features:**
- Comprehensive session documentation
- Risk assessment tracking
- Intervention recording
- Mood change documentation
- Homework assignment management

## Patient Engagement Repositories

### Mood Tracking Repository

Tracks patient mood patterns and provides analytics.

```python
# Log mood entry
mood_entry = MoodEntry(
    user_id="patient_123",
    mood_scale=MoodScale.ONE_TO_TEN,
    mood_rating=7,
    mood_type=MoodType.GENERAL,
    contributing_factors=["Good sleep", "Exercise"],
    triggers=["Work stress"],
    notes="Feeling more balanced today"
)
mood = repo.create(mood_entry)

# Analyze patterns
trends = repo.analyze_mood_trends(
    user_id="patient_123",
    days_back=30
)
```

**Key Features:**
- Multiple mood scales (1-10, 1-5, emotional states)
- Factor and trigger tracking
- Pattern analysis and insights
- Goal setting and progress monitoring
- Correlation analysis with other metrics

### Journaling Repository

Manages therapeutic journaling with CBT technique integration.

```python
# Create journal entry with CBT technique
journal_entry = JournalEntry(
    user_id="patient_123",
    title="Thought Challenging Exercise",
    content="Today I practiced questioning my negative thoughts...",
    journal_type=JournalType.THERAPEUTIC,
    cbt_technique=CBTTechnique.THOUGHT_RECORD,
    mood_before=4,
    mood_after=7,
    insights=["I can control my thoughts"],
    tags=["anxiety", "thought-challenging"]
)
entry = repo.create(journal_entry)

# AI sentiment analysis (automatically triggered)
sentiment = repo.analyze_sentiment(entry.entry_id)
```

**Key Features:**
- CBT technique integration
- AI sentiment analysis
- Crisis indicator detection
- Personalized prompts
- Therapeutic writing exercises

## Crisis Management Repositories

### Crisis Detection Repository

Automated crisis detection and escalation management.

```python
# Crisis detection (usually automated)
crisis = CrisisDetection(
    patient_id="patient_123",
    detection_source="journal_entry",
    crisis_type="suicidal_ideation",
    severity_level="high",
    detected_keywords=["hopeless", "ending it all"],
    confidence_score=0.95,
    requires_immediate_attention=True
)
detection = repo.create(crisis)

# Escalate crisis
escalation = repo.escalate_crisis(
    detection_id=detection.detection_id,
    escalated_to="crisis_team",
    escalation_reason="High-risk suicidal ideation detected"
)
```

**Key Features:**
- Keyword-based detection
- Machine learning risk assessment
- Automatic escalation protocols
- Professional notification system
- Response time tracking

### Safety Plan Repository

Manages comprehensive safety plans for crisis situations.

```python
# Create safety plan
safety_plan = SafetyPlan(
    patient_id="patient_123",
    created_by_provider_id="therapist_456",
    warning_signs=["Feeling hopeless", "Social isolation"],
    coping_strategies=["Deep breathing", "Call friend"],
    social_contacts=[
        {"name": "Sister", "phone": "(555) 123-4567"}
    ],
    professional_contacts=[
        {"name": "Crisis Hotline", "phone": "988"}
    ],
    environmental_safety=["Remove harmful objects"],
    reasons_to_live=["Family", "Future goals"]
)
plan = repo.create(safety_plan)
```

**Key Features:**
- Comprehensive safety planning
- Emergency contact management
- Coping strategy documentation
- Environmental safety assessment
- Reasons for living exploration

## Operational Repositories

### Appointment Repository

Manages appointment scheduling and provider calendars.

```python
# Check availability
is_available = repo.check_availability(
    provider_id="therapist_456",
    start_time=datetime(2024, 12, 15, 10, 0),
    duration_minutes=50
)

# Schedule appointment
appointment = Appointment(
    provider_id="therapist_456",
    patient_id="patient_123",
    appointment_type=AppointmentType.THERAPY_SESSION,
    scheduled_start=datetime(2024, 12, 15, 10, 0),
    modality=AppointmentModality.TELEHEALTH,
    agenda=["Review progress", "CBT techniques"]
)
appointment = repo.create(appointment)

# Send reminders
reminders = repo.send_appointment_reminders(
    appointment_id=appointment.appointment_id,
    reminder_types=[ReminderType.EMAIL, ReminderType.SMS]
)
```

**Key Features:**
- Provider calendar management
- Availability checking
- Multiple appointment types
- Automated reminders
- Cancellation and rescheduling

### Medication Repository

Comprehensive medication management and adherence tracking.

```python
# Add medication
medication = Medication(
    patient_id="patient_123",
    medication_name="Sertraline",
    strength="50mg",
    prescribed_dosage="50mg once daily",
    start_date=date.today(),
    indication="Major Depressive Disorder"
)
med = repo.create(medication)

# Track adherence
adherence = repo.calculate_adherence(
    patient_id="patient_123",
    period_days=30
)

# Generate adherence report
report = repo.generate_adherence_report(
    patient_id="patient_123",
    start_date=date.today() - timedelta(days=30),
    end_date=date.today()
)
```

**Key Features:**
- Prescription management
- Adherence tracking and calculation
- Side effect monitoring
- Drug interaction checking
- Refill scheduling

## Communication Repositories

### Conversational Agent Repository

Manages AI chatbot interactions and conversation analytics.

```python
# Start conversation
conversation = repo.start_conversation(
    user_id="patient_123",
    conversation_type=ConversationType.MOOD_CHECK_IN,
    title="Daily Check-in"
)

# Add messages
message = repo.add_message(
    conversation_id=conversation.conversation_id,
    content="I'm feeling anxious today",
    sender=MessageSender.USER
)

# AI response with intent recognition
response = repo.generate_ai_response(
    conversation_id=conversation.conversation_id,
    user_message=message
)
```

**Key Features:**
- Intent recognition and response generation
- Crisis detection in conversations
- Conversation analytics
- Multi-modal communication support
- User satisfaction tracking

## Administration Repositories

### User Account Repository

Manages user accounts with role-based access control.

```python
# Create user account
user = repo.create_user(
    username="john.doe",
    email="john@example.com",
    password_hash="hashed_password",
    role=UserRole.PATIENT
)

# Manage authentication
authenticated = repo.authenticate_user(
    email="john@example.com",
    password="password"
)

# Track security events
repo.log_security_event(
    user_id=user.user_id,
    event_type="login_attempt",
    success=True,
    ip_address="192.168.1.100"
)
```

**Key Features:**
- Role-based access control
- Multi-factor authentication support
- Security event logging
- License management for providers
- Session management

### Audit Log Repository

Comprehensive audit logging for compliance and security.

```python
# Log audit event
audit = repo.log_action(
    user_id="user_123",
    action_type=ActionType.UPDATE,
    resource_type="patient_record",
    resource_id="patient_456",
    description="Updated treatment plan",
    hipaa_relevant=True,
    old_values={"status": "draft"},
    new_values={"status": "active"}
)

# Generate compliance report
report = repo.get_hipaa_relevant_logs(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31)
)
```

**Key Features:**
- HIPAA-compliant logging
- Security event tracking
- Data change auditing
- Compliance reporting
- Failed action monitoring

## Care Coordination Repositories

### Provider Repository

Manages healthcare provider network and credentials.

```python
# Add provider
provider = Provider(
    first_name="Dr. Sarah",
    last_name="Johnson",
    provider_type=ProviderType.PSYCHIATRIST,
    license_number="MD12345",
    specialty="Adult Psychiatry",
    accepting_new_patients=True
)
provider = repo.create(provider)

# Find providers by specialty
psychiatrists = repo.find_providers_by_specialty(
    specialty="Adult Psychiatry",
    accepting_patients=True
)
```

**Key Features:**
- Provider credentialing
- Specialty and subspecialty tracking
- Network status management
- Availability tracking
- License expiration monitoring

### Referral Repository

Manages referrals between providers with tracking and outcomes.

```python
# Create referral
referral = repo.create_referral(
    patient_id="patient_123",
    referring_provider_id="therapist_456",
    receiving_provider_id="psychiatrist_789",
    referral_reason="Medication evaluation",
    priority=ReferralPriority.ROUTINE
)

# Track referral status
repo.update_referral_status(
    referral_id=referral.referral_id,
    status=ReferralStatus.ACCEPTED,
    notes="Appointment scheduled for next week"
)
```

**Key Features:**
- Referral workflow management
- Status tracking and notifications
- Outcome documentation
- Authorization management
- Communication tracking

### Care Team Repository

Manages multidisciplinary care teams.

```python
# Create care team
team = CareTeam(
    patient_id="patient_123",
    primary_provider_id="therapist_456",
    shared_goals=["Symptom reduction", "Improved functioning"],
    treatment_approach="Integrated therapy and medication"
)
team = repo.create(team)

# Add team member
repo.add_team_member(
    team_id=team.team_id,
    provider_id="psychiatrist_789",
    role=CareTeamRole.PSYCHIATRIST
)
```

**Key Features:**
- Team composition management
- Shared goal setting
- Communication planning
- Meeting coordination
- Role-based responsibilities

## Query System

### QueryOptions

Powerful querying interface for complex data retrieval:

```python
from backend.happypath.repository import QueryOptions

# Complex query example
options = QueryOptions(
    filters={
        'user_id': 'patient_123',
        'mood_rating__gte': 7,  # Mood rating >= 7
        'created_at__gte': datetime.now() - timedelta(days=30),
        'tags__contains': 'anxiety'  # Contains 'anxiety' tag
    },
    order_by=['-created_at', 'mood_rating'],
    limit=10,
    offset=0,
    include_count=True
)

result = repo.list_all(options)
```

**Supported Filter Operations:**
- `__eq`: Equals (default)
- `__ne`: Not equals
- `__gt`, `__gte`: Greater than, greater than or equal
- `__lt`, `__lte`: Less than, less than or equal
- `__in`: In list
- `__contains`: Contains (for arrays/strings)
- `__startswith`, `__endswith`: String operations
- `__isnull`: Is null/not null

## Error Handling

### Custom Exceptions

```python
from backend.happypath.repository import (
    ValidationError,
    NotFoundError,
    DuplicateError,
    RepositoryError
)

try:
    user = repo.create(invalid_user)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
except DuplicateError as e:
    logger.error(f"Duplicate entry: {e}")
except RepositoryError as e:
    logger.error(f"Repository error: {e}")
```

## Testing

### Repository Testing Patterns

```python
import pytest
from unittest.mock import Mock
from backend.happypath.repository import UserRepository

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def user_repo(mock_db):
    return UserRepository(mock_db)

def test_create_user(user_repo, mock_db):
    # Test user creation
    user = User(username="test", email="test@example.com")
    mock_db.execute_query.return_value = [{"id": 1, "username": "test"}]
    
    result = user_repo.create(user)
    
    assert result.username == "test"
    mock_db.execute_query.assert_called_once()
```

## Performance Considerations

### Database Optimization

1. **Indexing Strategy**: All repositories include proper indexing on frequently queried fields
2. **Query Optimization**: Use `QueryOptions` to limit results and include only necessary fields
3. **Connection Pooling**: Database manager handles connection pooling automatically
4. **Async Operations**: Use `AsyncBaseRepository` for high-concurrency scenarios

### Caching

```python
# Repository-level caching
@cache_result(ttl=300)  # 5-minute cache
def get_user_profile(self, user_id: str):
    return self.find_one_by(user_id=user_id)
```

## Security Considerations

### Data Protection

1. **Encryption**: Sensitive fields automatically encrypted at rest
2. **Access Control**: Role-based repository access patterns
3. **Audit Logging**: All data access automatically logged
4. **HIPAA Compliance**: Built-in compliance features for healthcare data

### Input Validation

```python
def _validate_entity(self, entity: User, is_update: bool = False):
    if not entity.email:
        raise ValidationError("Email is required")
    
    if not self._is_valid_email(entity.email):
        raise ValidationError("Invalid email format")
    
    # Additional validation logic
```

## Deployment

### Environment Configuration

```python
# Production configuration
repositories = {
    'clinical': {
        'therapeutic_relationship': create_therapeutic_relationship_repository(db, logger),
        'treatment_plan': create_treatment_plan_repository(db, logger),
        'therapy_session': create_therapy_session_repository(db, logger),
    },
    'patient_engagement': {
        'mood': create_mood_entry_repository(db, logger),
        'journal': create_journal_entry_repository(db, logger),
    },
    # ... additional repositories
}
```

### Monitoring and Logging

- All repositories include comprehensive logging
- Performance metrics automatically collected
- Error tracking and alerting integration
- Health check endpoints for monitoring

## Migration and Versioning

### Schema Evolution

```python
# Version-aware entity migration
def migrate_entity_v1_to_v2(self, entity_dict: dict) -> dict:
    if entity_dict.get('_version', 1) < 2:
        # Perform migration logic
        entity_dict['new_field'] = self._calculate_new_field(entity_dict)
        entity_dict['_version'] = 2
    return entity_dict
```

## Best Practices

### Repository Usage

1. **Single Responsibility**: Each repository handles one entity type
2. **Consistent Interface**: Use factory functions for repository creation
3. **Error Handling**: Always handle repository exceptions appropriately
4. **Logging**: Include sufficient logging for debugging and monitoring
5. **Testing**: Write comprehensive unit tests for repository operations

### Clinical Data Management

1. **Privacy by Design**: Default to most restrictive privacy settings
2. **Consent Tracking**: Document and track all consent decisions
3. **Data Retention**: Implement appropriate data retention policies
4. **Clinical Documentation**: Maintain comprehensive audit trails

### Performance Optimization

1. **Lazy Loading**: Load related entities only when needed
2. **Batch Operations**: Use batch operations for bulk data changes
3. **Query Optimization**: Use indexes and limit result sets appropriately
4. **Caching Strategy**: Implement appropriate caching for frequently accessed data

## Support and Maintenance

### Documentation Updates

- Keep repository documentation current with code changes
- Document all breaking changes in migration guides
- Maintain examples and sample code

### Community and Support

- Repository pattern examples in `/examples` directory
- Test cases serve as additional documentation
- Regular updates and security patches

This comprehensive repository system provides the foundation for a professional mental health wellness platform with enterprise-grade data management, clinical workflow support, and regulatory compliance features.
