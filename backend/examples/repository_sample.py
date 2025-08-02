"""
Mental Health Wellness Platform Repository Pattern Sample Code

This file demonstrates how to use the comprehensive repository pattern implementation
for mental health platform database operations across clinical, patient engagement,
and administrative entities.
"""

import asyncio
from datetime import datetime, timedelta, date, time
from decimal import Decimal
from typing import List, Optional
import logging

# Import core infrastructure
from backend.happypath.core import get_db_manager, get_logger

# Import repository classes and entities
from backend.happypath.repository import (
    # Core entities
    User, UserProfile, AuditEntry, Subscription, SubscriptionPlan, UserSession,
    
    # Clinical entities
    TherapeuticRelationship, TreatmentPlan, TherapySession,
    MoodEntry, MoodPattern, MoodGoal,
    JournalEntry, JournalPrompt, UserPromptHistory,
    CrisisDetection, CrisisEscalation, SafetyPlan,
    
    # Operational entities
    ProviderCalendar, Appointment, AppointmentReminder,
    Medication, MedicationDose, MedicationAdherence,
    
    # Communication entities
    Conversation, ChatMessage, ConversationIntent,
    
    # Administration entities
    UserAccount, AuditLog, SystemConfiguration,
    Provider, Referral, CareTeam,
    
    # Core repositories
    UserRepository, AuditRepository, SubscriptionRepository, 
    SubscriptionPlanRepository, SessionRepository,
    
    # Clinical repositories
    TherapeuticRelationshipRepository, TreatmentPlanRepository, TherapySessionRepository,
    MoodEntryRepository, MoodPatternRepository, MoodGoalRepository,
    JournalEntryRepository, JournalPromptRepository,
    CrisisDetectionRepository, SafetyPlanRepository,
    
    # Operational repositories
    AppointmentRepository, ProviderCalendarRepository,
    MedicationRepository, MedicationAdherenceRepository,
    
    # Communication repositories
    ConversationRepository, ChatMessageRepository,
    
    # Administration repositories
    UserAccountRepository, AuditLogRepository, SystemConfigurationRepository,
    ProviderRepository, ReferralRepository, CareTeamRepository,
    
    # Enums
    AuditAction, AuditLevel, SubscriptionStatus, BillingCycle,
    TherapyModality, TreatmentPhase, ClinicalSeverity, TreatmentOutcome,
    MoodScale, MoodType, CBTTechnique, JournalType,
    AppointmentType, AppointmentStatus, AppointmentModality, ReferralStatus, 
    ReferralPriority, ProviderType, CareTeamRole, CrisisSeverity,
    ConversationType, MessageType, MessageSender, UserRole, UserStatus,
    
    # Utilities
    QueryOptions,
    
    # Factory functions
    create_user_repository, create_audit_repository, 
    create_subscription_repository, create_session_repository,
    create_therapeutic_relationship_repository, create_treatment_plan_repository,
    create_mood_entry_repository, create_journal_entry_repository,
    create_appointment_repository, create_medication_repository,
    create_conversation_repository, create_provider_repository
)


def setup_repositories():
    """Set up repository instances with database connection."""
    # Get database manager and logger
    db_manager = get_db_manager()
    logger = get_logger('repository_sample')
    
    # Core repositories
    user_repo = create_user_repository(db_manager, logger)
    audit_repo = create_audit_repository(db_manager, logger)
    subscription_repo = create_subscription_repository(db_manager, logger)
    session_repo = create_session_repository(db_manager, logger)
    
    # Clinical repositories
    relationship_repo = create_therapeutic_relationship_repository(db_manager, logger)
    treatment_repo = create_treatment_plan_repository(db_manager, logger)
    mood_repo = create_mood_entry_repository(db_manager, logger)
    journal_repo = create_journal_entry_repository(db_manager, logger)
    
    # Operational repositories
    appointment_repo = create_appointment_repository(db_manager, logger)
    medication_repo = create_medication_repository(db_manager, logger)
    
    # Communication repositories
    conversation_repo = create_conversation_repository(db_manager, logger)
    
    # Administration repositories
    provider_repo = create_provider_repository(db_manager, logger)
    
    return {
        'user': user_repo,
        'audit': audit_repo,
        'subscription': subscription_repo,
        'session': session_repo,
        'relationship': relationship_repo,
        'treatment': treatment_repo,
        'mood': mood_repo,
        'journal': journal_repo,
        'appointment': appointment_repo,
        'medication': medication_repo,
        'conversation': conversation_repo,
        'provider': provider_repo
    }


def clinical_workflow_example():
    """Demonstrate a complete clinical workflow."""
    repos = setup_repositories()
    logger = get_logger('clinical_workflow')
    
    try:
        # 1. Create a therapeutic relationship
        logger.info("Creating therapeutic relationship...")
        relationship = TherapeuticRelationship(
            patient_id="patient_123",
            therapist_id="therapist_456",
            therapy_modality=TherapyModality.CBT,
            relationship_status="active",
            start_date=date.today()
        )
        relationship = repos['relationship'].create(relationship)
        logger.info(f"Created relationship: {relationship.relationship_id}")
        
        # 2. Create treatment plan
        logger.info("Creating treatment plan...")
        treatment_plan = TreatmentPlan(
            patient_id="patient_123",
            therapist_id="therapist_456",
            relationship_id=relationship.relationship_id,
            plan_name="Depression and Anxiety Treatment",
            primary_diagnosis="Major Depressive Disorder",
            treatment_goals=["Reduce depression symptoms", "Improve coping skills"],
            interventions=["CBT techniques", "Mood tracking", "Journaling"],
            target_outcomes=["PHQ-9 score < 10", "Improved daily functioning"],
            estimated_duration_weeks=12,
            phase=TreatmentPhase.ACTIVE
        )
        treatment_plan = repos['treatment'].create(treatment_plan)
        logger.info(f"Created treatment plan: {treatment_plan.plan_id}")
        
        # 3. Log mood entry
        logger.info("Creating mood entry...")
        mood_entry = MoodEntry(
            user_id="patient_123",
            mood_scale=MoodScale.ONE_TO_TEN,
            mood_rating=6,
            mood_type=MoodType.GENERAL,
            contributing_factors=["Good sleep", "Exercise"],
            notes="Feeling better today after morning walk",
            location="Home",
            privacy_level="private"
        )
        mood_entry = repos['mood'].create(mood_entry)
        logger.info(f"Created mood entry: {mood_entry.entry_id}")
        
        # 4. Create journal entry
        logger.info("Creating journal entry...")
        journal_entry = JournalEntry(
            user_id="patient_123",
            title="Daily Reflection",
            content="Today I practiced the breathing exercises we discussed. I noticed my anxiety decreased significantly.",
            journal_type=JournalType.THERAPEUTIC,
            cbt_technique=CBTTechnique.THOUGHT_RECORD,
            mood_before=4,
            mood_after=7,
            tags=["breathing", "anxiety", "progress"],
            privacy_level="therapist_shared"
        )
        journal_entry = repos['journal'].create(journal_entry)
        logger.info(f"Created journal entry: {journal_entry.entry_id}")
        
        # 5. Schedule appointment
        logger.info("Scheduling appointment...")
        appointment = Appointment(
            provider_id="therapist_456",
            patient_id="patient_123",
            appointment_type=AppointmentType.THERAPY_SESSION,
            scheduled_start=datetime.now() + timedelta(days=7),
            duration_minutes=50,
            modality=AppointmentModality.TELEHEALTH,
            agenda=["Review mood tracking", "Practice CBT techniques", "Discuss progress"]
        )
        appointment = repos['appointment'].create(appointment)
        logger.info(f"Scheduled appointment: {appointment.appointment_id}")
        
        # 6. Track medication if applicable
        logger.info("Adding medication...")
        medication = Medication(
            patient_id="patient_123",
            prescribing_provider_id="psychiatrist_789",
            medication_name="Sertraline",
            generic_name="Sertraline",
            strength="50mg",
            dosage_form="tablet",
            prescribed_dosage="50mg once daily",
            prescribed_frequency="daily",
            start_date=date.today(),
            indication="Major Depressive Disorder"
        )
        medication = repos['medication'].create(medication)
        logger.info(f"Added medication: {medication.medication_id}")
        
        logger.info("Clinical workflow completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Clinical workflow failed: {e}")
        return False


def patient_engagement_example():
    """Demonstrate patient engagement features."""
    repos = setup_repositories()
    logger = get_logger('patient_engagement')
    
    try:
        # 1. Start conversation with AI chatbot
        logger.info("Starting AI conversation...")
        conversation = repos['conversation'].start_conversation(
            user_id="patient_123",
            conversation_type=ConversationType.MOOD_CHECK_IN,
            title="Daily Mood Check-in"
        )
        logger.info(f"Started conversation: {conversation.conversation_id}")
        
        # 2. Add chat messages
        logger.info("Adding chat messages...")
        user_message = repos['conversation'].get_chat_message_repo().add_message(
            conversation_id=conversation.conversation_id,
            user_id="patient_123",
            content="I'm feeling anxious today",
            sender=MessageSender.USER
        )
        
        bot_response = repos['conversation'].get_chat_message_repo().add_message(
            conversation_id=conversation.conversation_id,
            user_id="patient_123",
            content="I understand you're feeling anxious. Can you tell me what might be contributing to this feeling?",
            sender=MessageSender.AGENT
        )
        
        # 3. Create mood pattern analysis
        logger.info("Analyzing mood patterns...")
        mood_pattern = MoodPattern(
            user_id="patient_123",
            pattern_name="Weekly Mood Trend",
            pattern_type="weekly",
            average_mood=6.5,
            mood_variance=1.2,
            trend_direction="improving",
            pattern_strength=0.75,
            contributing_factors=["Exercise", "Sleep quality", "Social activities"],
            recommendations=["Continue exercise routine", "Monitor sleep patterns"]
        )
        mood_pattern = repos['mood'].get_pattern_repo().create(mood_pattern)
        logger.info(f"Created mood pattern: {mood_pattern.pattern_id}")
        
        # 4. Set mood goals
        logger.info("Setting mood goals...")
        mood_goal = MoodGoal(
            user_id="patient_123",
            goal_type="average_mood",
            target_value=7.5,
            current_value=6.5,
            target_date=date.today() + timedelta(days=30),
            description="Achieve average mood rating of 7.5",
            strategies=["Daily meditation", "Regular exercise", "Journaling"],
            milestone_rewards=["Treat myself to a movie", "Buy a new book"]
        )
        mood_goal = repos['mood'].get_goal_repo().create(mood_goal)
        logger.info(f"Created mood goal: {mood_goal.goal_id}")
        
        logger.info("Patient engagement workflow completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Patient engagement workflow failed: {e}")
        return False


def care_coordination_example():
    """Demonstrate care coordination workflow."""
    repos = setup_repositories()
    logger = get_logger('care_coordination')
    
    try:
        # 1. Create provider
        logger.info("Creating healthcare provider...")
        provider = Provider(
            first_name="Dr. Sarah",
            last_name="Johnson",
            credentials=["MD", "Board Certified Psychiatrist"],
            provider_type=ProviderType.PSYCHIATRIST,
            license_number="MD12345",
            license_state="CA",
            specialty="Adult Psychiatry",
            phone="(555) 123-4567",
            email="dr.johnson@clinic.com",
            accepting_new_patients=True
        )
        provider = repos['provider'].create(provider)
        logger.info(f"Created provider: {provider.provider_id}")
        
        # 2. Create referral
        logger.info("Creating referral...")
        referral = repos['provider'].get_referral_repo().create_referral(
            patient_id="patient_123",
            referring_provider_id="therapist_456",
            receiving_provider_id=provider.provider_id,
            referral_reason="Psychiatric evaluation for medication management",
            priority=ReferralPriority.ROUTINE
        )
        logger.info(f"Created referral: {referral.referral_id}")
        
        # 3. Create care team
        logger.info("Creating care team...")
        care_team = CareTeam(
            patient_id="patient_123",
            team_name="Patient 123 Care Team",
            primary_provider_id="therapist_456",
            shared_goals=["Symptom reduction", "Improved functioning"],
            treatment_approach="Integrated CBT and medication management"
        )
        care_team = repos['provider'].get_care_team_repo().create(care_team)
        
        # Add team members
        repos['provider'].get_care_team_repo().add_team_member(
            team_id=care_team.team_id,
            provider_id=provider.provider_id,
            role=CareTeamRole.PSYCHIATRIST
        )
        logger.info(f"Created care team: {care_team.team_id}")
        
        logger.info("Care coordination workflow completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Care coordination workflow failed: {e}")
        return False


def crisis_management_example():
    """Demonstrate crisis detection and management."""
    repos = setup_repositories()
    logger = get_logger('crisis_management')
    
    try:
        # 1. Crisis detection in journal entry
        logger.info("Creating journal entry with crisis indicators...")
        crisis_journal = JournalEntry(
            user_id="patient_123",
            title="Difficult Day",
            content="I don't see the point anymore. Everything feels hopeless and I can't stop thinking about ending it all.",
            journal_type=JournalType.FREE_FORM,
            privacy_level="private"
        )
        
        # The repository would detect crisis keywords and flag this
        crisis_journal = repos['journal'].create(crisis_journal)
        logger.info(f"Created journal with crisis detection: {crisis_journal.entry_id}")
        
        # 2. Create crisis detection record
        logger.info("Creating crisis detection record...")
        crisis_detection = CrisisDetection(
            patient_id="patient_123",
            detection_source="journal_entry",
            source_id=crisis_journal.entry_id,
            crisis_type="suicidal_ideation",
            severity_level=CrisisSeverity.HIGH,
            risk_factors=["Hopelessness", "Suicidal ideation"],
            detected_keywords=["hopeless", "ending it all"],
            confidence_score=0.95,
            requires_immediate_attention=True
        )
        crisis_detection = repos['journal'].get_crisis_repo().create(crisis_detection)
        logger.info(f"Created crisis detection: {crisis_detection.detection_id}")
        
        # 3. Create safety plan
        logger.info("Creating safety plan...")
        safety_plan = SafetyPlan(
            patient_id="patient_123",
            created_by_provider_id="therapist_456",
            warning_signs=["Feeling hopeless", "Isolating from others", "Sleep disruption"],
            coping_strategies=["Deep breathing", "Call support person", "Go for a walk"],
            social_contacts=[
                {"name": "Best Friend", "phone": "(555) 999-8888", "relationship": "friend"},
                {"name": "Sister", "phone": "(555) 777-6666", "relationship": "family"}
            ],
            professional_contacts=[
                {"name": "Dr. Smith", "phone": "(555) 123-4567", "role": "therapist"},
                {"name": "Crisis Hotline", "phone": "988", "role": "crisis_support"}
            ],
            environmental_safety=["Remove harmful objects", "Stay with trusted person"],
            is_active=True
        )
        safety_plan = repos['journal'].get_safety_plan_repo().create(safety_plan)
        logger.info(f"Created safety plan: {safety_plan.plan_id}")
        
        logger.info("Crisis management workflow completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Crisis management workflow failed: {e}")
        return False


def medication_adherence_example():
    """Demonstrate medication adherence tracking."""
    repos = setup_repositories()
    logger = get_logger('medication_adherence')
    
    try:
        # 1. Get existing medication
        logger.info("Tracking medication adherence...")
        
        # 2. Record medication doses
        logger.info("Recording medication doses...")
        dose1 = MedicationDose(
            medication_id="med_123",
            patient_id="patient_123",
            scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
            actual_time=datetime.now().replace(hour=8, minute=15, second=0, microsecond=0),
            dose_amount="50mg",
            taken_as_prescribed=True,
            taken_status="taken",
            adherence_percentage=100.0
        )
        dose1 = repos['medication'].get_dose_repo().create(dose1)
        
        dose2 = MedicationDose(
            medication_id="med_123",
            patient_id="patient_123",
            scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) - timedelta(days=1),
            dose_amount="50mg",
            taken_as_prescribed=False,
            taken_status="missed",
            adherence_percentage=0.0,
            notes="Forgot to take medication"
        )
        dose2 = repos['medication'].get_dose_repo().create(dose2)
        
        # 3. Calculate adherence
        logger.info("Calculating medication adherence...")
        adherence = MedicationAdherence(
            medication_id="med_123",
            patient_id="patient_123",
            period_start=date.today() - timedelta(days=7),
            period_end=date.today(),
            doses_prescribed=7,
            doses_taken=6,
            adherence_percentage=85.7,
            missed_doses=1,
            late_doses=1,
            adherence_pattern="mostly_compliant",
            barriers_to_adherence=["Forgetfulness"],
            improvement_suggestions=["Set daily reminder", "Use pill organizer"]
        )
        adherence = repos['medication'].get_adherence_repo().create(adherence)
        logger.info(f"Created adherence record: {adherence.adherence_id}")
        
        logger.info("Medication adherence tracking completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Medication adherence tracking failed: {e}")
        return False


def demonstrate_query_operations():
    """Demonstrate advanced query operations."""
    repos = setup_repositories()
    logger = get_logger('query_operations')
    
    try:
        # 1. Complex filtering
        logger.info("Demonstrating complex queries...")
        
        # Get recent mood entries with specific criteria
        mood_options = QueryOptions(
            filters={
                'user_id': 'patient_123',
                'mood_rating__gte': 7,  # Mood rating >= 7
                'created_at__gte': datetime.now() - timedelta(days=30)
            },
            order_by=['-created_at'],
            limit=10
        )
        recent_good_moods = repos['mood'].list_all(mood_options)
        logger.info(f"Found {len(recent_good_moods.data)} recent good mood entries")
        
        # Get appointments by status
        appointment_options = QueryOptions(
            filters={
                'status__in': ['scheduled', 'confirmed'],
                'scheduled_start__gte': datetime.now()
            },
            order_by=['scheduled_start']
        )
        upcoming_appointments = repos['appointment'].list_all(appointment_options)
        logger.info(f"Found {len(upcoming_appointments.data)} upcoming appointments")
        
        # Get journal entries with specific tags
        journal_options = QueryOptions(
            filters={
                'user_id': 'patient_123',
                'tags__contains': 'anxiety'  # Contains 'anxiety' tag
            },
            order_by=['-created_at'],
            limit=5
        )
        anxiety_journals = repos['journal'].list_all(journal_options)
        logger.info(f"Found {len(anxiety_journals.data)} anxiety-related journal entries")
        
        logger.info("Query operations completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Query operations failed: {e}")
        return False


def demonstrate_analytics_operations():
    """Demonstrate analytics and reporting operations."""
    repos = setup_repositories()
    logger = get_logger('analytics_operations')
    
    try:
        # 1. Mood analytics
        logger.info("Generating mood analytics...")
        mood_trends = repos['mood'].analyze_mood_trends(
            user_id="patient_123",
            days_back=30
        )
        logger.info(f"Mood trend: {mood_trends.get('trend_direction', 'stable')}")
        
        # 2. Treatment progress analytics
        logger.info("Analyzing treatment progress...")
        treatment_progress = repos['treatment'].get_treatment_progress(
            treatment_plan_id="plan_123"
        )
        logger.info(f"Treatment completion: {treatment_progress.get('completion_percentage', 0)}%")
        
        # 3. Medication adherence analytics
        logger.info("Calculating medication adherence...")
        adherence_stats = repos['medication'].calculate_adherence_statistics(
            patient_id="patient_123",
            period_days=30
        )
        logger.info(f"Overall adherence: {adherence_stats.get('average_adherence', 0):.1f}%")
        
        # 4. Appointment analytics
        logger.info("Analyzing appointment patterns...")
        appointment_stats = repos['appointment'].get_appointment_statistics(
            provider_id="therapist_456",
            months_back=3
        )
        logger.info(f"No-show rate: {appointment_stats.get('no_show_rate', 0):.1f}%")
        
        logger.info("Analytics operations completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Analytics operations failed: {e}")
        return False


def main():
    """Main function to run all examples."""
    print("=" * 60)
    print("Mental Health Wellness Platform Repository Examples")
    print("=" * 60)
    
    examples = [
        ("Clinical Workflow", clinical_workflow_example),
        ("Patient Engagement", patient_engagement_example),
        ("Care Coordination", care_coordination_example),
        ("Crisis Management", crisis_management_example),
        ("Medication Adherence", medication_adherence_example),
        ("Query Operations", demonstrate_query_operations),
        ("Analytics Operations", demonstrate_analytics_operations)
    ]
    
    results = {}
    
    for name, example_func in examples:
        print(f"\n--- Running {name} Example ---")
        try:
            success = example_func()
            results[name] = "SUCCESS" if success else "FAILED"
            print(f"{name}: {'✓' if success else '✗'}")
        except Exception as e:
            results[name] = f"ERROR: {e}"
            print(f"{name}: ✗ (Error: {e})")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, result in results.items():
        print(f"{name:<25} {result}")
    
    # Overall success rate
    success_count = sum(1 for result in results.values() if result == "SUCCESS")
    total_count = len(results)
    print(f"\nOverall Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")


if __name__ == "__main__":
    main()
            features=["mood_tracking", "basic_analytics", "daily_checkins"],
            limits={"journal_entries_per_month": 50, "ai_sessions_per_month": 5},
            trial_days=7
        )
        
        plan_repo = SubscriptionPlanRepository(subscription_repo.db, subscription_repo.logger)
        created_basic_plan = plan_repo.create(basic_plan)
        print(f"Created plan: {created_basic_plan.name} - ${created_basic_plan.price}/month")
        
        # Premium plan
        premium_plan = SubscriptionPlan(
            name="Premium Plan",
            description="Complete mental wellness solution",
            price=Decimal('19.99'),
            billing_cycle=BillingCycle.MONTHLY.value,
            features=["mood_tracking", "advanced_analytics", "unlimited_journaling", "ai_therapy", "crisis_support"],
            limits={"journal_entries_per_month": -1, "ai_sessions_per_month": -1},  # unlimited
            trial_days=14
        )
        
        created_premium_plan = plan_repo.create(premium_plan)
        print(f"Created plan: {created_premium_plan.name} - ${created_premium_plan.price}/month")
        
        # Create subscription for user
        print("Creating subscription for user...")
        subscription = subscription_repo.create_subscription(
            user_id=user.id,
            plan_id=created_basic_plan.id,
            start_trial=True
        )
        print(f"Created subscription: {subscription.id} (Status: {subscription.status})")
        print(f"Trial ends: {subscription.trial_end}")
        
        # Log subscription creation
        audit_repo.log_user_action(
            user_id=user.id,
            action=AuditAction.CREATE.value,
            resource_type="subscription",
            resource_id=str(subscription.id),
            details={
                "plan_id": subscription.plan_id,
                "status": subscription.status,
                "trial_end": subscription.trial_end.isoformat() if subscription.trial_end else None
            }
        )
        
        # Get user subscription
        user_subscription = subscription_repo.get_user_subscription(user.id)
        print(f"User subscription status: {user_subscription.status}")
        print(f"Days until trial end: {user_subscription.days_until_trial_end()}")
        
        # Upgrade subscription
        print("Upgrading subscription...")
        upgraded_subscription = subscription_repo.upgrade_subscription(
            subscription.id, 
            created_premium_plan.id,
            prorate=True
        )
        print(f"Upgraded to plan: {upgraded_subscription.plan_id}")
        
        # Get subscription history
        history = subscription_repo.get_user_subscription_history(user.id)
        print(f"User has {len(history)} subscription records")
        
        return subscription
        
    except Exception as e:
        print(f"Error in subscription operations: {e}")
        return None


def demonstrate_session_operations(user: User):
    """Demonstrate session repository operations."""
    print("\n=== Session Repository Operations ===")
    
    _, audit_repo, _, session_repo = setup_repositories()
    
    try:
        # Create user session
        print("Creating user session...")
        session = session_repo.create_session(
            user_id=user.id,
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            device_info={
                "os": "macOS",
                "browser": "Chrome",
                "version": "96.0.4664.110"
            },
            location={"country": "US", "state": "CA", "city": "San Francisco"},
            is_remember_me=False
        )
        print(f"Created session: {session.id}")
        print(f"Session token: {session.token[:20]}...")
        print(f"Risk score: {session.risk_score}")
        
        # Log session creation
        audit_repo.log_security_event(
            action="session_created",
            user_id=user.id,
            ip_address=session.ip_address,
            details={
                "session_id": session.id,
                "user_agent": session.user_agent,
                "risk_score": session.risk_score
            }
        )
        
        # Validate session
        print("Validating session...")
        validated_session = session_repo.validate_session(session.token)
        if validated_session:
            print(f"Session validation successful: {validated_session.id}")
        
        # Update session data
        print("Updating session data...")
        session_repo.update_session_data(session.id, {
            "last_page": "/dashboard",
            "feature_flags": ["premium_ui", "beta_features"],
            "preferences": {"theme": "dark", "notifications": True}
        })
        
        # Get user sessions
        user_sessions = session_repo.get_user_sessions(user.id, active_only=True)
        print(f"User has {len(user_sessions)} active sessions")
        
        # Extend session
        print("Extending session...")
        session_repo.extend_session(session.id, timedelta(hours=12))
        
        # Create additional session (different device)
        mobile_session = session_repo.create_session(
            user_id=user.id,
            ip_address="10.0.0.50",
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
            device_info={
                "os": "iOS",
                "browser": "Safari",
                "version": "15.0"
            },
            location={"country": "US", "state": "CA", "city": "Los Angeles"},
            is_remember_me=True
        )
        print(f"Created mobile session: {mobile_session.id}")
        
        # Get session analytics
        print("Generating session analytics...")
        analytics = session_repo.generate_session_analytics(
            start_date=datetime.utcnow() - timedelta(days=30)
        )
        print(f"Analytics - Total sessions: {analytics.total_sessions}")
        print(f"Analytics - Unique users: {analytics.unique_users}")
        print(f"Analytics - Suspicious sessions: {analytics.suspicious_sessions}")
        
        return session
        
    except Exception as e:
        print(f"Error in session operations: {e}")
        return None


def demonstrate_audit_operations(user: User):
    """Demonstrate audit repository operations."""
    print("\n=== Audit Repository Operations ===")
    
    _, audit_repo, _, _ = setup_repositories()
    
    try:
        # Log various audit events
        print("Logging audit events...")
        
        # User action
        audit_repo.log_user_action(
            user_id=user.id,
            action=AuditAction.READ.value,
            resource_type="profile",
            resource_id=str(user.id),
            details={"section": "personal_info"}
        )
        
        # System event
        audit_repo.log_system_event(
            action="backup_completed",
            resource_type="database",
            details={"backup_size": "2.5GB", "duration": "45 minutes"}
        )
        
        # Security event
        audit_repo.log_security_event(
            action="failed_login",
            user_id=user.id,
            ip_address="192.168.1.100",
            details={"reason": "invalid_password", "attempt_count": 3},
            success=False
        )
        
        # Data modification with old/new values
        audit_repo.log_audit_event(
            user_id=user.id,
            action=AuditAction.UPDATE.value,
            resource_type="user",
            resource_id=str(user.id),
            old_values={"first_name": "John", "email": "john.doe@example.com"},
            new_values={"first_name": "Jonathan", "email": "john.doe@example.com"},
            level=AuditLevel.MEDIUM.value,
            compliance_category="general"
        )
        
        print("Logged various audit events")
        
        # Query audit logs
        print("Querying audit logs...")
        
        from backend.happypath.repository.audit_repository import AuditQuery
        
        # Get user's audit trail
        user_trail = audit_repo.get_user_audit_trail(user.id, limit=10)
        print(f"User audit trail: {len(user_trail)} entries")
        
        # Get security events
        security_events = audit_repo.get_security_events(
            start_time=datetime.utcnow() - timedelta(hours=24),
            limit=5
        )
        print(f"Recent security events: {len(security_events)} entries")
        
        # Get failed actions
        failed_actions = audit_repo.get_failed_actions(
            start_time=datetime.utcnow() - timedelta(hours=24),
            limit=5
        )
        print(f"Failed actions: {len(failed_actions)} entries")
        
        # Generate audit summary
        print("Generating audit summary...")
        summary = audit_repo.generate_audit_summary(
            start_time=datetime.utcnow() - timedelta(days=7),
            end_time=datetime.utcnow()
        )
        print(f"Audit summary - Total entries: {summary.total_entries}")
        print(f"Audit summary - Success rate: {summary.success_rate:.2%}")
        print(f"Audit summary - Actions breakdown: {summary.actions_breakdown}")
        
        # Export audit data
        print("Exporting audit data...")
        query = AuditQuery(
            user_id=user.id,
            start_time=datetime.utcnow() - timedelta(days=1),
            limit=100
        )
        
        json_export = audit_repo.export_audit_data(query, format="json")
        print(f"Exported audit data: {len(json_export)} characters")
        
        return True
        
    except Exception as e:
        print(f"Error in audit operations: {e}")
        return False


def demonstrate_advanced_queries():
    """Demonstrate advanced query capabilities."""
    print("\n=== Advanced Query Operations ===")
    
    user_repo, audit_repo, subscription_repo, session_repo = setup_repositories()
    
    try:
        # Advanced user queries
        print("Advanced user queries...")
        
        # Get premium users
        premium_users = user_repo.get_premium_users(limit=10)
        print(f"Premium users: {len(premium_users)}")
        
        # Get users by signup date
        recent_users = user_repo.get_users_by_signup_date(
            start_date=datetime.utcnow() - timedelta(days=30)
        )
        print(f"Users signed up in last 30 days: {len(recent_users)}")
        
        # Advanced subscription queries
        print("Advanced subscription queries...")
        
        # Get expiring subscriptions
        expiring_subs = subscription_repo.get_expiring_subscriptions(days=7)
        print(f"Subscriptions expiring in next 7 days: {len(expiring_subs)}")
        
        # Get subscriptions by status
        trial_subs = subscription_repo.get_subscriptions_by_status(
            SubscriptionStatus.TRIAL.value, 
            limit=20
        )
        print(f"Trial subscriptions: {len(trial_subs)}")
        
        # Advanced session queries
        print("Advanced session queries...")
        
        # Get suspicious sessions
        suspicious_sessions = session_repo.get_suspicious_sessions(limit=10)
        print(f"Suspicious sessions: {len(suspicious_sessions)}")
        
        # Get active sessions
        active_sessions = session_repo.get_active_sessions(limit=20)
        print(f"Active sessions: {len(active_sessions)}")
        
        # Custom query with QueryOptions
        print("Custom queries with QueryOptions...")
        
        # Find users with specific criteria
        query_options = QueryOptions(
            filters={
                'is_active': True,
                'is_verified': True
            },
            order_by=['created_at'],
            limit=10,
            include_count=True
        )
        
        result = user_repo.list_all(query_options)
        print(f"Active verified users: {len(result.data)} (Total: {result.total_count})")
        
        return True
        
    except Exception as e:
        print(f"Error in advanced queries: {e}")
        return False


def demonstrate_repository_pattern():
    """Main demonstration of repository pattern usage."""
    print("Repository Pattern Demonstration")
    print("=" * 50)
    
    try:
        # Create a user first
        user = demonstrate_user_operations()
        if not user:
            print("Failed to create user, skipping other demonstrations")
            return
        
        # Demonstrate other operations
        demonstrate_subscription_operations(user)
        demonstrate_session_operations(user)
        demonstrate_audit_operations(user)
        demonstrate_advanced_queries()
        
        print("\n" + "=" * 50)
        print("Repository pattern demonstration completed successfully!")
        
    except Exception as e:
        print(f"Error in demonstration: {e}")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run demonstration
    demonstrate_repository_pattern()
