"""
Clinical and Therapy Repository

Repository implementation for clinical therapy support, therapeutic relationships,
treatment plans, and clinical oversight functionality.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class TherapyModality(Enum):
    """Therapy modality enumeration."""
    CBT = "cbt"
    DBT = "dbt"
    EMDR = "emdr"
    PSYCHODYNAMIC = "psychodynamic"
    HUMANISTIC = "humanistic"
    GESTALT = "gestalt"
    FAMILY_THERAPY = "family_therapy"
    GROUP_THERAPY = "group_therapy"
    MINDFULNESS_BASED = "mindfulness_based"
    ACCEPTANCE_COMMITMENT = "acceptance_commitment"
    INTERPERSONAL = "interpersonal"
    SOLUTION_FOCUSED = "solution_focused"


class TreatmentPhase(Enum):
    """Treatment phase enumeration."""
    ASSESSMENT = "assessment"
    ENGAGEMENT = "engagement"
    ACTIVE_TREATMENT = "active_treatment"
    MAINTENANCE = "maintenance"
    RELAPSE_PREVENTION = "relapse_prevention"
    TERMINATION = "termination"
    FOLLOW_UP = "follow_up"


class ClinicalSeverity(Enum):
    """Clinical severity enumeration."""
    MINIMAL = "minimal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    EXTREME = "extreme"


@dataclass
class TherapeuticRelationship:
    """Therapeutic relationship entity."""
    relationship_id: Optional[str] = None
    therapist_id: Optional[str] = None
    patient_id: Optional[str] = None
    
    # Relationship details
    relationship_type: str = "primary"  # primary, consulting, supervision
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    
    # Treatment context
    primary_modality: Optional[TherapyModality] = None
    secondary_modalities: Optional[List[TherapyModality]] = None
    treatment_setting: Optional[str] = None  # in_person, telehealth, hybrid, app_assisted
    
    # Clinical information
    presenting_concerns: Optional[List[str]] = None
    diagnosis_codes: Optional[List[str]] = None  # ICD-10 codes
    treatment_goals: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None
    
    # Session logistics
    typical_session_length: int = 50  # minutes
    session_frequency: str = "weekly"
    preferred_session_times: Optional[Dict[str, Any]] = None
    
    # Consent and agreements
    informed_consent_obtained: bool = False
    app_integration_consent: bool = False
    data_sharing_consent: bool = False
    emergency_contact_consent: bool = False
    
    # Clinical notes access
    notes_access_level: str = "summary"  # none, summary, full
    patient_access_to_notes: bool = False
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class TreatmentPlan:
    """Treatment plan entity."""
    plan_id: Optional[str] = None
    relationship_id: Optional[str] = None
    patient_id: Optional[str] = None
    therapist_id: Optional[str] = None
    
    # Plan details
    plan_name: str = ""
    version_number: int = 1
    is_current: bool = True
    
    # Clinical assessment
    current_phase: TreatmentPhase = TreatmentPhase.ASSESSMENT
    severity_level: Optional[ClinicalSeverity] = None
    risk_level: Optional[str] = None  # low, moderate, high
    
    # Goals and objectives
    long_term_goals: Optional[List[Dict[str, Any]]] = None
    short_term_objectives: Optional[List[Dict[str, Any]]] = None
    behavioral_targets: Optional[List[Dict[str, Any]]] = None
    
    # Treatment approach
    primary_interventions: Optional[List[str]] = None
    therapeutic_techniques: Optional[List[str]] = None
    homework_assignments: Optional[List[str]] = None
    between_session_activities: Optional[List[str]] = None
    
    # App integration
    app_supported_interventions: Optional[List[str]] = None
    digital_homework: Optional[List[Dict[str, Any]]] = None
    mood_tracking_required: bool = True
    journaling_assignments: Optional[List[str]] = None
    
    # Crisis planning
    crisis_indicators: Optional[List[str]] = None
    crisis_response_plan: Optional[str] = None
    safety_plan_required: bool = False
    
    # Progress measurement
    outcome_measures: Optional[List[str]] = None
    progress_indicators: Optional[List[Dict[str, Any]]] = None
    measurement_frequency: str = "weekly"
    
    # Timeline
    estimated_duration_sessions: Optional[int] = None
    target_completion_date: Optional[date] = None
    review_date: Optional[date] = None
    
    # Collaboration
    patient_input: Optional[str] = None
    family_involvement: bool = False
    care_team_members: Optional[List[Dict[str, Any]]] = None
    
    # Documentation
    clinical_rationale: str = ""
    evidence_base: Optional[str] = None
    cultural_considerations: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class TherapySession:
    """Therapy session entity."""
    session_id: Optional[str] = None
    relationship_id: Optional[str] = None
    patient_id: Optional[str] = None
    therapist_id: Optional[str] = None
    
    # Session details
    session_number: Optional[int] = None
    session_date: Optional[datetime] = None
    duration_minutes: int = 50
    session_type: str = "individual"  # individual, group, family, couples
    modality: str = "in_person"  # in_person, telehealth, phone
    
    # Session content
    session_goals: Optional[List[str]] = None
    topics_discussed: Optional[List[str]] = None
    interventions_used: Optional[List[str]] = None
    homework_assigned: Optional[List[str]] = None
    
    # Progress and assessment
    patient_mood_start: Optional[int] = None  # 1-10 scale
    patient_mood_end: Optional[int] = None
    session_rating: Optional[int] = None  # Patient rating 1-10
    therapist_notes: Optional[str] = None
    
    # Risk assessment
    suicide_risk_level: str = "none"  # none, low, moderate, high
    self_harm_risk: str = "none"
    crisis_indicators_present: Optional[List[str]] = None
    safety_plan_reviewed: bool = False
    
    # Technical details
    video_quality_issues: bool = False
    audio_quality_issues: bool = False
    technical_notes: Optional[str] = None
    
    # Administrative
    billing_status: str = "pending"  # pending, billed, paid, disputed
    billing_code: Optional[str] = None
    insurance_authorization: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TherapeuticRelationshipRepository(BaseRepository[TherapeuticRelationship, str]):
    """Repository for therapeutic relationship management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "therapeutic_relationships", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> TherapeuticRelationship:
        """Convert database row to TherapeuticRelationship entity."""
        return TherapeuticRelationship(
            relationship_id=row.get('relationship_id'),
            therapist_id=row.get('therapist_id'),
            patient_id=row.get('patient_id'),
            relationship_type=row.get('relationship_type', 'primary'),
            start_date=row.get('start_date'),
            end_date=row.get('end_date'),
            is_active=row.get('is_active', True),
            primary_modality=TherapyModality(row['primary_modality']) if row.get('primary_modality') else None,
            secondary_modalities=[TherapyModality(m) for m in row.get('secondary_modalities', [])],
            treatment_setting=row.get('treatment_setting'),
            presenting_concerns=row.get('presenting_concerns', []),
            diagnosis_codes=row.get('diagnosis_codes', []),
            treatment_goals=row.get('treatment_goals', []),
            contraindications=row.get('contraindications', []),
            typical_session_length=row.get('typical_session_length', 50),
            session_frequency=row.get('session_frequency', 'weekly'),
            preferred_session_times=row.get('preferred_session_times'),
            informed_consent_obtained=row.get('informed_consent_obtained', False),
            app_integration_consent=row.get('app_integration_consent', False),
            data_sharing_consent=row.get('data_sharing_consent', False),
            emergency_contact_consent=row.get('emergency_contact_consent', False),
            notes_access_level=row.get('notes_access_level', 'summary'),
            patient_access_to_notes=row.get('patient_access_to_notes', False),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: TherapeuticRelationship) -> Dict[str, Any]:
        """Convert TherapeuticRelationship entity to dictionary."""
        return {
            'relationship_id': entity.relationship_id,
            'therapist_id': entity.therapist_id,
            'patient_id': entity.patient_id,
            'relationship_type': entity.relationship_type,
            'start_date': entity.start_date,
            'end_date': entity.end_date,
            'is_active': entity.is_active,
            'primary_modality': entity.primary_modality.value if entity.primary_modality else None,
            'secondary_modalities': [m.value for m in entity.secondary_modalities] if entity.secondary_modalities else [],
            'treatment_setting': entity.treatment_setting,
            'presenting_concerns': entity.presenting_concerns,
            'diagnosis_codes': entity.diagnosis_codes,
            'treatment_goals': entity.treatment_goals,
            'contraindications': entity.contraindications,
            'typical_session_length': entity.typical_session_length,
            'session_frequency': entity.session_frequency,
            'preferred_session_times': entity.preferred_session_times,
            'informed_consent_obtained': entity.informed_consent_obtained,
            'app_integration_consent': entity.app_integration_consent,
            'data_sharing_consent': entity.data_sharing_consent,
            'emergency_contact_consent': entity.emergency_contact_consent,
            'notes_access_level': entity.notes_access_level,
            'patient_access_to_notes': entity.patient_access_to_notes,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: TherapeuticRelationship, is_update: bool = False) -> None:
        """Validate TherapeuticRelationship entity."""
        if not entity.therapist_id:
            raise ValidationError("Therapist ID is required")
        
        if not entity.patient_id:
            raise ValidationError("Patient ID is required")
        
        if entity.therapist_id == entity.patient_id:
            raise ValidationError("Therapist and patient cannot be the same person")
        
        if not entity.start_date:
            entity.start_date = date.today()
        
        if entity.end_date and entity.start_date and entity.end_date < entity.start_date:
            raise ValidationError("End date cannot be before start date")
        
        if entity.typical_session_length <= 0:
            raise ValidationError("Session length must be positive")
        
        if not entity.relationship_id and not is_update:
            import uuid
            entity.relationship_id = str(uuid.uuid4())
    
    def get_patient_relationships(self, patient_id: str, active_only: bool = True) -> List[TherapeuticRelationship]:
        """Get all therapeutic relationships for a patient."""
        filters = {'patient_id': patient_id}
        if active_only:
            filters['is_active'] = True
        
        options = QueryOptions(
            filters=filters,
            order_by=['-start_date']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_therapist_relationships(self, therapist_id: str, active_only: bool = True) -> List[TherapeuticRelationship]:
        """Get all therapeutic relationships for a therapist."""
        filters = {'therapist_id': therapist_id}
        if active_only:
            filters['is_active'] = True
        
        options = QueryOptions(
            filters=filters,
            order_by=['-start_date']
        )
        
        result = self.list_all(options)
        return result.data
    
    def find_active_relationship(self, therapist_id: str, patient_id: str) -> Optional[TherapeuticRelationship]:
        """Find active relationship between therapist and patient."""
        return self.find_one_by(
            therapist_id=therapist_id,
            patient_id=patient_id,
            is_active=True
        )
    
    def end_relationship(self, relationship_id: str, end_date: date = None) -> bool:
        """End a therapeutic relationship."""
        try:
            relationship = self.get_by_id(relationship_id)
            if not relationship:
                return False
            
            relationship.is_active = False
            relationship.end_date = end_date or date.today()
            
            self.update(relationship)
            
            self.logger.info(f"Ended therapeutic relationship {relationship_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to end relationship {relationship_id}: {e}")
            return False


class TreatmentPlanRepository(BaseRepository[TreatmentPlan, str]):
    """Repository for treatment plan management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "treatment_plans", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> TreatmentPlan:
        """Convert database row to TreatmentPlan entity."""
        return TreatmentPlan(
            plan_id=row.get('plan_id'),
            relationship_id=row.get('relationship_id'),
            patient_id=row.get('patient_id'),
            therapist_id=row.get('therapist_id'),
            plan_name=row.get('plan_name', ''),
            version_number=row.get('version_number', 1),
            is_current=row.get('is_current', True),
            current_phase=TreatmentPhase(row['current_phase']) if row.get('current_phase') else TreatmentPhase.ASSESSMENT,
            severity_level=ClinicalSeverity(row['severity_level']) if row.get('severity_level') else None,
            risk_level=row.get('risk_level'),
            long_term_goals=row.get('long_term_goals', []),
            short_term_objectives=row.get('short_term_objectives', []),
            behavioral_targets=row.get('behavioral_targets', []),
            primary_interventions=row.get('primary_interventions', []),
            therapeutic_techniques=row.get('therapeutic_techniques', []),
            homework_assignments=row.get('homework_assignments', []),
            between_session_activities=row.get('between_session_activities', []),
            app_supported_interventions=row.get('app_supported_interventions', []),
            digital_homework=row.get('digital_homework', []),
            mood_tracking_required=row.get('mood_tracking_required', True),
            journaling_assignments=row.get('journaling_assignments', []),
            crisis_indicators=row.get('crisis_indicators', []),
            crisis_response_plan=row.get('crisis_response_plan'),
            safety_plan_required=row.get('safety_plan_required', False),
            outcome_measures=row.get('outcome_measures', []),
            progress_indicators=row.get('progress_indicators', []),
            measurement_frequency=row.get('measurement_frequency', 'weekly'),
            estimated_duration_sessions=row.get('estimated_duration_sessions'),
            target_completion_date=row.get('target_completion_date'),
            review_date=row.get('review_date'),
            patient_input=row.get('patient_input'),
            family_involvement=row.get('family_involvement', False),
            care_team_members=row.get('care_team_members', []),
            clinical_rationale=row.get('clinical_rationale', ''),
            evidence_base=row.get('evidence_base'),
            cultural_considerations=row.get('cultural_considerations'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: TreatmentPlan) -> Dict[str, Any]:
        """Convert TreatmentPlan entity to dictionary."""
        return {
            'plan_id': entity.plan_id,
            'relationship_id': entity.relationship_id,
            'patient_id': entity.patient_id,
            'therapist_id': entity.therapist_id,
            'plan_name': entity.plan_name,
            'version_number': entity.version_number,
            'is_current': entity.is_current,
            'current_phase': entity.current_phase.value,
            'severity_level': entity.severity_level.value if entity.severity_level else None,
            'risk_level': entity.risk_level,
            'long_term_goals': entity.long_term_goals,
            'short_term_objectives': entity.short_term_objectives,
            'behavioral_targets': entity.behavioral_targets,
            'primary_interventions': entity.primary_interventions,
            'therapeutic_techniques': entity.therapeutic_techniques,
            'homework_assignments': entity.homework_assignments,
            'between_session_activities': entity.between_session_activities,
            'app_supported_interventions': entity.app_supported_interventions,
            'digital_homework': entity.digital_homework,
            'mood_tracking_required': entity.mood_tracking_required,
            'journaling_assignments': entity.journaling_assignments,
            'crisis_indicators': entity.crisis_indicators,
            'crisis_response_plan': entity.crisis_response_plan,
            'safety_plan_required': entity.safety_plan_required,
            'outcome_measures': entity.outcome_measures,
            'progress_indicators': entity.progress_indicators,
            'measurement_frequency': entity.measurement_frequency,
            'estimated_duration_sessions': entity.estimated_duration_sessions,
            'target_completion_date': entity.target_completion_date,
            'review_date': entity.review_date,
            'patient_input': entity.patient_input,
            'family_involvement': entity.family_involvement,
            'care_team_members': entity.care_team_members,
            'clinical_rationale': entity.clinical_rationale,
            'evidence_base': entity.evidence_base,
            'cultural_considerations': entity.cultural_considerations,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: TreatmentPlan, is_update: bool = False) -> None:
        """Validate TreatmentPlan entity."""
        if not entity.relationship_id:
            raise ValidationError("Relationship ID is required")
        
        if not entity.patient_id:
            raise ValidationError("Patient ID is required")
        
        if not entity.therapist_id:
            raise ValidationError("Therapist ID is required")
        
        if not entity.plan_name:
            raise ValidationError("Plan name is required")
        
        if not entity.clinical_rationale:
            raise ValidationError("Clinical rationale is required")
        
        if entity.version_number <= 0:
            raise ValidationError("Version number must be positive")
        
        if entity.estimated_duration_sessions and entity.estimated_duration_sessions <= 0:
            raise ValidationError("Estimated duration must be positive")
        
        if not entity.review_date:
            entity.review_date = date.today() + timedelta(days=30)
        
        if not entity.plan_id and not is_update:
            import uuid
            entity.plan_id = str(uuid.uuid4())
    
    def get_current_plan(self, relationship_id: str) -> Optional[TreatmentPlan]:
        """Get current treatment plan for a relationship."""
        return self.find_one_by(
            relationship_id=relationship_id,
            is_current=True
        )
    
    def get_patient_plans(self, patient_id: str, current_only: bool = True) -> List[TreatmentPlan]:
        """Get treatment plans for a patient."""
        filters = {'patient_id': patient_id}
        if current_only:
            filters['is_current'] = True
        
        options = QueryOptions(
            filters=filters,
            order_by=['-version_number', '-created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def create_new_version(self, plan_id: str, updates: Dict[str, Any]) -> TreatmentPlan:
        """Create new version of treatment plan."""
        current_plan = self.get_by_id(plan_id)
        if not current_plan:
            raise NotFoundError(f"Treatment plan {plan_id} not found")
        
        # Mark current plan as not current
        current_plan.is_current = False
        self.update(current_plan)
        
        # Create new version
        new_plan_dict = self._to_dict(current_plan)
        new_plan_dict.update(updates)
        new_plan_dict['plan_id'] = None  # Will be auto-generated
        new_plan_dict['version_number'] = current_plan.version_number + 1
        new_plan_dict['is_current'] = True
        new_plan_dict['created_at'] = None
        new_plan_dict['updated_at'] = None
        
        new_plan = self._to_entity(new_plan_dict)
        return self.create(new_plan)


class TherapySessionRepository(BaseRepository[TherapySession, str]):
    """Repository for therapy session management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "therapy_sessions", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> TherapySession:
        """Convert database row to TherapySession entity."""
        return TherapySession(
            session_id=row.get('session_id'),
            relationship_id=row.get('relationship_id'),
            patient_id=row.get('patient_id'),
            therapist_id=row.get('therapist_id'),
            session_number=row.get('session_number'),
            session_date=row.get('session_date'),
            duration_minutes=row.get('duration_minutes', 50),
            session_type=row.get('session_type', 'individual'),
            modality=row.get('modality', 'in_person'),
            session_goals=row.get('session_goals', []),
            topics_discussed=row.get('topics_discussed', []),
            interventions_used=row.get('interventions_used', []),
            homework_assigned=row.get('homework_assigned', []),
            patient_mood_start=row.get('patient_mood_start'),
            patient_mood_end=row.get('patient_mood_end'),
            session_rating=row.get('session_rating'),
            therapist_notes=row.get('therapist_notes'),
            suicide_risk_level=row.get('suicide_risk_level', 'none'),
            self_harm_risk=row.get('self_harm_risk', 'none'),
            crisis_indicators_present=row.get('crisis_indicators_present', []),
            safety_plan_reviewed=row.get('safety_plan_reviewed', False),
            video_quality_issues=row.get('video_quality_issues', False),
            audio_quality_issues=row.get('audio_quality_issues', False),
            technical_notes=row.get('technical_notes'),
            billing_status=row.get('billing_status', 'pending'),
            billing_code=row.get('billing_code'),
            insurance_authorization=row.get('insurance_authorization'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: TherapySession) -> Dict[str, Any]:
        """Convert TherapySession entity to dictionary."""
        return {
            'session_id': entity.session_id,
            'relationship_id': entity.relationship_id,
            'patient_id': entity.patient_id,
            'therapist_id': entity.therapist_id,
            'session_number': entity.session_number,
            'session_date': entity.session_date,
            'duration_minutes': entity.duration_minutes,
            'session_type': entity.session_type,
            'modality': entity.modality,
            'session_goals': entity.session_goals,
            'topics_discussed': entity.topics_discussed,
            'interventions_used': entity.interventions_used,
            'homework_assigned': entity.homework_assigned,
            'patient_mood_start': entity.patient_mood_start,
            'patient_mood_end': entity.patient_mood_end,
            'session_rating': entity.session_rating,
            'therapist_notes': entity.therapist_notes,
            'suicide_risk_level': entity.suicide_risk_level,
            'self_harm_risk': entity.self_harm_risk,
            'crisis_indicators_present': entity.crisis_indicators_present,
            'safety_plan_reviewed': entity.safety_plan_reviewed,
            'video_quality_issues': entity.video_quality_issues,
            'audio_quality_issues': entity.audio_quality_issues,
            'technical_notes': entity.technical_notes,
            'billing_status': entity.billing_status,
            'billing_code': entity.billing_code,
            'insurance_authorization': entity.insurance_authorization,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: TherapySession, is_update: bool = False) -> None:
        """Validate TherapySession entity."""
        if not entity.relationship_id:
            raise ValidationError("Relationship ID is required")
        
        if not entity.patient_id:
            raise ValidationError("Patient ID is required")
        
        if not entity.therapist_id:
            raise ValidationError("Therapist ID is required")
        
        if entity.duration_minutes <= 0:
            raise ValidationError("Session duration must be positive")
        
        if entity.patient_mood_start and (entity.patient_mood_start < 1 or entity.patient_mood_start > 10):
            raise ValidationError("Patient mood start must be between 1 and 10")
        
        if entity.patient_mood_end and (entity.patient_mood_end < 1 or entity.patient_mood_end > 10):
            raise ValidationError("Patient mood end must be between 1 and 10")
        
        if entity.session_rating and (entity.session_rating < 1 or entity.session_rating > 10):
            raise ValidationError("Session rating must be between 1 and 10")
        
        if not entity.session_id and not is_update:
            import uuid
            entity.session_id = str(uuid.uuid4())
    
    def get_patient_sessions(self, patient_id: str, limit: Optional[int] = None) -> List[TherapySession]:
        """Get therapy sessions for a patient."""
        options = QueryOptions(
            filters={'patient_id': patient_id},
            order_by=['-session_date'],
            limit=limit
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_therapist_sessions(self, therapist_id: str, start_date: date = None, 
                             end_date: date = None) -> List[TherapySession]:
        """Get therapy sessions for a therapist."""
        filters = {'therapist_id': therapist_id}
        
        # Add date filters if provided
        if start_date:
            filters['session_date__gte'] = start_date
        if end_date:
            filters['session_date__lte'] = end_date
        
        options = QueryOptions(
            filters=filters,
            order_by=['-session_date']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_relationship_sessions(self, relationship_id: str) -> List[TherapySession]:
        """Get all sessions for a therapeutic relationship."""
        options = QueryOptions(
            filters={'relationship_id': relationship_id},
            order_by=['session_number', 'session_date']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_next_session_number(self, relationship_id: str) -> int:
        """Get the next session number for a relationship."""
        try:
            query = f"""
                SELECT COALESCE(MAX(session_number), 0) + 1 as next_number
                FROM {self.table_name}
                WHERE relationship_id = %(relationship_id)s
            """
            
            result = self.db.execute_query(query, {'relationship_id': relationship_id})
            return result[0]['next_number'] if result else 1
            
        except Exception as e:
            self.logger.error(f"Failed to get next session number: {e}")
            return 1
