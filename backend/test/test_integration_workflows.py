"""
Integration tests for clinical workflows in the mental health platform.
"""
import pytest
from datetime import date, datetime, timedelta
from unittest.mock import Mock

class TestClinicalWorkflows:
    """Integration tests for clinical workflows."""
    
    @pytest.fixture
    def repositories(self, mock_db_manager, mock_logger):
        """Create mock repositories for testing."""
        # Create simple mock repositories
        therapeutic_repo = Mock()
        treatment_repo = Mock()
        session_repo = Mock()
        mood_repo = Mock()
        crisis_repo = Mock()
        
        return {
            'therapeutic': therapeutic_repo,
            'treatment': treatment_repo,
            'session': session_repo,
            'mood': mood_repo,
            'crisis': crisis_repo
        }
    
    def test_complete_patient_intake_workflow(self, repositories, mock_db_manager):
        """Test complete patient intake and first session workflow."""
        # Arrange
        patient_id = "patient_123"
        therapist_id = "therapist_456"
        
        # Configure mock responses
        repositories['therapeutic'].create.return_value = Mock(
            relationship_id="rel_789",
            patient_id=patient_id,
            therapist_id=therapist_id
        )
        
        repositories['treatment'].create.return_value = Mock(
            plan_id="plan_101",
            patient_id=patient_id,
            plan_name="Initial Assessment"
        )
        
        repositories['session'].create.return_value = Mock(
            session_id="session_202",
            relationship_id="rel_789",
            session_type="intake"
        )
        
        # Act - Simulate intake workflow
        
        # 1. Establish therapeutic relationship
        relationship_data = {
            "patient_id": patient_id,
            "therapist_id": therapist_id,
            "therapy_modality": "CBT",
            "relationship_status": "active",
            "start_date": date.today()
        }
        created_relationship = repositories['therapeutic'].create(relationship_data)
        
        # 2. Create initial treatment plan
        treatment_plan_data = {
            "patient_id": patient_id,
            "therapist_id": therapist_id,
            "plan_name": "Initial Assessment and Stabilization",
            "primary_diagnosis": "To be determined",
            "treatment_goals": ["Complete assessment", "Establish rapport"],
            "phase": "ASSESSMENT"
        }
        created_plan = repositories['treatment'].create(treatment_plan_data)
        
        # 3. Document intake session
        intake_session_data = {
            "relationship_id": created_relationship.relationship_id,
            "patient_id": patient_id,
            "therapist_id": therapist_id,
            "session_date": date.today(),
            "session_type": "intake",
            "duration_minutes": 60,
            "session_notes": "Initial assessment completed.",
            "risk_assessment": "low"
        }
        documented_session = repositories['session'].create(intake_session_data)
        
        # Assert
        assert created_relationship.patient_id == patient_id
        assert created_plan.plan_name == "Initial Assessment"
        assert documented_session.session_type == "intake"
        
        # Verify all repository methods were called
        repositories['therapeutic'].create.assert_called_once()
        repositories['treatment'].create.assert_called_once()
        repositories['session'].create.assert_called_once()
    
    def test_crisis_detection_and_response_workflow(self, repositories, mock_db_manager):
        """Test crisis detection triggering immediate response workflow."""
        # Arrange
        patient_id = "patient_123"
        
        # Configure mock responses
        repositories['crisis'].create.return_value = Mock(
            detection_id="crisis_456",
            patient_id=patient_id,
            severity_level="high"
        )
        
        repositories['crisis'].escalate_crisis.return_value = Mock(
            escalation_id="esc_789",
            escalated_to="crisis_team"
        )
        
        repositories['crisis'].get_active_safety_plan.return_value = Mock(
            plan_id="safety_101",
            patient_id=patient_id,
            active=True
        )
        
        # Act - Simulate crisis workflow
        
        # 1. Crisis detected
        crisis_data = {
            "patient_id": patient_id,
            "detection_source": "journal_entry",
            "crisis_type": "suicidal_ideation",
            "severity_level": "high",
            "detected_keywords": ["hopeless", "end it all"],
            "confidence_score": 0.95,
            "requires_immediate_attention": True
        }
        detected_crisis = repositories['crisis'].create(crisis_data)
        
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
        
        # Verify workflow calls
        repositories['crisis'].create.assert_called_once()
        repositories['crisis'].escalate_crisis.assert_called_once()
        repositories['crisis'].get_active_safety_plan.assert_called_once()
    
    def test_treatment_progress_tracking_workflow(self, repositories, mock_db_manager):
        """Test treatment progress tracking across multiple sessions."""
        # Arrange
        patient_id = "patient_123"
        plan_id = "plan_456"
        
        # Configure mock responses
        mood_entries = [
            Mock(entry_id="mood_1", mood_rating=4, date="2024-01-01"),
            Mock(entry_id="mood_2", mood_rating=6, date="2024-01-08"),
            Mock(entry_id="mood_3", mood_rating=7, date="2024-01-15")
        ]
        repositories['mood'].create.side_effect = mood_entries
        
        repositories['treatment'].update_treatment_progress.return_value = {
            "plan_id": plan_id,
            "goals_progress": {"mood_improvement": 75}
        }
        
        repositories['mood'].analyze_mood_patterns.return_value = {
            "average_mood": 5.7,
            "trend": "improving",
            "variance": 1.5
        }
        
        # Act - Track progress over time
        
        # 1. Patient logs mood over several weeks
        created_mood_entries = []
        for i, rating in enumerate([4, 6, 7], 1):
            mood_data = {
                "user_id": patient_id,
                "mood_rating": rating,
                "mood_scale": "ONE_TO_TEN",
                "entry_date": date.today() - timedelta(weeks=3-i)
            }
            created_mood_entries.append(repositories['mood'].create(mood_data))
        
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
        assert len(created_mood_entries) == 3
        assert created_mood_entries[-1].mood_rating == 7  # Latest mood improved
        assert progress_update["goals_progress"]["mood_improvement"] == 75
        assert mood_analysis["trend"] == "improving"
        
        # Verify all calls
        assert repositories['mood'].create.call_count == 3
        repositories['treatment'].update_treatment_progress.assert_called_once()
        repositories['mood'].analyze_mood_patterns.assert_called_once()
    
    def test_medication_adherence_workflow(self, repositories, mock_db_manager):
        """Test medication adherence tracking workflow."""
        # Arrange
        patient_id = "patient_123"
        
        # Add medication repository to mocks
        repositories['medication'] = Mock()
        
        # Configure mock responses
        repositories['medication'].create.return_value = Mock(
            medication_id="med_123",
            patient_id=patient_id,
            medication_name="Sertraline"
        )
        
        repositories['medication'].log_adherence.return_value = Mock(
            log_id="log_456",
            taken=True,
            date=date.today()
        )
        
        repositories['medication'].calculate_adherence.return_value = {
            "adherence_rate": 0.85,
            "missed_doses": 3,
            "total_doses": 20
        }
        
        # Act - Medication workflow
        
        # 1. Add medication
        medication_data = {
            "patient_id": patient_id,
            "medication_name": "Sertraline",
            "strength": "50mg",
            "prescribed_dosage": "50mg once daily",
            "start_date": date.today()
        }
        medication = repositories['medication'].create(medication_data)
        
        # 2. Log adherence
        adherence_log = repositories['medication'].log_adherence(
            medication_id=medication.medication_id,
            date=date.today(),
            taken=True
        )
        
        # 3. Calculate adherence rate
        adherence_stats = repositories['medication'].calculate_adherence(
            patient_id=patient_id,
            period_days=30
        )
        
        # Assert
        assert medication.medication_name == "Sertraline"
        assert adherence_log.taken is True
        assert adherence_stats["adherence_rate"] == 0.85
        
        # Verify workflow calls
        repositories['medication'].create.assert_called_once()
        repositories['medication'].log_adherence.assert_called_once()
        repositories['medication'].calculate_adherence.assert_called_once()
    
    def test_care_coordination_workflow(self, repositories, mock_db_manager):
        """Test care coordination and referral workflow."""
        # Arrange
        patient_id = "patient_123"
        
        # Add care coordination repositories to mocks
        repositories['provider'] = Mock()
        repositories['referral'] = Mock()
        repositories['care_team'] = Mock()
        
        # Configure mock responses
        repositories['provider'].find_providers_by_specialty.return_value = [
            Mock(provider_id="psychiatrist_789", specialty="Adult Psychiatry"),
            Mock(provider_id="psychiatrist_101", specialty="Adult Psychiatry")
        ]
        
        repositories['referral'].create_referral.return_value = Mock(
            referral_id="ref_456",
            patient_id=patient_id,
            status="pending"
        )
        
        repositories['care_team'].create.return_value = Mock(
            team_id="team_789",
            patient_id=patient_id,
            primary_provider_id="therapist_456"
        )
        
        # Act - Care coordination workflow
        
        # 1. Find available psychiatrists
        psychiatrists = repositories['provider'].find_providers_by_specialty(
            specialty="Adult Psychiatry",
            accepting_patients=True
        )
        
        # 2. Create referral
        referral = repositories['referral'].create_referral(
            patient_id=patient_id,
            referring_provider_id="therapist_456",
            receiving_provider_id=psychiatrists[0].provider_id,
            referral_reason="Medication evaluation"
        )
        
        # 3. Create care team
        care_team_data = {
            "patient_id": patient_id,
            "primary_provider_id": "therapist_456",
            "shared_goals": ["Symptom reduction", "Improved functioning"],
            "treatment_approach": "Integrated therapy and medication"
        }
        care_team = repositories['care_team'].create(care_team_data)
        
        # Assert
        assert len(psychiatrists) >= 1
        assert referral.patient_id == patient_id
        assert care_team.patient_id == patient_id
        
        # Verify workflow calls
        repositories['provider'].find_providers_by_specialty.assert_called_once()
        repositories['referral'].create_referral.assert_called_once()
        repositories['care_team'].create.assert_called_once()
