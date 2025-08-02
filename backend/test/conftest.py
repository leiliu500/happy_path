"""
Test configuration and fixtures for the mental health platform repository test suite.
"""
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
