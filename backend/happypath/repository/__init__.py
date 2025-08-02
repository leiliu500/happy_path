"""
Happy Path Repository Package

This package provides the data access layer for the Happy Path mental health wellness platform 
using the repository pattern. It includes base repository classes, common database operations, 
and specialized repositories for all clinical and patient engagement data entities.

The repository pattern provides:
- Clean separation of data access logic from business logic
- Consistent interface for database operations
- Easy testing with mockable interfaces
- Centralized query management
- Transaction handling
- Data validation and transformation
"""

# Base repository classes
from .base_repository import (
    BaseRepository,
    AsyncBaseRepository,
    QueryOptions,
    QueryResult,
    RepositoryError,
    ValidationError,
    NotFoundError,
    DuplicateError,
    build_where_clause,
    build_order_clause
)

# User management repositories
from .user_repository import (
    User,
    UserProfile,
    UserRepository,
    AsyncUserRepository
)

from .audit_repository import (
    AuditEntry,
    AuditQuery,
    AuditSummary,
    AuditAction,
    AuditLevel,
    AuditRepository,
    AsyncAuditRepository
)

from .subscription_repository import (
    SubscriptionPlan,
    Subscription,
    Payment,
    UsageRecord,
    SubscriptionAnalytics,
    SubscriptionStatus,
    BillingCycle,
    PaymentStatus,
    SubscriptionPlanRepository,
    SubscriptionRepository,
    PaymentRepository
)

from .session_repository import (
    UserSession,
    SessionAnalytics,
    SessionStatus,
    SessionRepository,
    AsyncSessionRepository
)

# Clinical and mental health repositories
from .clinical_repository import (
    TherapeuticRelationship,
    TreatmentPlan,
    TherapySession,
    TherapeuticRelationshipRepository,
    TreatmentPlanRepository,
    TherapySessionRepository
)

from .mood_repository import (
    MoodEntry,
    MoodPattern,
    MoodGoal,
    MoodEntryRepository,
    MoodPatternRepository,
    MoodGoalRepository
)

from .journaling_repository import (
    JournalEntry,
    JournalPrompt,
    UserPromptHistory,
    JournalEntryRepository,
    JournalPromptRepository,
    UserPromptHistoryRepository
)

from .crisis_repository import (
    CrisisDetection,
    CrisisEscalation,
    SafetyPlan,
    CrisisDetectionRepository,
    CrisisEscalationRepository,
    SafetyPlanRepository
)

from .appointment_repository import (
    ProviderCalendar,
    Appointment,
    AppointmentReminder,
    ProviderCalendarRepository,
    AppointmentRepository,
    AppointmentReminderRepository
)

from .medication_repository import (
    Medication,
    MedicationDose,
    MedicationAdherence,
    MedicationRepository,
    MedicationDoseRepository,
    MedicationAdherenceRepository
)

from .conversational_repository import (
    Conversation,
    ChatMessage,
    ConversationIntent,
    ConversationAnalytics,
    ConversationRepository,
    ChatMessageRepository,
    ConversationIntentRepository
)

from .system_administration_repository import (
    UserAccount,
    AuditLog,
    SystemConfiguration,
    SystemAlert,
    UserAccountRepository,
    AuditLogRepository,
    SystemConfigurationRepository
)

from .care_coordination_repository import (
    Provider,
    Referral,
    CareTeam,
    CareCoordination,
    CommunicationLog,
    ProviderRepository,
    ReferralRepository,
    CareTeamRepository
)

# Repository factory functions for core repositories
def create_user_repository(db_manager, logger=None):
    """Create a UserRepository instance."""
    return UserRepository(db_manager, logger)

def create_audit_repository(db_manager, logger=None):
    """Create an AuditRepository instance."""
    return AuditRepository(db_manager, logger)

def create_subscription_repository(db_manager, logger=None):
    """Create a SubscriptionRepository instance."""
    return SubscriptionRepository(db_manager, logger)

def create_session_repository(db_manager, logger=None):
    """Create a SessionRepository instance."""
    return SessionRepository(db_manager, logger)

def create_subscription_plan_repository(db_manager, logger=None):
    """Create a SubscriptionPlanRepository instance."""
    return SubscriptionPlanRepository(db_manager, logger)

def create_payment_repository(db_manager, logger=None):
    """Create a PaymentRepository instance."""
    return PaymentRepository(db_manager, logger)

# Factory functions for clinical repositories
def create_therapeutic_relationship_repository(db_manager, logger=None):
    """Create a TherapeuticRelationshipRepository instance."""
    return TherapeuticRelationshipRepository(db_manager, logger)

def create_treatment_plan_repository(db_manager, logger=None):
    """Create a TreatmentPlanRepository instance."""
    return TreatmentPlanRepository(db_manager, logger)

def create_therapy_session_repository(db_manager, logger=None):
    """Create a TherapySessionRepository instance."""
    return TherapySessionRepository(db_manager, logger)

def create_mood_entry_repository(db_manager, logger=None):
    """Create a MoodEntryRepository instance."""
    return MoodEntryRepository(db_manager, logger)

def create_mood_pattern_repository(db_manager, logger=None):
    """Create a MoodPatternRepository instance."""
    return MoodPatternRepository(db_manager, logger)

def create_mood_goal_repository(db_manager, logger=None):
    """Create a MoodGoalRepository instance."""
    return MoodGoalRepository(db_manager, logger)

def create_journal_entry_repository(db_manager, logger=None):
    """Create a JournalEntryRepository instance."""
    return JournalEntryRepository(db_manager, logger)

def create_journal_prompt_repository(db_manager, logger=None):
    """Create a JournalPromptRepository instance."""
    return JournalPromptRepository(db_manager, logger)

def create_crisis_detection_repository(db_manager, logger=None):
    """Create a CrisisDetectionRepository instance."""
    return CrisisDetectionRepository(db_manager, logger)

def create_crisis_escalation_repository(db_manager, logger=None):
    """Create a CrisisEscalationRepository instance."""
    return CrisisEscalationRepository(db_manager, logger)

def create_safety_plan_repository(db_manager, logger=None):
    """Create a SafetyPlanRepository instance."""
    return SafetyPlanRepository(db_manager, logger)

def create_appointment_repository(db_manager, logger=None):
    """Create an AppointmentRepository instance."""
    return AppointmentRepository(db_manager, logger)

def create_provider_calendar_repository(db_manager, logger=None):
    """Create a ProviderCalendarRepository instance."""
    return ProviderCalendarRepository(db_manager, logger)

def create_medication_repository(db_manager, logger=None):
    """Create a MedicationRepository instance."""
    return MedicationRepository(db_manager, logger)

def create_medication_dose_repository(db_manager, logger=None):
    """Create a MedicationDoseRepository instance."""
    return MedicationDoseRepository(db_manager, logger)

def create_medication_adherence_repository(db_manager, logger=None):
    """Create a MedicationAdherenceRepository instance."""
    return MedicationAdherenceRepository(db_manager, logger)

def create_conversation_repository(db_manager, logger=None):
    """Create a ConversationRepository instance."""
    return ConversationRepository(db_manager, logger)

def create_chat_message_repository(db_manager, logger=None):
    """Create a ChatMessageRepository instance."""
    return ChatMessageRepository(db_manager, logger)

def create_user_account_repository(db_manager, logger=None):
    """Create a UserAccountRepository instance."""
    return UserAccountRepository(db_manager, logger)

def create_audit_log_repository(db_manager, logger=None):
    """Create an AuditLogRepository instance."""
    return AuditLogRepository(db_manager, logger)

def create_system_configuration_repository(db_manager, logger=None):
    """Create a SystemConfigurationRepository instance."""
    return SystemConfigurationRepository(db_manager, logger)

def create_provider_repository(db_manager, logger=None):
    """Create a ProviderRepository instance."""
    return ProviderRepository(db_manager, logger)

def create_referral_repository(db_manager, logger=None):
    """Create a ReferralRepository instance."""
    return ReferralRepository(db_manager, logger)

def create_care_team_repository(db_manager, logger=None):
    """Create a CareTeamRepository instance."""
    return CareTeamRepository(db_manager, logger)

# Async repository factory functions
def create_async_user_repository(db_manager, logger=None):
    """Create an AsyncUserRepository instance."""
    return AsyncUserRepository(db_manager, logger)

def create_async_audit_repository(db_manager, logger=None):
    """Create an AsyncAuditRepository instance."""
    return AsyncAuditRepository(db_manager, logger)

def create_async_session_repository(db_manager, logger=None):
    """Create an AsyncSessionRepository instance."""
    return AsyncSessionRepository(db_manager, logger)

__all__ = [
    # Base classes
    'BaseRepository',
    'AsyncBaseRepository',
    'QueryOptions',
    'QueryResult',
    'RepositoryError',
    'ValidationError',
    'NotFoundError',
    'DuplicateError',
    'build_where_clause',
    'build_order_clause',
    
    # User management entities and repositories
    'User',
    'UserProfile',
    'UserRepository',
    'AsyncUserRepository',
    
    # Audit entities and repositories
    'AuditEntry',
    'AuditQuery',
    'AuditSummary',
    'AuditAction',
    'AuditLevel',
    'AuditRepository',
    'AsyncAuditRepository',
    
    # Subscription entities and repositories
    'SubscriptionPlan',
    'Subscription',
    'Payment',
    'UsageRecord',
    'SubscriptionAnalytics',
    'SubscriptionStatus',
    'BillingCycle',
    'PaymentStatus',
    'SubscriptionPlanRepository',
    'SubscriptionRepository',
    'PaymentRepository',
    
    # Session entities and repositories
    'UserSession',
    'SessionAnalytics',
    'SessionStatus',
    'SessionRepository',
    'AsyncSessionRepository',
    
    # Clinical therapy entities and repositories
    'TherapeuticRelationship',
    'TreatmentPlan',
    'TherapySession',
    'TherapeuticRelationshipRepository',
    'TreatmentPlanRepository',
    'TherapySessionRepository',
    
    # Mood tracking entities and repositories
    'MoodEntry',
    'MoodPattern',
    'MoodGoal',
    'MoodEntryRepository',
    'MoodPatternRepository',
    'MoodGoalRepository',
    
    # Journaling entities and repositories
    'JournalEntry',
    'JournalPrompt',
    'UserPromptHistory',
    'JournalEntryRepository',
    'JournalPromptRepository',
    'UserPromptHistoryRepository',
    
    # Crisis management entities and repositories
    'CrisisDetection',
    'CrisisEscalation',
    'SafetyPlan',
    'CrisisDetectionRepository',
    'CrisisEscalationRepository',
    'SafetyPlanRepository',
    
    # Appointment entities and repositories
    'ProviderCalendar',
    'Appointment',
    'AppointmentReminder',
    'ProviderCalendarRepository',
    'AppointmentRepository',
    'AppointmentReminderRepository',
    
    # Medication entities and repositories
    'Medication',
    'MedicationDose',
    'MedicationAdherence',
    'MedicationRepository',
    'MedicationDoseRepository',
    'MedicationAdherenceRepository',
    
    # Conversational agent entities and repositories
    'Conversation',
    'ChatMessage',
    'ConversationIntent',
    'ConversationAnalytics',
    'ConversationRepository',
    'ChatMessageRepository',
    'ConversationIntentRepository',
    
    # System administration entities and repositories
    'UserAccount',
    'AuditLog',
    'SystemConfiguration',
    'SystemAlert',
    'UserAccountRepository',
    'AuditLogRepository',
    'SystemConfigurationRepository',
    
    # Care coordination entities and repositories
    'Provider',
    'Referral',
    'CareTeam',
    'CareCoordination',
    'CommunicationLog',
    'ProviderRepository',
    'ReferralRepository',
    'CareTeamRepository',
    
    # Core repository factory functions
    'create_user_repository',
    'create_audit_repository',
    'create_subscription_repository',
    'create_session_repository',
    'create_subscription_plan_repository',
    'create_payment_repository',
    
    # Clinical repository factory functions
    'create_therapeutic_relationship_repository',
    'create_treatment_plan_repository',
    'create_therapy_session_repository',
    'create_mood_entry_repository',
    'create_mood_pattern_repository',
    'create_mood_goal_repository',
    'create_journal_entry_repository',
    'create_journal_prompt_repository',
    'create_crisis_detection_repository',
    'create_crisis_escalation_repository',
    'create_safety_plan_repository',
    'create_appointment_repository',
    'create_provider_calendar_repository',
    'create_medication_repository',
    'create_medication_dose_repository',
    'create_medication_adherence_repository',
    'create_conversation_repository',
    'create_chat_message_repository',
    'create_user_account_repository',
    'create_audit_log_repository',
    'create_system_configuration_repository',
    'create_provider_repository',
    'create_referral_repository',
    'create_care_team_repository',
    
    # Async repository factory functions
    'create_async_user_repository',
    'create_async_audit_repository',
    'create_async_session_repository',
]

__version__ = '1.0.0'
