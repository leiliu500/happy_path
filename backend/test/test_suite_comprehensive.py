# Mental Health Platform Repository Test Suite

## Overview

This comprehensive test suite covers all repository modules in the mental health wellness platform. The tests ensure data integrity, clinical workflow compliance, and robust error handling across all healthcare scenarios.

## Test Structure

```
backend/test/
├── conftest.py                 # Test configuration and fixtures
├── test_base_repository.py     # Base repository functionality
├── clinical/
│   ├── test_therapeutic_relationship_repository.py
│   ├── test_treatment_plan_repository.py
│   └── test_therapy_session_repository.py
├── patient_engagement/
│   ├── test_mood_tracking_repository.py
│   └── test_journaling_repository.py
├── crisis_management/
│   ├── test_crisis_detection_repository.py
│   └── test_safety_plan_repository.py
├── operational/
│   ├── test_appointment_repository.py
│   └── test_medication_repository.py
├── communication/
│   └── test_conversational_repository.py
├── administration/
│   ├── test_user_account_repository.py
│   └── test_audit_log_repository.py
├── care_coordination/
│   ├── test_provider_repository.py
│   ├── test_referral_repository.py
│   └── test_care_team_repository.py
└── integration/
    ├── test_clinical_workflows.py
    ├── test_crisis_workflows.py
    └── test_care_coordination_workflows.py
```

## Test Configuration (conftest.py)

```python
import pytest
from datetime import date, datetime, timedelta
from unittest.mock import Mock, AsyncMock
from dataclasses import asdict

from backend.happypath.repository import *

@pytest.fixture
def mock_db_manager():
    """Mock database manager for testing."""
    mock_db = Mock()
    mock_db.execute_query = Mock()
    mock_db.execute_async_query = AsyncMock()
    mock_db.begin_transaction = Mock()
    mock_db.commit_transaction = Mock()
    mock_db.rollback_transaction = Mock()
    return mock_db

@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    return Mock()

@pytest.fixture
def sample_patient_id():
    """Standard patient ID for testing."""
    return "patient_test_123"

@pytest.fixture
def sample_therapist_id():
    """Standard therapist ID for testing."""
    return "therapist_test_456"

@pytest.fixture
def sample_provider_id():
    """Standard provider ID for testing."""
    return "provider_test_789"

# Clinical Test Fixtures

@pytest.fixture
def sample_therapeutic_relationship(sample_patient_id, sample_therapist_id):
    """Sample therapeutic relationship for testing."""
    return TherapeuticRelationship(
        patient_id=sample_patient_id,
        therapist_id=sample_therapist_id,
        therapy_modality=TherapyModality.CBT,
        relationship_status="active",
        start_date=date.today(),
        session_frequency=SessionFrequency.WEEKLY,
        treatment_focus=["Depression", "Anxiety"],
        therapeutic_goals=["Reduce symptoms", "Improve coping"],
        treatment_phase=TreatmentPhase.ACTIVE,
        supervision_required=False
    )

@pytest.fixture
def sample_treatment_plan(sample_patient_id, sample_therapist_id):
    """Sample treatment plan for testing."""
    return TreatmentPlan(
        patient_id=sample_patient_id,
        therapist_id=sample_therapist_id,
        plan_name="CBT for Depression",
        primary_diagnosis="Major Depressive Disorder",
        secondary_diagnoses=["Generalized Anxiety Disorder"],
        treatment_goals=["Reduce depressive symptoms", "Improve daily functioning"],
        interventions=["Cognitive restructuring", "Behavioral activation"],
        estimated_duration_weeks=16,
        session_frequency=SessionFrequency.WEEKLY,
        phase=TreatmentPhase.ACTIVE,
        created_date=date.today(),
        last_updated=datetime.now(),
        review_date=date.today() + timedelta(weeks=4)
    )

@pytest.fixture
def sample_therapy_session(sample_patient_id, sample_therapist_id):
    """Sample therapy session for testing."""
    return TherapySession(
        relationship_id="rel_123",
        patient_id=sample_patient_id,
        therapist_id=sample_therapist_id,
        session_date=date.today(),
        session_type="individual",
        duration_minutes=50,
        session_notes="Patient showed good progress with cognitive techniques",
        interventions_used=["Cognitive restructuring", "Homework review"],
        patient_mood_start=4,
        patient_mood_end=7,
        risk_assessment="low",
        homework_assigned=["Daily thought record", "Mood tracking"],
        next_session_date=date.today() + timedelta(weeks=1),
        session_goals=["Review homework", "Practice new techniques"],
        treatment_plan_id="plan_123"
    )

# Patient Engagement Test Fixtures

@pytest.fixture
def sample_mood_entry(sample_patient_id):
    """Sample mood entry for testing."""
    return MoodEntry(
        user_id=sample_patient_id,
        mood_scale=MoodScale.ONE_TO_TEN,
        mood_rating=7,
        mood_type=MoodType.GENERAL,
        contributing_factors=["Good sleep", "Exercise"],
        triggers=["Work stress"],
        notes="Feeling more balanced today",
        activities=["Walked", "Meditated"],
        sleep_hours=8,
        energy_level=EnergyLevel.MODERATE,
        anxiety_level=3,
        depression_level=2,
        location="home",
        social_context="alone"
    )

@pytest.fixture
def sample_journal_entry(sample_patient_id):
    """Sample journal entry for testing."""
    return JournalEntry(
        user_id=sample_patient_id,
        title="Thought Challenging Exercise",
        content="Today I practiced questioning my negative thoughts about work...",
        journal_type=JournalType.THERAPEUTIC,
        cbt_technique=CBTTechnique.THOUGHT_RECORD,
        mood_before=4,
        mood_after=7,
        insights=["I can control my response to thoughts"],
        tags=["anxiety", "work", "cognitive-techniques"],
        prompt_used="What thoughts are causing you stress?",
        word_count=150,
        is_private=True,
        shared_with_therapist=True
    )

# Crisis Management Test Fixtures

@pytest.fixture
def sample_crisis_detection(sample_patient_id):
    """Sample crisis detection for testing."""
    return CrisisDetection(
        patient_id=sample_patient_id,
        detection_source="journal_entry",
        source_content_id="journal_456",
        crisis_type="suicidal_ideation",
        severity_level="high",
        detected_keywords=["hopeless", "ending it all", "no point"],
        confidence_score=0.95,
        risk_factors=["social isolation", "recent loss"],
        protective_factors=["family support"],
        requires_immediate_attention=True,
        detection_method="keyword_ml_hybrid",
        ai_model_version="v2.1"
    )

@pytest.fixture
def sample_safety_plan(sample_patient_id, sample_therapist_id):
    """Sample safety plan for testing."""
    return SafetyPlan(
        patient_id=sample_patient_id,
        created_by_provider_id=sample_therapist_id,
        warning_signs=["Feeling hopeless", "Social isolation", "Increased substance use"],
        coping_strategies=["Deep breathing exercises", "Call a friend", "Go for a walk"],
        social_contacts=[
            {"name": "Sister Mary", "phone": "(555) 123-4567", "relationship": "sister"},
            {"name": "Best Friend John", "phone": "(555) 987-6543", "relationship": "friend"}
        ],
        professional_contacts=[
            {"name": "Dr. Smith", "phone": "(555) 111-2222", "role": "therapist"},
            {"name": "Crisis Hotline", "phone": "988", "role": "crisis_support"}
        ],
        environmental_safety=["Remove firearms", "Secure medications", "Remove sharp objects"],
        reasons_to_live=["My children", "Future goals", "Unfinished projects"],
        plan_version=1,
        last_reviewed=date.today()
    )

# Utility Functions

def create_mock_query_result(data_list, total_count=None):
    """Create a mock QueryResult for testing."""
    return QueryResult(
        data=data_list,
        total_count=total_count or len(data_list),
        page_info={
            'has_next_page': False,
            'has_previous_page': False,
            'start_cursor': None,
            'end_cursor': None
        }
    )

def mock_db_response(mock_db, return_data):
    """Configure mock database to return specific data."""
    if isinstance(return_data, list):
        mock_db.execute_query.return_value = return_data
    else:
        mock_db.execute_query.return_value = [asdict(return_data)]
    return mock_db
```

## Base Repository Tests

```python
# test_base_repository.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, date

from backend.happypath.repository import (
    BaseRepository, QueryOptions, QueryResult,
    ValidationError, NotFoundError, DuplicateError
)

class TestEntity:
    """Test entity for base repository testing."""
    def __init__(self, id=None, name=None, created_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at or datetime.now()

class TestBaseRepository:
    """Test suite for BaseRepository functionality."""
    
    @pytest.fixture
    def test_repository(self, mock_db_manager, mock_logger):
        """Create test repository instance."""
        return BaseRepository(
            entity_class=TestEntity,
            db_manager=mock_db_manager,
            logger=mock_logger,
            table_name="test_entities"
        )
    
    def test_create_entity_success(self, test_repository, mock_db_manager):
        """Test successful entity creation."""
        # Arrange
        entity = TestEntity(name="Test Entity")
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Test Entity"}]
        
        # Act
        result = test_repository.create(entity)
        
        # Assert
        assert result.id == 1
        assert result.name == "Test Entity"
        mock_db_manager.execute_query.assert_called_once()
    
    def test_create_entity_validation_error(self, test_repository):
        """Test entity creation with validation error."""
        # Arrange
        entity = TestEntity(name="")  # Invalid empty name
        
        # Act & Assert
        with pytest.raises(ValidationError):
            test_repository.create(entity)
    
    def test_get_by_id_found(self, test_repository, mock_db_manager):
        """Test successful entity retrieval by ID."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Test Entity"}]
        
        # Act
        result = test_repository.get_by_id(1)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.name == "Test Entity"
    
    def test_get_by_id_not_found(self, test_repository, mock_db_manager):
        """Test entity retrieval when not found."""
        # Arrange
        mock_db_manager.execute_query.return_value = []
        
        # Act
        result = test_repository.get_by_id(999)
        
        # Assert
        assert result is None
    
    def test_update_entity_success(self, test_repository, mock_db_manager):
        """Test successful entity update."""
        # Arrange
        entity = TestEntity(id=1, name="Updated Entity")
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Updated Entity"}]
        
        # Act
        result = test_repository.update(entity)
        
        # Assert
        assert result.name == "Updated Entity"
        mock_db_manager.execute_query.assert_called_once()
    
    def test_delete_entity_success(self, test_repository, mock_db_manager):
        """Test successful entity deletion."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"affected_rows": 1}]
        
        # Act
        result = test_repository.delete(1)
        
        # Assert
        assert result is True
        mock_db_manager.execute_query.assert_called_once()
    
    def test_delete_entity_not_found(self, test_repository, mock_db_manager):
        """Test entity deletion when not found."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"affected_rows": 0}]
        
        # Act
        result = test_repository.delete(999)
        
        # Assert
        assert result is False
    
    def test_list_all_with_filters(self, test_repository, mock_db_manager):
        """Test listing entities with filters."""
        # Arrange
        options = QueryOptions(
            filters={"name": "Test"},
            order_by=["name"],
            limit=10
        )
        mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Test Entity 1"},
            {"id": 2, "name": "Test Entity 2"}
        ]
        
        # Act
        result = test_repository.list_all(options)
        
        # Assert
        assert len(result.data) == 2
        assert result.data[0].name == "Test Entity 1"
        mock_db_manager.execute_query.assert_called_once()
    
    def test_find_one_by_success(self, test_repository, mock_db_manager):
        """Test finding single entity by criteria."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Test Entity"}]
        
        # Act
        result = test_repository.find_one_by(name="Test Entity")
        
        # Assert
        assert result is not None
        assert result.name == "Test Entity"
    
    def test_find_one_by_multiple_results_error(self, test_repository, mock_db_manager):
        """Test finding single entity when multiple results exist."""
        # Arrange
        mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Test Entity"},
            {"id": 2, "name": "Test Entity"}
        ]
        
        # Act & Assert
        with pytest.raises(ValueError, match="Multiple entities found"):
            test_repository.find_one_by(name="Test Entity")
    
    def test_exists_true(self, test_repository, mock_db_manager):
        """Test entity existence check returns True."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"count": 1}]
        
        # Act
        result = test_repository.exists(id=1)
        
        # Assert
        assert result is True
    
    def test_exists_false(self, test_repository, mock_db_manager):
        """Test entity existence check returns False."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"count": 0}]
        
        # Act
        result = test_repository.exists(id=999)
        
        # Assert
        assert result is False
    
    def test_count_entities(self, test_repository, mock_db_manager):
        """Test counting entities with filters."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"count": 5}]
        
        # Act
        result = test_repository.count(name="Test")
        
        # Assert
        assert result == 5
    
    def test_transaction_success(self, test_repository, mock_db_manager):
        """Test successful transaction execution."""
        # Arrange
        entity = TestEntity(name="Transaction Test")
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Transaction Test"}]
        
        # Act
        with test_repository.transaction():
            result = test_repository.create(entity)
        
        # Assert
        assert result.name == "Transaction Test"
        mock_db_manager.begin_transaction.assert_called_once()
        mock_db_manager.commit_transaction.assert_called_once()
    
    def test_transaction_rollback_on_error(self, test_repository, mock_db_manager):
        """Test transaction rollback on error."""
        # Arrange
        mock_db_manager.execute_query.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception):
            with test_repository.transaction():
                test_repository.create(TestEntity(name="Test"))
        
        mock_db_manager.rollback_transaction.assert_called_once()
```

## Clinical Repository Tests

```python
# test_therapeutic_relationship_repository.py
import pytest
from datetime import date, timedelta
from unittest.mock import Mock

from backend.happypath.repository import (
    TherapeuticRelationshipRepository,
    TherapeuticRelationship,
    TherapyModality,
    SessionFrequency,
    TreatmentPhase
)

class TestTherapeuticRelationshipRepository:
    """Test suite for TherapeuticRelationshipRepository."""
    
    @pytest.fixture
    def relationship_repo(self, mock_db_manager, mock_logger):
        """Create therapeutic relationship repository instance."""
        return TherapeuticRelationshipRepository(mock_db_manager, mock_logger)
    
    def test_create_relationship_success(self, relationship_repo, mock_db_manager, sample_therapeutic_relationship):
        """Test successful therapeutic relationship creation."""
        # Arrange
        mock_db_response(mock_db_manager, sample_therapeutic_relationship)
        
        # Act
        result = relationship_repo.create(sample_therapeutic_relationship)
        
        # Assert
        assert result.therapy_modality == TherapyModality.CBT
        assert result.relationship_status == "active"
        assert result.session_frequency == SessionFrequency.WEEKLY
        mock_db_manager.execute_query.assert_called_once()
    
    def test_get_active_relationships_for_patient(self, relationship_repo, mock_db_manager, sample_patient_id):
        """Test retrieving active relationships for a patient."""
        # Arrange
        relationships_data = [
            {
                "relationship_id": "rel_1",
                "patient_id": sample_patient_id,
                "therapist_id": "therapist_1",
                "therapy_modality": "CBT",
                "relationship_status": "active"
            }
        ]
        mock_db_manager.execute_query.return_value = relationships_data
        
        # Act
        result = relationship_repo.get_active_relationships_for_patient(sample_patient_id)
        
        # Assert
        assert len(result) == 1
        assert result[0].patient_id == sample_patient_id
        assert result[0].relationship_status == "active"
    
    def test_update_relationship_phase(self, relationship_repo, mock_db_manager):
        """Test updating relationship treatment phase."""
        # Arrange
        relationship_id = "rel_123"
        new_phase = TreatmentPhase.MAINTENANCE
        mock_db_manager.execute_query.return_value = [{"updated": True}]
        
        # Act
        result = relationship_repo.update_treatment_phase(relationship_id, new_phase)
        
        # Assert
        assert result is True
        mock_db_manager.execute_query.assert_called_once()
    
    def test_get_relationships_by_therapist(self, relationship_repo, mock_db_manager, sample_therapist_id):
        """Test retrieving relationships by therapist."""
        # Arrange
        relationships_data = [
            {
                "relationship_id": "rel_1",
                "patient_id": "patient_1",
                "therapist_id": sample_therapist_id,
                "therapy_modality": "CBT"
            },
            {
                "relationship_id": "rel_2", 
                "patient_id": "patient_2",
                "therapist_id": sample_therapist_id,
                "therapy_modality": "DBT"
            }
        ]
        mock_db_manager.execute_query.return_value = relationships_data
        
        # Act
        result = relationship_repo.get_relationships_by_therapist(sample_therapist_id)
        
        # Assert
        assert len(result) == 2
        assert all(rel.therapist_id == sample_therapist_id for rel in result)
    
    def test_end_relationship(self, relationship_repo, mock_db_manager):
        """Test ending a therapeutic relationship."""
        # Arrange
        relationship_id = "rel_123"
        end_reason = "Treatment completed successfully"
        mock_db_manager.execute_query.return_value = [{"updated": True}]
        
        # Act
        result = relationship_repo.end_relationship(relationship_id, end_reason)
        
        # Assert
        assert result is True
        mock_db_manager.execute_query.assert_called_once()
        
        # Verify the call included end_date and reason
        call_args = mock_db_manager.execute_query.call_args
        assert "end_date" in str(call_args)
        assert end_reason in str(call_args)
```

## Patient Engagement Tests

```python
# test_mood_tracking_repository.py
import pytest
from datetime import date, datetime, timedelta
from unittest.mock import Mock

from backend.happypath.repository import (
    MoodEntryRepository,
    MoodEntry,
    MoodScale,
    MoodType,
    EnergyLevel
)

class TestMoodEntryRepository:
    """Test suite for MoodEntryRepository."""
    
    @pytest.fixture
    def mood_repo(self, mock_db_manager, mock_logger):
        """Create mood entry repository instance."""
        return MoodEntryRepository(mock_db_manager, mock_logger)
    
    def test_create_mood_entry_success(self, mood_repo, mock_db_manager, sample_mood_entry):
        """Test successful mood entry creation."""
        # Arrange
        mock_db_response(mock_db_manager, sample_mood_entry)
        
        # Act
        result = mood_repo.create(sample_mood_entry)
        
        # Assert
        assert result.mood_rating == 7
        assert result.mood_scale == MoodScale.ONE_TO_TEN
        assert len(result.contributing_factors) == 2
        mock_db_manager.execute_query.assert_called_once()
    
    def test_get_mood_trends(self, mood_repo, mock_db_manager, sample_patient_id):
        """Test retrieving mood trends for analysis."""
        # Arrange
        trend_data = [
            {"date": "2024-01-01", "avg_mood": 6.5, "entry_count": 3},
            {"date": "2024-01-02", "avg_mood": 7.2, "entry_count": 2},
            {"date": "2024-01-03", "avg_mood": 5.8, "entry_count": 4}
        ]
        mock_db_manager.execute_query.return_value = trend_data
        
        # Act
        trends = mood_repo.get_mood_trends(
            user_id=sample_patient_id,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 3)
        )
        
        # Assert
        assert len(trends) == 3
        assert trends[0]["avg_mood"] == 6.5
        assert trends[1]["avg_mood"] == 7.2
    
    def test_analyze_mood_patterns(self, mood_repo, mock_db_manager, sample_patient_id):
        """Test mood pattern analysis."""
        # Arrange
        analysis_data = {
            "average_mood": 6.8,
            "mood_variance": 1.2,
            "trend": "improving",
            "common_factors": ["exercise", "good sleep"],
            "trigger_patterns": ["work stress", "social isolation"]
        }
        mock_db_manager.execute_query.return_value = [analysis_data]
        
        # Act
        analysis = mood_repo.analyze_mood_patterns(
            user_id=sample_patient_id,
            days_back=30
        )
        
        # Assert
        assert analysis["average_mood"] == 6.8
        assert analysis["trend"] == "improving"
        assert "exercise" in analysis["common_factors"]
    
    def test_get_mood_correlations(self, mood_repo, mock_db_manager, sample_patient_id):
        """Test mood correlation analysis with other metrics."""
        # Arrange
        correlation_data = [
            {"metric": "sleep_hours", "correlation": 0.73},
            {"metric": "exercise_minutes", "correlation": 0.65},
            {"metric": "social_interaction", "correlation": 0.58}
        ]
        mock_db_manager.execute_query.return_value = correlation_data
        
        # Act
        correlations = mood_repo.get_mood_correlations(sample_patient_id)
        
        # Assert
        assert len(correlations) == 3
        assert correlations[0]["metric"] == "sleep_hours"
        assert correlations[0]["correlation"] == 0.73
    
    def test_detect_mood_anomalies(self, mood_repo, mock_db_manager, sample_patient_id):
        """Test mood anomaly detection."""
        # Arrange
        anomaly_data = [
            {
                "entry_id": "mood_123",
                "date": "2024-01-15",
                "mood_rating": 2,
                "anomaly_type": "sudden_drop",
                "severity": "high",
                "baseline_mood": 7.5
            }
        ]
        mock_db_manager.execute_query.return_value = anomaly_data
        
        # Act
        anomalies = mood_repo.detect_mood_anomalies(
            user_id=sample_patient_id,
            days_back=7
        )
        
        # Assert
        assert len(anomalies) == 1
        assert anomalies[0]["anomaly_type"] == "sudden_drop"
        assert anomalies[0]["severity"] == "high"
    
    def test_get_mood_goals_progress(self, mood_repo, mock_db_manager, sample_patient_id):
        """Test mood goals progress tracking."""
        # Arrange
        progress_data = {
            "goal_id": "goal_123",
            "target_mood": 8,
            "current_average": 7.2,
            "progress_percentage": 72,
            "days_to_goal": 14,
            "on_track": True
        }
        mock_db_manager.execute_query.return_value = [progress_data]
        
        # Act
        progress = mood_repo.get_mood_goals_progress(sample_patient_id)
        
        # Assert
        assert progress["current_average"] == 7.2
        assert progress["progress_percentage"] == 72
        assert progress["on_track"] is True
```

## Crisis Management Tests

```python
# test_crisis_detection_repository.py
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from backend.happypath.repository import (
    CrisisDetectionRepository,
    CrisisDetection,
    CrisisEscalation,
    CrisisResponse
)

class TestCrisisDetectionRepository:
    """Test suite for CrisisDetectionRepository."""
    
    @pytest.fixture
    def crisis_repo(self, mock_db_manager, mock_logger):
        """Create crisis detection repository instance."""
        return CrisisDetectionRepository(mock_db_manager, mock_logger)
    
    def test_create_crisis_detection_high_severity(self, crisis_repo, mock_db_manager, sample_crisis_detection):
        """Test creating high-severity crisis detection triggers immediate response."""
        # Arrange
        mock_db_response(mock_db_manager, sample_crisis_detection)
        
        # Act
        result = crisis_repo.create(sample_crisis_detection)
        
        # Assert
        assert result.severity_level == "high"
        assert result.requires_immediate_attention is True
        assert result.confidence_score == 0.95
        mock_db_manager.execute_query.assert_called()
    
    def test_escalate_crisis_automatic(self, crisis_repo, mock_db_manager):
        """Test automatic crisis escalation for high-risk cases."""
        # Arrange
        detection_id = "crisis_123"
        escalation_data = {
            "escalation_id": "esc_456",
            "detection_id": detection_id,
            "escalated_to": "crisis_team",
            "escalation_reason": "High-risk suicidal ideation",
            "escalation_time": datetime.now(),
            "response_required_by": datetime.now() + timedelta(minutes=15)
        }
        mock_db_manager.execute_query.return_value = [escalation_data]
        
        # Act
        result = crisis_repo.escalate_crisis(
            detection_id=detection_id,
            escalated_to="crisis_team",
            escalation_reason="High-risk suicidal ideation"
        )
        
        # Assert
        assert result.escalated_to == "crisis_team"
        assert result.detection_id == detection_id
        mock_db_manager.execute_query.assert_called_once()
    
    def test_get_active_crises(self, crisis_repo, mock_db_manager):
        """Test retrieving active crisis cases."""
        # Arrange
        active_crises = [
            {
                "detection_id": "crisis_1",
                "patient_id": "patient_123",
                "severity_level": "high",
                "status": "escalated",
                "created_at": datetime.now() - timedelta(hours=1)
            },
            {
                "detection_id": "crisis_2",
                "patient_id": "patient_456",
                "severity_level": "medium",
                "status": "monitoring",
                "created_at": datetime.now() - timedelta(hours=2)
            }
        ]
        mock_db_manager.execute_query.return_value = active_crises
        
        # Act
        result = crisis_repo.get_active_crises()
        
        # Assert
        assert len(result) == 2
        assert result[0]["severity_level"] == "high"
        assert result[1]["status"] == "monitoring"
    
    @patch('backend.happypath.repository.datetime')
    def test_check_response_times(self, mock_datetime, crisis_repo, mock_db_manager):
        """Test crisis response time monitoring."""
        # Arrange
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        overdue_responses = [
            {
                "escalation_id": "esc_123",
                "detection_id": "crisis_456",
                "escalated_to": "crisis_team",
                "response_required_by": datetime(2024, 1, 1, 11, 45, 0),
                "minutes_overdue": 15
            }
        ]
        mock_db_manager.execute_query.return_value = overdue_responses
        
        # Act
        overdue = crisis_repo.check_response_times()
        
        # Assert
        assert len(overdue) == 1
        assert overdue[0]["minutes_overdue"] == 15
    
    def test_update_crisis_status(self, crisis_repo, mock_db_manager):
        """Test updating crisis status and resolution."""
        # Arrange
        detection_id = "crisis_123"
        mock_db_manager.execute_query.return_value = [{"updated": True}]
        
        # Act
        result = crisis_repo.update_crisis_status(
            detection_id=detection_id,
            status="resolved",
            resolution_notes="Patient contacted, safety plan activated"
        )
        
        # Assert
        assert result is True
        mock_db_manager.execute_query.assert_called_once()
    
    def test_get_crisis_analytics(self, crisis_repo, mock_db_manager):
        """Test crisis detection analytics and reporting."""
        # Arrange
        analytics_data = {
            "total_detections": 45,
            "high_severity_count": 12,
            "average_response_time_minutes": 8.5,
            "false_positive_rate": 0.15,
            "resolution_rate": 0.92,
            "common_triggers": ["isolation", "hopelessness", "loss"]
        }
        mock_db_manager.execute_query.return_value = [analytics_data]
        
        # Act
        analytics = crisis_repo.get_crisis_analytics(
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        
        # Assert
        assert analytics["total_detections"] == 45
        assert analytics["average_response_time_minutes"] == 8.5
        assert analytics["false_positive_rate"] == 0.15
```

## Integration Tests

```python
# test_clinical_workflows.py
import pytest
from datetime import date, datetime, timedelta
from unittest.mock import Mock

from backend.happypath.repository import *

class TestClinicalWorkflows:
    """Integration tests for clinical workflows."""
    
    @pytest.fixture
    def repositories(self, mock_db_manager, mock_logger):
        """Create all clinical repositories."""
        return {
            'therapeutic': create_therapeutic_relationship_repository(mock_db_manager, mock_logger),
            'treatment': create_treatment_plan_repository(mock_db_manager, mock_logger),
            'session': create_therapy_session_repository(mock_db_manager, mock_logger),
            'mood': create_mood_entry_repository(mock_db_manager, mock_logger),
            'crisis': create_crisis_detection_repository(mock_db_manager, mock_logger)
        }
    
    def test_complete_patient_intake_workflow(self, repositories, mock_db_manager):
        """Test complete patient intake and first session workflow."""
        # Arrange
        patient_id = "patient_123"
        therapist_id = "therapist_456"
        
        # Mock responses for each repository call
        mock_db_manager.execute_query.side_effect = [
            # Therapeutic relationship creation
            [{"relationship_id": "rel_789", "patient_id": patient_id, "therapist_id": therapist_id}],
            # Treatment plan creation
            [{"plan_id": "plan_101", "patient_id": patient_id, "plan_name": "Initial Assessment"}],
            # First session documentation
            [{"session_id": "session_202", "relationship_id": "rel_789", "session_type": "intake"}]
        ]
        
        # Act - Complete intake workflow
        
        # 1. Establish therapeutic relationship
        relationship = TherapeuticRelationship(
            patient_id=patient_id,
            therapist_id=therapist_id,
            therapy_modality=TherapyModality.CBT,
            relationship_status="active",
            start_date=date.today()
        )
        created_relationship = repositories['therapeutic'].create(relationship)
        
        # 2. Create initial treatment plan
        treatment_plan = TreatmentPlan(
            patient_id=patient_id,
            therapist_id=therapist_id,
            plan_name="Initial Assessment and Stabilization",
            primary_diagnosis="To be determined",
            treatment_goals=["Complete assessment", "Establish rapport"],
            phase=TreatmentPhase.ASSESSMENT
        )
        created_plan = repositories['treatment'].create(treatment_plan)
        
        # 3. Document intake session
        intake_session = TherapySession(
            relationship_id=created_relationship.relationship_id,
            patient_id=patient_id,
            therapist_id=therapist_id,
            session_date=date.today(),
            session_type="intake",
            duration_minutes=60,
            session_notes="Initial assessment completed. Patient presenting with anxiety and mood concerns.",
            risk_assessment="low"
        )
        documented_session = repositories['session'].create(intake_session)
        
        # Assert
        assert created_relationship.patient_id == patient_id
        assert created_plan.phase == TreatmentPhase.ASSESSMENT
        assert documented_session.session_type == "intake"
        assert mock_db_manager.execute_query.call_count == 3
    
    def test_crisis_detection_and_response_workflow(self, repositories, mock_db_manager):
        """Test crisis detection triggering immediate response workflow."""
        # Arrange
        patient_id = "patient_123"
        
        mock_db_manager.execute_query.side_effect = [
            # Crisis detection creation
            [{"detection_id": "crisis_456", "patient_id": patient_id, "severity_level": "high"}],
            # Crisis escalation
            [{"escalation_id": "esc_789", "escalated_to": "crisis_team"}],
            # Safety plan retrieval
            [{"plan_id": "safety_101", "patient_id": patient_id, "active": True}]
        ]
        
        # Act - Crisis workflow
        
        # 1. Crisis detected (usually automatic)
        crisis = CrisisDetection(
            patient_id=patient_id,
            detection_source="journal_entry",
            crisis_type="suicidal_ideation",
            severity_level="high",
            detected_keywords=["hopeless", "end it all"],
            confidence_score=0.95,
            requires_immediate_attention=True
        )
        detected_crisis = repositories['crisis'].create(crisis)
        
        # 2. Automatic escalation for high severity
        escalation = repositories['crisis'].escalate_crisis(
            detection_id=detected_crisis.detection_id,
            escalated_to="crisis_team",
            escalation_reason="High-confidence suicidal ideation detected"
        )
        
        # 3. Retrieve active safety plan
        safety_plan = repositories['crisis'].get_active_safety_plan(patient_id)
        
        # Assert
        assert detected_crisis.severity_level == "high"
        assert escalation.escalated_to == "crisis_team"
        assert safety_plan is not None
        assert mock_db_manager.execute_query.call_count == 3
    
    def test_treatment_progress_tracking_workflow(self, repositories, mock_db_manager):
        """Test treatment progress tracking across multiple sessions."""
        # Arrange
        patient_id = "patient_123"
        plan_id = "plan_456"
        
        mock_db_manager.execute_query.side_effect = [
            # Mood entries
            [{"entry_id": "mood_1", "mood_rating": 4, "date": "2024-01-01"}],
            [{"entry_id": "mood_2", "mood_rating": 6, "date": "2024-01-08"}],
            [{"entry_id": "mood_3", "mood_rating": 7, "date": "2024-01-15"}],
            # Treatment plan update
            [{"plan_id": plan_id, "goals_progress": {"mood_improvement": 75}}],
            # Progress analysis
            [{"average_mood": 5.7, "trend": "improving", "variance": 1.5}]
        ]
        
        # Act - Track progress over time
        
        # 1. Patient logs mood over several weeks
        mood_entries = []
        for i, rating in enumerate([4, 6, 7], 1):
            mood = MoodEntry(
                user_id=patient_id,
                mood_rating=rating,
                mood_scale=MoodScale.ONE_TO_TEN,
                entry_date=date.today() - timedelta(weeks=3-i)
            )
            mood_entries.append(repositories['mood'].create(mood))
        
        # 2. Update treatment plan progress
        progress_update = repositories['treatment'].update_treatment_progress(
            plan_id=plan_id,
            goals_progress={"mood_improvement": 75},
            phase_notes="Significant improvement in mood stability"
        )
        
        # 3. Analyze overall progress
        mood_analysis = repositories['mood'].analyze_mood_patterns(
            user_id=patient_id,
            days_back=30
        )
        
        # Assert
        assert len(mood_entries) == 3
        assert mood_entries[-1].mood_rating == 7  # Latest mood improved
        assert progress_update["goals_progress"]["mood_improvement"] == 75
        assert mood_analysis["trend"] == "improving"
        assert mock_db_manager.execute_query.call_count == 5
```

## Test Execution Instructions

### Running All Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock pytest-asyncio

# Run all tests with coverage
pytest backend/test/ --cov=backend/happypath/repository --cov-report=html

# Run specific test categories
pytest backend/test/clinical/ -v                    # Clinical tests only
pytest backend/test/patient_engagement/ -v         # Patient engagement tests
pytest backend/test/crisis_management/ -v          # Crisis management tests
pytest backend/test/integration/ -v                # Integration tests

# Run tests with specific markers
pytest -m "not slow" backend/test/                 # Skip slow tests
pytest -m "crisis" backend/test/                   # Run crisis-related tests only
```

### Test Coverage Requirements

- **Unit Tests**: Minimum 90% code coverage
- **Integration Tests**: Cover all major clinical workflows
- **Error Cases**: Test all custom exceptions and error conditions
- **Edge Cases**: Test boundary conditions and invalid inputs
- **Performance**: Include performance tests for query operations

### Continuous Integration

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: |
          pytest backend/test/ --cov=backend/happypath/repository --cov-fail-under=90
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

This comprehensive test suite ensures the mental health platform repository system maintains high quality, reliability, and clinical safety across all workflows and edge cases.
