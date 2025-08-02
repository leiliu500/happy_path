"""
Care Coordination Repository

Repository implementation for care coordination, provider networks,
referrals, and multidisciplinary care team management.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging
import json

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class ProviderType(Enum):
    """Provider type enumeration."""
    PRIMARY_THERAPIST = "primary_therapist"
    PSYCHIATRIST = "psychiatrist"
    PSYCHOLOGIST = "psychologist"
    COUNSELOR = "counselor"
    SOCIAL_WORKER = "social_worker"
    CASE_MANAGER = "case_manager"
    PEER_SUPPORT = "peer_support"
    FAMILY_THERAPIST = "family_therapist"
    GROUP_FACILITATOR = "group_facilitator"
    CRISIS_COUNSELOR = "crisis_counselor"
    MEDICAL_DOCTOR = "medical_doctor"
    NURSE = "nurse"
    PHARMACIST = "pharmacist"


class ReferralStatus(Enum):
    """Referral status enumeration."""
    PENDING = "pending"
    SENT = "sent"
    RECEIVED = "received"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ReferralPriority(Enum):
    """Referral priority enumeration."""
    ROUTINE = "routine"
    URGENT = "urgent"
    EMERGENT = "emergent"
    CRITICAL = "critical"


class CareTeamRole(Enum):
    """Care team role enumeration."""
    LEAD_THERAPIST = "lead_therapist"
    SECONDARY_THERAPIST = "secondary_therapist"
    PSYCHIATRIST = "psychiatrist"
    CASE_MANAGER = "case_manager"
    SUPERVISOR = "supervisor"
    CONSULTANT = "consultant"
    PEER_SPECIALIST = "peer_specialist"
    FAMILY_ADVOCATE = "family_advocate"


class CommunicationMethod(Enum):
    """Communication method enumeration."""
    IN_PERSON = "in_person"
    PHONE = "phone"
    VIDEO_CALL = "video_call"
    EMAIL = "email"
    SECURE_MESSAGE = "secure_message"
    FAX = "fax"
    MAIL = "mail"


class DocumentType(Enum):
    """Care coordination document type enumeration."""
    REFERRAL_FORM = "referral_form"
    TREATMENT_SUMMARY = "treatment_summary"
    PROGRESS_REPORT = "progress_report"
    DISCHARGE_SUMMARY = "discharge_summary"
    ASSESSMENT_REPORT = "assessment_report"
    MEDICATION_LIST = "medication_list"
    CRISIS_PLAN = "crisis_plan"
    CONSENT_FORM = "consent_form"
    RELEASE_OF_INFORMATION = "release_of_information"


@dataclass
class Provider:
    """Healthcare provider entity."""
    provider_id: Optional[str] = None
    
    # Basic information
    first_name: str = ""
    last_name: str = ""
    credentials: Optional[List[str]] = None
    provider_type: ProviderType = ProviderType.PRIMARY_THERAPIST
    
    # Professional details
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    license_expiry: Optional[date] = None
    npi_number: Optional[str] = None  # National Provider Identifier
    dea_number: Optional[str] = None  # Drug Enforcement Administration
    
    # Contact information
    phone: Optional[str] = None
    email: Optional[str] = None
    fax: Optional[str] = None
    
    # Practice information
    practice_name: Optional[str] = None
    practice_address: Optional[Dict[str, str]] = None
    specialty: Optional[str] = None
    subspecialties: Optional[List[str]] = None
    
    # Network and affiliations
    insurance_accepted: Optional[List[str]] = None
    hospital_affiliations: Optional[List[str]] = None
    network_status: str = "in_network"  # in_network, out_of_network, unknown
    
    # Availability
    accepting_new_patients: bool = True
    preferred_communication: Optional[List[CommunicationMethod]] = None
    languages_spoken: Optional[List[str]] = None
    
    # Quality metrics
    patient_satisfaction_score: Optional[Decimal] = None
    years_experience: Optional[int] = None
    board_certified: bool = False
    
    # System information
    is_active: bool = True
    last_verified: Optional[datetime] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Referral:
    """Referral entity."""
    referral_id: Optional[str] = None
    
    # Patient and referral details
    patient_id: str = ""
    referring_provider_id: str = ""
    receiving_provider_id: Optional[str] = None
    
    # Referral information
    referral_reason: str = ""
    clinical_summary: Optional[str] = None
    presenting_concerns: Optional[List[str]] = None
    diagnosis_codes: Optional[List[str]] = None
    
    # Urgency and timing
    priority: ReferralPriority = ReferralPriority.ROUTINE
    requested_appointment_date: Optional[date] = None
    referral_expires: Optional[date] = None
    
    # Status tracking
    status: ReferralStatus = ReferralStatus.PENDING
    status_updated_at: Optional[datetime] = None
    status_notes: Optional[str] = None
    
    # Communication
    patient_consent_obtained: bool = False
    release_of_information_signed: bool = False
    communication_method: Optional[CommunicationMethod] = None
    
    # Insurance and authorization
    insurance_authorization_required: bool = False
    authorization_number: Optional[str] = None
    authorization_expires: Optional[date] = None
    
    # Follow-up
    follow_up_required: bool = False
    follow_up_date: Optional[date] = None
    outcome_received: bool = False
    outcome_summary: Optional[str] = None
    
    # Attachments
    attached_documents: Optional[List[str]] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CareTeam:
    """Care team entity."""
    team_id: Optional[str] = None
    patient_id: str = ""
    
    # Team information
    team_name: Optional[str] = None
    primary_provider_id: str = ""
    care_coordinator_id: Optional[str] = None
    
    # Team composition
    team_members: Optional[List[Dict[str, Any]]] = None  # provider_id, role, start_date, end_date
    
    # Team dynamics
    meeting_frequency: Optional[str] = None  # weekly, biweekly, monthly, as_needed
    next_meeting_date: Optional[datetime] = None
    communication_plan: Optional[str] = None
    
    # Patient goals and treatment
    shared_goals: Optional[List[str]] = None
    treatment_approach: Optional[str] = None
    crisis_protocol: Optional[str] = None
    
    # Status
    is_active: bool = True
    team_formed_date: Optional[date] = None
    team_disbanded_date: Optional[date] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CareCoordination:
    """Care coordination activity entity."""
    coordination_id: Optional[str] = None
    patient_id: str = ""
    coordinator_id: str = ""
    
    # Activity details
    activity_type: str = ""  # assessment, planning, implementation, monitoring, evaluation
    activity_description: str = ""
    
    # Participants
    participants: Optional[List[str]] = None  # provider IDs
    communication_method: Optional[CommunicationMethod] = None
    
    # Scheduling
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    
    # Outcomes and follow-up
    outcomes: Optional[str] = None
    action_items: Optional[List[Dict[str, Any]]] = None
    follow_up_required: bool = False
    follow_up_date: Optional[date] = None
    
    # Documentation
    notes: Optional[str] = None
    attached_documents: Optional[List[str]] = None
    
    # Quality and compliance
    billable: bool = False
    billing_code: Optional[str] = None
    compliance_checked: bool = False
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CommunicationLog:
    """Communication log entity."""
    communication_id: Optional[str] = None
    
    # Communication parties
    from_provider_id: str = ""
    to_provider_id: str = ""
    patient_id: Optional[str] = None
    
    # Communication details
    subject: Optional[str] = None
    message: str = ""
    communication_method: CommunicationMethod = CommunicationMethod.SECURE_MESSAGE
    
    # Priority and urgency
    priority: str = "normal"  # low, normal, high, urgent
    requires_response: bool = False
    response_by_date: Optional[datetime] = None
    
    # Status tracking
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    
    # Security and compliance
    encrypted: bool = True
    hipaa_compliant: bool = True
    patient_consent_verified: bool = True
    
    # Attachments and references
    attached_documents: Optional[List[str]] = None
    related_referral_id: Optional[str] = None
    related_appointment_id: Optional[str] = None
    
    created_at: Optional[datetime] = None


class ProviderRepository(BaseRepository[Provider, str]):
    """Repository for provider management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "providers", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> Provider:
        """Convert database row to Provider entity."""
        return Provider(
            provider_id=row.get('provider_id'),
            first_name=row.get('first_name', ''),
            last_name=row.get('last_name', ''),
            credentials=row.get('credentials', []),
            provider_type=ProviderType(row['provider_type']) if row.get('provider_type') else ProviderType.PRIMARY_THERAPIST,
            license_number=row.get('license_number'),
            license_state=row.get('license_state'),
            license_expiry=row.get('license_expiry'),
            npi_number=row.get('npi_number'),
            dea_number=row.get('dea_number'),
            phone=row.get('phone'),
            email=row.get('email'),
            fax=row.get('fax'),
            practice_name=row.get('practice_name'),
            practice_address=row.get('practice_address'),
            specialty=row.get('specialty'),
            subspecialties=row.get('subspecialties', []),
            insurance_accepted=row.get('insurance_accepted', []),
            hospital_affiliations=row.get('hospital_affiliations', []),
            network_status=row.get('network_status', 'in_network'),
            accepting_new_patients=row.get('accepting_new_patients', True),
            preferred_communication=[CommunicationMethod(m) for m in row.get('preferred_communication', [])],
            languages_spoken=row.get('languages_spoken', []),
            patient_satisfaction_score=Decimal(str(row['patient_satisfaction_score'])) if row.get('patient_satisfaction_score') else None,
            years_experience=row.get('years_experience'),
            board_certified=row.get('board_certified', False),
            is_active=row.get('is_active', True),
            last_verified=row.get('last_verified'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: Provider) -> Dict[str, Any]:
        """Convert Provider entity to dictionary."""
        return {
            'provider_id': entity.provider_id,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'credentials': entity.credentials,
            'provider_type': entity.provider_type.value,
            'license_number': entity.license_number,
            'license_state': entity.license_state,
            'license_expiry': entity.license_expiry,
            'npi_number': entity.npi_number,
            'dea_number': entity.dea_number,
            'phone': entity.phone,
            'email': entity.email,
            'fax': entity.fax,
            'practice_name': entity.practice_name,
            'practice_address': entity.practice_address,
            'specialty': entity.specialty,
            'subspecialties': entity.subspecialties,
            'insurance_accepted': entity.insurance_accepted,
            'hospital_affiliations': entity.hospital_affiliations,
            'network_status': entity.network_status,
            'accepting_new_patients': entity.accepting_new_patients,
            'preferred_communication': [m.value for m in entity.preferred_communication] if entity.preferred_communication else [],
            'languages_spoken': entity.languages_spoken,
            'patient_satisfaction_score': entity.patient_satisfaction_score,
            'years_experience': entity.years_experience,
            'board_certified': entity.board_certified,
            'is_active': entity.is_active,
            'last_verified': entity.last_verified,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: Provider, is_update: bool = False) -> None:
        """Validate Provider entity."""
        if not entity.first_name:
            raise ValidationError("First name is required")
        
        if not entity.last_name:
            raise ValidationError("Last name is required")
        
        if entity.license_expiry and entity.license_expiry < date.today():
            self.logger.warning(f"License expired for provider {entity.provider_id}")
        
        if entity.patient_satisfaction_score and (entity.patient_satisfaction_score < 0 or entity.patient_satisfaction_score > 5):
            raise ValidationError("Patient satisfaction score must be between 0 and 5")
        
        if entity.years_experience and entity.years_experience < 0:
            raise ValidationError("Years of experience cannot be negative")
        
        if not entity.provider_id and not is_update:
            import uuid
            entity.provider_id = str(uuid.uuid4())
    
    def find_providers_by_specialty(self, specialty: str, accepting_patients: bool = True) -> List[Provider]:
        """Find providers by specialty."""
        filters = {
            'specialty': specialty,
            'is_active': True
        }
        
        if accepting_patients:
            filters['accepting_new_patients'] = True
        
        options = QueryOptions(
            filters=filters,
            order_by=['last_name', 'first_name']
        )
        
        result = self.list_all(options)
        return result.data
    
    def find_providers_by_type(self, provider_type: ProviderType, 
                              network_status: str = "in_network") -> List[Provider]:
        """Find providers by type."""
        options = QueryOptions(
            filters={
                'provider_type': provider_type.value,
                'network_status': network_status,
                'is_active': True
            },
            order_by=['last_name', 'first_name']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_expired_licenses(self, days_ahead: int = 30) -> List[Provider]:
        """Get providers with licenses expiring soon."""
        cutoff_date = date.today() + timedelta(days=days_ahead)
        
        options = QueryOptions(
            filters={
                'license_expiry__lte': cutoff_date,
                'is_active': True
            },
            order_by=['license_expiry']
        )
        
        result = self.list_all(options)
        return result.data


class ReferralRepository(BaseRepository[Referral, str]):
    """Repository for referral management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "referrals", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> Referral:
        """Convert database row to Referral entity."""
        return Referral(
            referral_id=row.get('referral_id'),
            patient_id=row.get('patient_id', ''),
            referring_provider_id=row.get('referring_provider_id', ''),
            receiving_provider_id=row.get('receiving_provider_id'),
            referral_reason=row.get('referral_reason', ''),
            clinical_summary=row.get('clinical_summary'),
            presenting_concerns=row.get('presenting_concerns', []),
            diagnosis_codes=row.get('diagnosis_codes', []),
            priority=ReferralPriority(row['priority']) if row.get('priority') else ReferralPriority.ROUTINE,
            requested_appointment_date=row.get('requested_appointment_date'),
            referral_expires=row.get('referral_expires'),
            status=ReferralStatus(row['status']) if row.get('status') else ReferralStatus.PENDING,
            status_updated_at=row.get('status_updated_at'),
            status_notes=row.get('status_notes'),
            patient_consent_obtained=row.get('patient_consent_obtained', False),
            release_of_information_signed=row.get('release_of_information_signed', False),
            communication_method=CommunicationMethod(row['communication_method']) if row.get('communication_method') else None,
            insurance_authorization_required=row.get('insurance_authorization_required', False),
            authorization_number=row.get('authorization_number'),
            authorization_expires=row.get('authorization_expires'),
            follow_up_required=row.get('follow_up_required', False),
            follow_up_date=row.get('follow_up_date'),
            outcome_received=row.get('outcome_received', False),
            outcome_summary=row.get('outcome_summary'),
            attached_documents=row.get('attached_documents', []),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: Referral) -> Dict[str, Any]:
        """Convert Referral entity to dictionary."""
        return {
            'referral_id': entity.referral_id,
            'patient_id': entity.patient_id,
            'referring_provider_id': entity.referring_provider_id,
            'receiving_provider_id': entity.receiving_provider_id,
            'referral_reason': entity.referral_reason,
            'clinical_summary': entity.clinical_summary,
            'presenting_concerns': entity.presenting_concerns,
            'diagnosis_codes': entity.diagnosis_codes,
            'priority': entity.priority.value,
            'requested_appointment_date': entity.requested_appointment_date,
            'referral_expires': entity.referral_expires,
            'status': entity.status.value,
            'status_updated_at': entity.status_updated_at,
            'status_notes': entity.status_notes,
            'patient_consent_obtained': entity.patient_consent_obtained,
            'release_of_information_signed': entity.release_of_information_signed,
            'communication_method': entity.communication_method.value if entity.communication_method else None,
            'insurance_authorization_required': entity.insurance_authorization_required,
            'authorization_number': entity.authorization_number,
            'authorization_expires': entity.authorization_expires,
            'follow_up_required': entity.follow_up_required,
            'follow_up_date': entity.follow_up_date,
            'outcome_received': entity.outcome_received,
            'outcome_summary': entity.outcome_summary,
            'attached_documents': entity.attached_documents,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: Referral, is_update: bool = False) -> None:
        """Validate Referral entity."""
        if not entity.patient_id:
            raise ValidationError("Patient ID is required")
        
        if not entity.referring_provider_id:
            raise ValidationError("Referring provider ID is required")
        
        if not entity.referral_reason:
            raise ValidationError("Referral reason is required")
        
        if entity.referral_expires and entity.referral_expires < date.today():
            self.logger.warning(f"Referral {entity.referral_id} has expired")
        
        if entity.authorization_expires and entity.authorization_expires < date.today():
            self.logger.warning(f"Authorization for referral {entity.referral_id} has expired")
        
        if not entity.referral_id and not is_update:
            import uuid
            entity.referral_id = str(uuid.uuid4())
    
    def create_referral(self, patient_id: str, referring_provider_id: str,
                       referral_reason: str, priority: ReferralPriority = ReferralPriority.ROUTINE,
                       receiving_provider_id: str = None) -> Referral:
        """Create a new referral."""
        referral = Referral(
            patient_id=patient_id,
            referring_provider_id=referring_provider_id,
            receiving_provider_id=receiving_provider_id,
            referral_reason=referral_reason,
            priority=priority
        )
        
        created_referral = self.create(referral)
        
        self.logger.info(f"Created referral {created_referral.referral_id} for patient {patient_id}")
        return created_referral
    
    def get_patient_referrals(self, patient_id: str, active_only: bool = False) -> List[Referral]:
        """Get referrals for a patient."""
        filters = {'patient_id': patient_id}
        
        if active_only:
            active_statuses = [ReferralStatus.PENDING.value, ReferralStatus.SENT.value, 
                             ReferralStatus.RECEIVED.value, ReferralStatus.ACCEPTED.value]
            filters['status__in'] = active_statuses
        
        options = QueryOptions(
            filters=filters,
            order_by=['-created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_provider_referrals(self, provider_id: str, 
                              direction: str = "both") -> List[Referral]:
        """Get referrals for a provider (sent, received, or both)."""
        filters = {}
        
        if direction == "sent":
            filters['referring_provider_id'] = provider_id
        elif direction == "received":
            filters['receiving_provider_id'] = provider_id
        else:  # both
            # This would need a custom query for OR condition
            pass
        
        options = QueryOptions(
            filters=filters,
            order_by=['-created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def update_referral_status(self, referral_id: str, status: ReferralStatus,
                              notes: str = None) -> bool:
        """Update referral status."""
        try:
            referral = self.get_by_id(referral_id)
            if not referral:
                return False
            
            referral.status = status
            referral.status_updated_at = datetime.now()
            if notes:
                referral.status_notes = notes
            
            self.update(referral)
            
            self.logger.info(f"Updated referral {referral_id} status to {status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update referral status: {e}")
            return False
    
    def get_pending_referrals(self, provider_id: str = None) -> List[Referral]:
        """Get pending referrals."""
        filters = {'status': ReferralStatus.PENDING.value}
        
        if provider_id:
            filters['receiving_provider_id'] = provider_id
        
        options = QueryOptions(
            filters=filters,
            order_by=['priority', 'created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_expiring_referrals(self, days_ahead: int = 7) -> List[Referral]:
        """Get referrals expiring soon."""
        cutoff_date = date.today() + timedelta(days=days_ahead)
        
        options = QueryOptions(
            filters={
                'referral_expires__lte': cutoff_date,
                'status__in': [ReferralStatus.PENDING.value, ReferralStatus.SENT.value, 
                             ReferralStatus.RECEIVED.value]
            },
            order_by=['referral_expires']
        )
        
        result = self.list_all(options)
        return result.data


class CareTeamRepository(BaseRepository[CareTeam, str]):
    """Repository for care team management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "care_teams", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> CareTeam:
        """Convert database row to CareTeam entity."""
        return CareTeam(
            team_id=row.get('team_id'),
            patient_id=row.get('patient_id', ''),
            team_name=row.get('team_name'),
            primary_provider_id=row.get('primary_provider_id', ''),
            care_coordinator_id=row.get('care_coordinator_id'),
            team_members=row.get('team_members', []),
            meeting_frequency=row.get('meeting_frequency'),
            next_meeting_date=row.get('next_meeting_date'),
            communication_plan=row.get('communication_plan'),
            shared_goals=row.get('shared_goals', []),
            treatment_approach=row.get('treatment_approach'),
            crisis_protocol=row.get('crisis_protocol'),
            is_active=row.get('is_active', True),
            team_formed_date=row.get('team_formed_date'),
            team_disbanded_date=row.get('team_disbanded_date'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: CareTeam) -> Dict[str, Any]:
        """Convert CareTeam entity to dictionary."""
        return {
            'team_id': entity.team_id,
            'patient_id': entity.patient_id,
            'team_name': entity.team_name,
            'primary_provider_id': entity.primary_provider_id,
            'care_coordinator_id': entity.care_coordinator_id,
            'team_members': entity.team_members,
            'meeting_frequency': entity.meeting_frequency,
            'next_meeting_date': entity.next_meeting_date,
            'communication_plan': entity.communication_plan,
            'shared_goals': entity.shared_goals,
            'treatment_approach': entity.treatment_approach,
            'crisis_protocol': entity.crisis_protocol,
            'is_active': entity.is_active,
            'team_formed_date': entity.team_formed_date,
            'team_disbanded_date': entity.team_disbanded_date,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: CareTeam, is_update: bool = False) -> None:
        """Validate CareTeam entity."""
        if not entity.patient_id:
            raise ValidationError("Patient ID is required")
        
        if not entity.primary_provider_id:
            raise ValidationError("Primary provider ID is required")
        
        if not entity.team_id and not is_update:
            import uuid
            entity.team_id = str(uuid.uuid4())
        
        if not entity.team_formed_date:
            entity.team_formed_date = date.today()
    
    def get_patient_care_team(self, patient_id: str) -> Optional[CareTeam]:
        """Get active care team for a patient."""
        return self.find_one_by(patient_id=patient_id, is_active=True)
    
    def add_team_member(self, team_id: str, provider_id: str, 
                       role: CareTeamRole, start_date: date = None) -> bool:
        """Add a member to the care team."""
        try:
            team = self.get_by_id(team_id)
            if not team:
                return False
            
            if not team.team_members:
                team.team_members = []
            
            # Check if provider is already on the team
            for member in team.team_members:
                if member.get('provider_id') == provider_id and not member.get('end_date'):
                    self.logger.warning(f"Provider {provider_id} already on team {team_id}")
                    return False
            
            new_member = {
                'provider_id': provider_id,
                'role': role.value,
                'start_date': start_date or date.today(),
                'end_date': None
            }
            
            team.team_members.append(new_member)
            self.update(team)
            
            self.logger.info(f"Added provider {provider_id} to care team {team_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add team member: {e}")
            return False
    
    def remove_team_member(self, team_id: str, provider_id: str, 
                          end_date: date = None) -> bool:
        """Remove a member from the care team."""
        try:
            team = self.get_by_id(team_id)
            if not team or not team.team_members:
                return False
            
            for member in team.team_members:
                if member.get('provider_id') == provider_id and not member.get('end_date'):
                    member['end_date'] = end_date or date.today()
                    break
            else:
                return False  # Member not found
            
            self.update(team)
            
            self.logger.info(f"Removed provider {provider_id} from care team {team_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove team member: {e}")
            return False
    
    def get_provider_teams(self, provider_id: str) -> List[CareTeam]:
        """Get care teams that include a specific provider."""
        # This would need a custom query to search within team_members JSON
        query = f"""
            SELECT * FROM {self.table_name}
            WHERE is_active = true
            AND (primary_provider_id = %(provider_id)s
                 OR care_coordinator_id = %(provider_id)s
                 OR team_members::text LIKE %(provider_search)s)
            ORDER BY team_formed_date DESC
        """
        
        try:
            result = self.db.execute_query(query, {
                'provider_id': provider_id,
                'provider_search': f'%{provider_id}%'
            })
            return [self._to_entity(row) for row in result] if result else []
            
        except Exception as e:
            self.logger.error(f"Failed to get provider teams: {e}")
            return []
