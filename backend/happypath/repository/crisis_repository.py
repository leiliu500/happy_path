"""
Crisis Management Repository

Repository implementation for crisis detection, escalation protocols,
emergency response, and safety planning functionality.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class CrisisSeverity(Enum):
    """Crisis severity enumeration."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    IMMINENT = "imminent"


class CrisisType(Enum):
    """Crisis type enumeration."""
    SUICIDAL_IDEATION = "suicidal_ideation"
    SELF_HARM = "self_harm"
    SUBSTANCE_ABUSE = "substance_abuse"
    PSYCHOTIC_EPISODE = "psychotic_episode"
    PANIC_ATTACK = "panic_attack"
    SEVERE_DEPRESSION = "severe_depression"
    DOMESTIC_VIOLENCE = "domestic_violence"
    EATING_DISORDER = "eating_disorder"
    TRAUMA_RESPONSE = "trauma_response"
    OTHER = "other"


class EscalationStatus(Enum):
    """Escalation status enumeration."""
    DETECTED = "detected"
    UNDER_REVIEW = "under_review"
    ESCALATED = "escalated"
    CONTACTED_USER = "contacted_user"
    EMERGENCY_SERVICES_CALLED = "emergency_services_called"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


@dataclass
class CrisisKeyword:
    """Crisis keyword entity."""
    keyword_id: Optional[str] = None
    keyword_phrase: str = ""
    crisis_type: CrisisType = CrisisType.OTHER
    severity_weight: Decimal = Decimal('0.5')
    context_required: bool = False
    
    # Pattern matching
    is_regex: bool = False
    case_sensitive: bool = False
    word_boundary_required: bool = True
    
    # Effectiveness tracking
    true_positive_count: int = 0
    false_positive_count: int = 0
    last_triggered: Optional[datetime] = None
    
    # Management
    is_active: bool = True
    created_by: Optional[str] = None
    reviewed_by: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CrisisDetection:
    """Crisis detection entity."""
    detection_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Detection source
    source_type: str = ""  # chat, journal, mood_entry, direct_report
    source_id: Optional[str] = None
    content_excerpt: str = ""
    full_content: Optional[str] = None
    
    # Crisis assessment
    crisis_type: CrisisType = CrisisType.OTHER
    severity_level: CrisisSeverity = CrisisSeverity.LOW
    confidence_score: Decimal = Decimal('0.5')
    
    # Detected keywords/patterns
    triggered_keywords: Optional[List[str]] = None
    keyword_scores: Optional[Dict[str, Any]] = None
    
    # Context analysis
    sentiment_score: Optional[Decimal] = None  # -1 to 1
    emotion_intensity: Optional[Decimal] = None  # 0 to 1
    temporal_indicators: Optional[List[str]] = None  # immediate, planning, historical
    contextual_factors: Optional[List[str]] = None  # isolation, recent_loss, substance_use
    
    # Detection metadata
    detection_algorithm: Optional[str] = None
    algorithm_version: Optional[str] = None
    processing_time_ms: Optional[int] = None
    
    # Review and validation
    human_reviewed: bool = False
    human_assessment: Optional[CrisisSeverity] = None
    reviewer_id: Optional[str] = None
    review_notes: Optional[str] = None
    false_positive: bool = False
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CrisisEscalation:
    """Crisis escalation entity."""
    escalation_id: Optional[str] = None
    detection_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Escalation details
    escalation_status: EscalationStatus = EscalationStatus.DETECTED
    escalated_by: Optional[str] = None  # system, user, therapist
    escalated_to: Optional[str] = None  # therapist, crisis_counselor, emergency
    
    # Timeline
    escalated_at: Optional[datetime] = None
    first_contact_attempt: Optional[datetime] = None
    user_contacted_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    # Contact attempts
    contact_methods_tried: Optional[List[str]] = None  # phone, email, sms, in_app
    contact_attempts: int = 0
    successful_contact: bool = False
    
    # Emergency services
    emergency_services_called: bool = False
    emergency_call_time: Optional[datetime] = None
    emergency_reference_number: Optional[str] = None
    emergency_responder_info: Optional[Dict[str, Any]] = None
    
    # Resolution
    resolution_summary: Optional[str] = None
    follow_up_required: bool = False
    follow_up_scheduled: Optional[datetime] = None
    
    # Documentation
    escalation_notes: Optional[str] = None
    actions_taken: Optional[List[str]] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class SafetyPlan:
    """Safety plan entity."""
    plan_id: Optional[str] = None
    user_id: Optional[str] = None
    therapist_id: Optional[str] = None
    
    # Plan details
    plan_name: str = "Personal Safety Plan"
    version_number: int = 1
    is_active: bool = True
    
    # Warning signs
    early_warning_signs: Optional[List[str]] = None
    crisis_warning_signs: Optional[List[str]] = None
    
    # Coping strategies
    internal_coping_strategies: Optional[List[str]] = None
    external_coping_strategies: Optional[List[str]] = None
    distraction_techniques: Optional[List[str]] = None
    
    # Support network
    supportive_people: Optional[List[Dict[str, Any]]] = None  # name, relationship, phone
    professional_contacts: Optional[List[Dict[str, Any]]] = None  # name, role, phone
    
    # Emergency contacts
    emergency_contacts: Optional[List[Dict[str, Any]]] = None
    crisis_hotlines: Optional[List[Dict[str, Any]]] = None
    local_emergency_services: Optional[Dict[str, Any]] = None
    
    # Environment safety
    lethal_means_removal: Optional[List[str]] = None
    safe_environment_steps: Optional[List[str]] = None
    
    # Reasons for living
    reasons_for_living: Optional[List[str]] = None
    personal_values: Optional[List[str]] = None
    future_goals: Optional[List[str]] = None
    
    # Usage tracking
    last_reviewed: Optional[datetime] = None
    last_used: Optional[datetime] = None
    usage_count: int = 0
    
    # Collaboration
    patient_input: Optional[str] = None
    family_involvement: bool = False
    shared_with_family: bool = False
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CrisisAnalytics:
    """Crisis analytics data."""
    period_start: date
    period_end: date
    
    # Detection statistics
    total_detections: int
    true_positives: int
    false_positives: int
    detection_accuracy: float
    
    # Crisis types breakdown
    crisis_types: Dict[str, int]
    severity_distribution: Dict[str, int]
    
    # Response metrics
    average_response_time: Optional[timedelta]
    escalation_rate: float
    resolution_rate: float
    
    # User engagement
    safety_plans_created: int
    safety_plans_active: int
    crisis_contacts_made: int


class CrisisKeywordRepository(BaseRepository[CrisisKeyword, str]):
    """Repository for crisis keyword management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "crisis_keywords", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> CrisisKeyword:
        """Convert database row to CrisisKeyword entity."""
        return CrisisKeyword(
            keyword_id=row.get('keyword_id'),
            keyword_phrase=row.get('keyword_phrase', ''),
            crisis_type=CrisisType(row['crisis_type']) if row.get('crisis_type') else CrisisType.OTHER,
            severity_weight=Decimal(str(row['severity_weight'])) if row.get('severity_weight') else Decimal('0.5'),
            context_required=row.get('context_required', False),
            is_regex=row.get('is_regex', False),
            case_sensitive=row.get('case_sensitive', False),
            word_boundary_required=row.get('word_boundary_required', True),
            true_positive_count=row.get('true_positive_count', 0),
            false_positive_count=row.get('false_positive_count', 0),
            last_triggered=row.get('last_triggered'),
            is_active=row.get('is_active', True),
            created_by=row.get('created_by'),
            reviewed_by=row.get('reviewed_by'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: CrisisKeyword) -> Dict[str, Any]:
        """Convert CrisisKeyword entity to dictionary."""
        return {
            'keyword_id': entity.keyword_id,
            'keyword_phrase': entity.keyword_phrase,
            'crisis_type': entity.crisis_type.value,
            'severity_weight': entity.severity_weight,
            'context_required': entity.context_required,
            'is_regex': entity.is_regex,
            'case_sensitive': entity.case_sensitive,
            'word_boundary_required': entity.word_boundary_required,
            'true_positive_count': entity.true_positive_count,
            'false_positive_count': entity.false_positive_count,
            'last_triggered': entity.last_triggered,
            'is_active': entity.is_active,
            'created_by': entity.created_by,
            'reviewed_by': entity.reviewed_by,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: CrisisKeyword, is_update: bool = False) -> None:
        """Validate CrisisKeyword entity."""
        if not entity.keyword_phrase:
            raise ValidationError("Keyword phrase is required")
        
        if entity.severity_weight < 0 or entity.severity_weight > 1:
            raise ValidationError("Severity weight must be between 0 and 1")
        
        if not entity.keyword_id and not is_update:
            import uuid
            entity.keyword_id = str(uuid.uuid4())
    
    def get_active_keywords(self, crisis_type: CrisisType = None) -> List[CrisisKeyword]:
        """Get active crisis keywords."""
        filters = {'is_active': True}
        if crisis_type:
            filters['crisis_type'] = crisis_type.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['-severity_weight']
        )
        
        result = self.list_all(options)
        return result.data
    
    def update_effectiveness(self, keyword_id: str, is_true_positive: bool) -> bool:
        """Update keyword effectiveness tracking."""
        try:
            keyword = self.get_by_id(keyword_id)
            if not keyword:
                return False
            
            if is_true_positive:
                keyword.true_positive_count += 1
            else:
                keyword.false_positive_count += 1
            
            keyword.last_triggered = datetime.now()
            
            self.update(keyword)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update keyword effectiveness: {e}")
            return False


class CrisisDetectionRepository(BaseRepository[CrisisDetection, str]):
    """Repository for crisis detection management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "crisis_detections", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> CrisisDetection:
        """Convert database row to CrisisDetection entity."""
        return CrisisDetection(
            detection_id=row.get('detection_id'),
            user_id=row.get('user_id'),
            source_type=row.get('source_type', ''),
            source_id=row.get('source_id'),
            content_excerpt=row.get('content_excerpt', ''),
            full_content=row.get('full_content'),
            crisis_type=CrisisType(row['crisis_type']) if row.get('crisis_type') else CrisisType.OTHER,
            severity_level=CrisisSeverity(row['severity_level']) if row.get('severity_level') else CrisisSeverity.LOW,
            confidence_score=Decimal(str(row['confidence_score'])) if row.get('confidence_score') else Decimal('0.5'),
            triggered_keywords=row.get('triggered_keywords', []),
            keyword_scores=row.get('keyword_scores'),
            sentiment_score=Decimal(str(row['sentiment_score'])) if row.get('sentiment_score') else None,
            emotion_intensity=Decimal(str(row['emotion_intensity'])) if row.get('emotion_intensity') else None,
            temporal_indicators=row.get('temporal_indicators', []),
            contextual_factors=row.get('contextual_factors', []),
            detection_algorithm=row.get('detection_algorithm'),
            algorithm_version=row.get('algorithm_version'),
            processing_time_ms=row.get('processing_time_ms'),
            human_reviewed=row.get('human_reviewed', False),
            human_assessment=CrisisSeverity(row['human_assessment']) if row.get('human_assessment') else None,
            reviewer_id=row.get('reviewer_id'),
            review_notes=row.get('review_notes'),
            false_positive=row.get('false_positive', False),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: CrisisDetection) -> Dict[str, Any]:
        """Convert CrisisDetection entity to dictionary."""
        return {
            'detection_id': entity.detection_id,
            'user_id': entity.user_id,
            'source_type': entity.source_type,
            'source_id': entity.source_id,
            'content_excerpt': entity.content_excerpt,
            'full_content': entity.full_content,
            'crisis_type': entity.crisis_type.value,
            'severity_level': entity.severity_level.value,
            'confidence_score': entity.confidence_score,
            'triggered_keywords': entity.triggered_keywords,
            'keyword_scores': entity.keyword_scores,
            'sentiment_score': entity.sentiment_score,
            'emotion_intensity': entity.emotion_intensity,
            'temporal_indicators': entity.temporal_indicators,
            'contextual_factors': entity.contextual_factors,
            'detection_algorithm': entity.detection_algorithm,
            'algorithm_version': entity.algorithm_version,
            'processing_time_ms': entity.processing_time_ms,
            'human_reviewed': entity.human_reviewed,
            'human_assessment': entity.human_assessment.value if entity.human_assessment else None,
            'reviewer_id': entity.reviewer_id,
            'review_notes': entity.review_notes,
            'false_positive': entity.false_positive,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: CrisisDetection, is_update: bool = False) -> None:
        """Validate CrisisDetection entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.source_type:
            raise ValidationError("Source type is required")
        
        if not entity.content_excerpt:
            raise ValidationError("Content excerpt is required")
        
        if entity.confidence_score < 0 or entity.confidence_score > 1:
            raise ValidationError("Confidence score must be between 0 and 1")
        
        if entity.sentiment_score and (entity.sentiment_score < -1 or entity.sentiment_score > 1):
            raise ValidationError("Sentiment score must be between -1 and 1")
        
        if entity.emotion_intensity and (entity.emotion_intensity < 0 or entity.emotion_intensity > 1):
            raise ValidationError("Emotion intensity must be between 0 and 1")
        
        if not entity.detection_id and not is_update:
            import uuid
            entity.detection_id = str(uuid.uuid4())
    
    def get_user_detections(self, user_id: str, start_date: date = None, 
                           end_date: date = None, severity: CrisisSeverity = None) -> List[CrisisDetection]:
        """Get crisis detections for a user."""
        filters = {'user_id': user_id}
        
        if start_date:
            filters['created_at__gte'] = datetime.combine(start_date, datetime.min.time())
        if end_date:
            filters['created_at__lte'] = datetime.combine(end_date, datetime.max.time())
        if severity:
            filters['severity_level'] = severity.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['-created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_pending_review(self, limit: Optional[int] = None) -> List[CrisisDetection]:
        """Get detections pending human review."""
        options = QueryOptions(
            filters={
                'human_reviewed': False,
                'severity_level__in': ['high', 'critical', 'imminent']
            },
            order_by=['-severity_level', '-created_at'],
            limit=limit
        )
        
        result = self.list_all(options)
        return result.data
    
    def mark_reviewed(self, detection_id: str, reviewer_id: str, 
                     assessment: CrisisSeverity, notes: str = "",
                     false_positive: bool = False) -> bool:
        """Mark detection as reviewed."""
        try:
            detection = self.get_by_id(detection_id)
            if not detection:
                return False
            
            detection.human_reviewed = True
            detection.human_assessment = assessment
            detection.reviewer_id = reviewer_id
            detection.review_notes = notes
            detection.false_positive = false_positive
            
            self.update(detection)
            
            self.logger.info(f"Marked detection {detection_id} as reviewed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to mark detection as reviewed: {e}")
            return False


class CrisisEscalationRepository(BaseRepository[CrisisEscalation, str]):
    """Repository for crisis escalation management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "crisis_escalations", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> CrisisEscalation:
        """Convert database row to CrisisEscalation entity."""
        return CrisisEscalation(
            escalation_id=row.get('escalation_id'),
            detection_id=row.get('detection_id'),
            user_id=row.get('user_id'),
            escalation_status=EscalationStatus(row['escalation_status']) if row.get('escalation_status') else EscalationStatus.DETECTED,
            escalated_by=row.get('escalated_by'),
            escalated_to=row.get('escalated_to'),
            escalated_at=row.get('escalated_at'),
            first_contact_attempt=row.get('first_contact_attempt'),
            user_contacted_at=row.get('user_contacted_at'),
            resolved_at=row.get('resolved_at'),
            contact_methods_tried=row.get('contact_methods_tried', []),
            contact_attempts=row.get('contact_attempts', 0),
            successful_contact=row.get('successful_contact', False),
            emergency_services_called=row.get('emergency_services_called', False),
            emergency_call_time=row.get('emergency_call_time'),
            emergency_reference_number=row.get('emergency_reference_number'),
            emergency_responder_info=row.get('emergency_responder_info'),
            resolution_summary=row.get('resolution_summary'),
            follow_up_required=row.get('follow_up_required', False),
            follow_up_scheduled=row.get('follow_up_scheduled'),
            escalation_notes=row.get('escalation_notes'),
            actions_taken=row.get('actions_taken', []),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: CrisisEscalation) -> Dict[str, Any]:
        """Convert CrisisEscalation entity to dictionary."""
        return {
            'escalation_id': entity.escalation_id,
            'detection_id': entity.detection_id,
            'user_id': entity.user_id,
            'escalation_status': entity.escalation_status.value,
            'escalated_by': entity.escalated_by,
            'escalated_to': entity.escalated_to,
            'escalated_at': entity.escalated_at,
            'first_contact_attempt': entity.first_contact_attempt,
            'user_contacted_at': entity.user_contacted_at,
            'resolved_at': entity.resolved_at,
            'contact_methods_tried': entity.contact_methods_tried,
            'contact_attempts': entity.contact_attempts,
            'successful_contact': entity.successful_contact,
            'emergency_services_called': entity.emergency_services_called,
            'emergency_call_time': entity.emergency_call_time,
            'emergency_reference_number': entity.emergency_reference_number,
            'emergency_responder_info': entity.emergency_responder_info,
            'resolution_summary': entity.resolution_summary,
            'follow_up_required': entity.follow_up_required,
            'follow_up_scheduled': entity.follow_up_scheduled,
            'escalation_notes': entity.escalation_notes,
            'actions_taken': entity.actions_taken,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: CrisisEscalation, is_update: bool = False) -> None:
        """Validate CrisisEscalation entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if entity.contact_attempts < 0:
            raise ValidationError("Contact attempts must be non-negative")
        
        if not entity.escalation_id and not is_update:
            import uuid
            entity.escalation_id = str(uuid.uuid4())
    
    def get_active_escalations(self, escalated_to: str = None) -> List[CrisisEscalation]:
        """Get active escalations."""
        filters = {
            'escalation_status__in': ['escalated', 'under_review', 'contacted_user']
        }
        
        if escalated_to:
            filters['escalated_to'] = escalated_to
        
        options = QueryOptions(
            filters=filters,
            order_by=['-escalated_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def update_contact_attempt(self, escalation_id: str, method: str, 
                             successful: bool = False) -> bool:
        """Update contact attempt information."""
        try:
            escalation = self.get_by_id(escalation_id)
            if not escalation:
                return False
            
            escalation.contact_attempts += 1
            
            if not escalation.contact_methods_tried:
                escalation.contact_methods_tried = []
            escalation.contact_methods_tried.append(method)
            
            if successful:
                escalation.successful_contact = True
                escalation.user_contacted_at = datetime.now()
                escalation.escalation_status = EscalationStatus.CONTACTED_USER
            
            if not escalation.first_contact_attempt:
                escalation.first_contact_attempt = datetime.now()
            
            self.update(escalation)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update contact attempt: {e}")
            return False


class SafetyPlanRepository(BaseRepository[SafetyPlan, str]):
    """Repository for safety plan management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "safety_plans", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> SafetyPlan:
        """Convert database row to SafetyPlan entity."""
        return SafetyPlan(
            plan_id=row.get('plan_id'),
            user_id=row.get('user_id'),
            therapist_id=row.get('therapist_id'),
            plan_name=row.get('plan_name', 'Personal Safety Plan'),
            version_number=row.get('version_number', 1),
            is_active=row.get('is_active', True),
            early_warning_signs=row.get('early_warning_signs', []),
            crisis_warning_signs=row.get('crisis_warning_signs', []),
            internal_coping_strategies=row.get('internal_coping_strategies', []),
            external_coping_strategies=row.get('external_coping_strategies', []),
            distraction_techniques=row.get('distraction_techniques', []),
            supportive_people=row.get('supportive_people', []),
            professional_contacts=row.get('professional_contacts', []),
            emergency_contacts=row.get('emergency_contacts', []),
            crisis_hotlines=row.get('crisis_hotlines', []),
            local_emergency_services=row.get('local_emergency_services'),
            lethal_means_removal=row.get('lethal_means_removal', []),
            safe_environment_steps=row.get('safe_environment_steps', []),
            reasons_for_living=row.get('reasons_for_living', []),
            personal_values=row.get('personal_values', []),
            future_goals=row.get('future_goals', []),
            last_reviewed=row.get('last_reviewed'),
            last_used=row.get('last_used'),
            usage_count=row.get('usage_count', 0),
            patient_input=row.get('patient_input'),
            family_involvement=row.get('family_involvement', False),
            shared_with_family=row.get('shared_with_family', False),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: SafetyPlan) -> Dict[str, Any]:
        """Convert SafetyPlan entity to dictionary."""
        return {
            'plan_id': entity.plan_id,
            'user_id': entity.user_id,
            'therapist_id': entity.therapist_id,
            'plan_name': entity.plan_name,
            'version_number': entity.version_number,
            'is_active': entity.is_active,
            'early_warning_signs': entity.early_warning_signs,
            'crisis_warning_signs': entity.crisis_warning_signs,
            'internal_coping_strategies': entity.internal_coping_strategies,
            'external_coping_strategies': entity.external_coping_strategies,
            'distraction_techniques': entity.distraction_techniques,
            'supportive_people': entity.supportive_people,
            'professional_contacts': entity.professional_contacts,
            'emergency_contacts': entity.emergency_contacts,
            'crisis_hotlines': entity.crisis_hotlines,
            'local_emergency_services': entity.local_emergency_services,
            'lethal_means_removal': entity.lethal_means_removal,
            'safe_environment_steps': entity.safe_environment_steps,
            'reasons_for_living': entity.reasons_for_living,
            'personal_values': entity.personal_values,
            'future_goals': entity.future_goals,
            'last_reviewed': entity.last_reviewed,
            'last_used': entity.last_used,
            'usage_count': entity.usage_count,
            'patient_input': entity.patient_input,
            'family_involvement': entity.family_involvement,
            'shared_with_family': entity.shared_with_family,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: SafetyPlan, is_update: bool = False) -> None:
        """Validate SafetyPlan entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if entity.version_number <= 0:
            raise ValidationError("Version number must be positive")
        
        if entity.usage_count < 0:
            raise ValidationError("Usage count must be non-negative")
        
        if not entity.plan_id and not is_update:
            import uuid
            entity.plan_id = str(uuid.uuid4())
    
    def get_user_safety_plan(self, user_id: str) -> Optional[SafetyPlan]:
        """Get active safety plan for a user."""
        return self.find_one_by(user_id=user_id, is_active=True)
    
    def record_usage(self, plan_id: str) -> bool:
        """Record usage of safety plan."""
        try:
            plan = self.get_by_id(plan_id)
            if not plan:
                return False
            
            plan.usage_count += 1
            plan.last_used = datetime.now()
            
            self.update(plan)
            
            self.logger.info(f"Recorded usage of safety plan {plan_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to record safety plan usage: {e}")
            return False
