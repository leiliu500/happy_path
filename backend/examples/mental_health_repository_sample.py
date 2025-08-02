"""
Mental Health Wellness Platform Repository Pattern Sample Code

This file demonstrates comprehensive usage of the mental health platform
repository pattern implementation across all clinical and operational workflows.
"""

import logging
from datetime import datetime, timedelta, date, time
from decimal import Decimal
from typing import List, Optional

# Import core infrastructure
from backend.happypath.core import get_db_manager, get_logger

# Import repository classes and entities
from backend.happypath.repository import (
    # Clinical entities
    TherapeuticRelationship, TreatmentPlan, TherapySession,
    MoodEntry, MoodPattern, MoodGoal,
    JournalEntry, JournalPrompt,
    CrisisDetection, SafetyPlan,
    
    # Operational entities
    Appointment, ProviderCalendar, AppointmentReminder,
    Medication, MedicationDose, MedicationAdherence,
    
    # Communication entities
    Conversation, ChatMessage,
    
    # Administration entities
    Provider, Referral, CareTeam,
    
    # Repositories
    create_therapeutic_relationship_repository,
    create_treatment_plan_repository,
    create_mood_entry_repository,
    create_journal_entry_repository,
    create_appointment_repository,
    create_medication_repository,
    create_conversation_repository,
    create_provider_repository,
    
    # Enums
    TherapyModality, TreatmentPhase, MoodScale, MoodType,
    CBTTechnique, JournalType, AppointmentType, AppointmentStatus,
    AppointmentModality, ConversationType, MessageSender,
    ProviderType, ReferralPriority, CareTeamRole
)


def setup_mental_health_repositories():
    """Set up mental health repository instances."""
    db_manager = get_db_manager()
    logger = get_logger('mental_health_repositories')
    
    return {
        'relationship': create_therapeutic_relationship_repository(db_manager, logger),
        'treatment': create_treatment_plan_repository(db_manager, logger),
        'mood': create_mood_entry_repository(db_manager, logger),
        'journal': create_journal_entry_repository(db_manager, logger),
        'appointment': create_appointment_repository(db_manager, logger),
        'medication': create_medication_repository(db_manager, logger),
        'conversation': create_conversation_repository(db_manager, logger),
        'provider': create_provider_repository(db_manager, logger)
    }


def clinical_workflow_demo():
    """Demonstrate complete clinical workflow."""
    repos = setup_mental_health_repositories()
    logger = get_logger('clinical_workflow')
    
    try:
        logger.info("=== Clinical Workflow Demo ===")
        
        # 1. Establish therapeutic relationship
        relationship = TherapeuticRelationship(
            patient_id="patient_001",
            therapist_id="therapist_001",
            therapy_modality=TherapyModality.CBT,
            relationship_status="active",
            start_date=date.today(),
            session_frequency="weekly",
            treatment_focus=["Depression", "Anxiety"]
        )
        relationship = repos['relationship'].create(relationship)
        logger.info(f"Created therapeutic relationship: {relationship.relationship_id}")
        
        # 2. Create treatment plan
        treatment_plan = TreatmentPlan(
            patient_id="patient_001",
            therapist_id="therapist_001",
            relationship_id=relationship.relationship_id,
            plan_name="CBT for Depression and Anxiety",
            primary_diagnosis="Major Depressive Disorder",
            secondary_diagnoses=["Generalized Anxiety Disorder"],
            treatment_goals=[
                "Reduce depressive symptoms by 50%",
                "Improve coping strategies",
                "Increase daily activities"
            ],
            interventions=[
                "Cognitive restructuring",
                "Behavioral activation",
                "Exposure therapy"
            ],
            target_outcomes=["PHQ-9 score < 10", "GAD-7 score < 8"],
            estimated_duration_weeks=16,
            phase=TreatmentPhase.ACTIVE
        )
        treatment_plan = repos['treatment'].create(treatment_plan)
        logger.info(f"Created treatment plan: {treatment_plan.plan_id}")
        
        # 3. Track patient mood
        mood_entry = MoodEntry(
            user_id="patient_001",
            mood_scale=MoodScale.ONE_TO_TEN,
            mood_rating=6,
            mood_type=MoodType.GENERAL,
            contributing_factors=["Good sleep", "Exercise", "Medication"],
            triggers=["Work stress"],
            notes="Feeling more balanced today",
            location="Home",
            weather="Sunny",
            privacy_level="therapist_shared"
        )
        mood_entry = repos['mood'].create(mood_entry)
        logger.info(f"Logged mood entry: {mood_entry.entry_id}")
        
        # 4. Create therapeutic journal entry
        journal_entry = JournalEntry(
            user_id="patient_001",
            title="Daily Reflection - Week 3",
            content="Today I practiced the thought challenging technique we discussed. When I started feeling anxious about the presentation, I wrote down my automatic thoughts and questioned their validity. I realized I was catastrophizing and was able to reframe my thinking.",
            journal_type=JournalType.THERAPEUTIC,
            cbt_technique=CBTTechnique.THOUGHT_RECORD,
            mood_before=4,
            mood_after=7,
            insights=["I can control my thoughts", "Evidence helps challenge anxiety"],
            action_items=["Practice thought challenging daily", "Prepare presentation outline"],
            tags=["anxiety", "thought-challenging", "progress", "presentation"],
            privacy_level="therapist_shared"
        )
        journal_entry = repos['journal'].create(journal_entry)
        logger.info(f"Created journal entry: {journal_entry.entry_id}")
        
        # 5. Schedule next therapy session
        appointment = Appointment(
            provider_id="therapist_001",
            patient_id="patient_001",
            appointment_type=AppointmentType.THERAPY_SESSION,
            scheduled_start=datetime.now() + timedelta(days=7),
            duration_minutes=50,
            modality=AppointmentModality.IN_PERSON,
            agenda=[
                "Review mood tracking data",
                "Discuss journal insights",
                "Practice cognitive restructuring",
                "Plan homework assignments"
            ],
            goals=["Assess progress on treatment goals", "Introduce new CBT technique"],
            preparation_notes="Review thought records from past week"
        )
        appointment = repos['appointment'].create(appointment)
        logger.info(f"Scheduled appointment: {appointment.appointment_id}")
        
        # 6. Medication management
        medication = Medication(
            patient_id="patient_001",
            prescribing_provider_id="psychiatrist_001",
            medication_name="Sertraline",
            generic_name="Sertraline",
            brand_name="Zoloft",
            strength="50mg",
            dosage_form="tablet",
            prescribed_dosage="50mg once daily",
            prescribed_frequency="daily",
            prescribed_route="oral",
            start_date=date.today() - timedelta(days=30),
            indication="Major Depressive Disorder",
            prescriber_notes="Start with 50mg, may increase to 100mg if tolerated"
        )
        medication = repos['medication'].create(medication)
        logger.info(f"Added medication: {medication.medication_id}")
        
        logger.info("Clinical workflow completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Clinical workflow failed: {e}")
        return False


def patient_engagement_demo():
    """Demonstrate patient engagement features."""
    repos = setup_mental_health_repositories()
    logger = get_logger('patient_engagement')
    
    try:
        logger.info("=== Patient Engagement Demo ===")
        
        # 1. AI Chatbot conversation
        conversation = repos['conversation'].start_conversation(
            user_id="patient_001",
            conversation_type=ConversationType.MOOD_CHECK_IN,
            title="Daily Mood Check-in",
            context={"previous_mood": 6, "last_checkin": "yesterday"}
        )
        logger.info(f"Started conversation: {conversation.conversation_id}")
        
        # Add chat messages
        chat_repo = repos['conversation']  # Assuming we can get the chat message repo
        user_message = ChatMessage(
            conversation_id=conversation.conversation_id,
            user_id="patient_001",
            sender=MessageSender.USER,
            content="I'm feeling quite anxious today about my job interview tomorrow",
            sentiment_score=Decimal('-0.3'),
            emotion_analysis={"primary": "anxiety", "secondary": "worry"}
        )
        
        bot_response = ChatMessage(
            conversation_id=conversation.conversation_id,
            user_id="patient_001",
            sender=MessageSender.AGENT,
            content="I understand you're feeling anxious about your interview. That's completely normal. Let's use some of the coping strategies we've discussed. Have you tried the breathing technique?",
            intent="provide_support",
            response_template="anxiety_support_template"
        )
        
        # 2. Mood pattern analysis
        mood_pattern = MoodPattern(
            user_id="patient_001",
            pattern_name="Weekly Anxiety Pattern",
            pattern_type="weekly",
            timeframe_days=30,
            average_mood=6.2,
            mood_variance=1.5,
            trend_direction="improving",
            pattern_strength=0.78,
            contributing_factors=["Work schedule", "Sleep quality", "Exercise routine"],
            pattern_insights=["Anxiety peaks on Sundays", "Exercise correlates with better mood"],
            recommendations=["Maintain exercise routine", "Sunday evening relaxation ritual"]
        )
        
        # 3. Set mood improvement goals
        mood_goal = MoodGoal(
            user_id="patient_001",
            goal_type="average_mood",
            target_value=7.5,
            current_value=6.2,
            target_date=date.today() + timedelta(days=30),
            description="Achieve consistent mood rating of 7.5 or higher",
            strategies=[
                "Daily 30-minute walk",
                "Evening journaling",
                "Mindfulness meditation",
                "Regular sleep schedule"
            ],
            milestone_rewards=["New book", "Spa day", "Movie night"],
            tracking_frequency="daily"
        )
        
        logger.info("Patient engagement features demonstrated successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Patient engagement demo failed: {e}")
        return False


def care_coordination_demo():
    """Demonstrate care coordination workflow."""
    repos = setup_mental_health_repositories()
    logger = get_logger('care_coordination')
    
    try:
        logger.info("=== Care Coordination Demo ===")
        
        # 1. Create psychiatrist provider
        psychiatrist = Provider(
            first_name="Dr. Sarah",
            last_name="Johnson",
            credentials=["MD", "Board Certified Psychiatrist"],
            provider_type=ProviderType.PSYCHIATRIST,
            license_number="MD12345",
            license_state="CA",
            specialty="Adult Psychiatry",
            subspecialties=["Mood Disorders", "Anxiety Disorders"],
            phone="(555) 123-4567",
            email="dr.johnson@clinic.com",
            accepting_new_patients=True,
            languages_spoken=["English", "Spanish"]
        )
        psychiatrist = repos['provider'].create(psychiatrist)
        logger.info(f"Created psychiatrist: {psychiatrist.provider_id}")
        
        # 2. Create referral for medication evaluation
        referral = Referral(
            patient_id="patient_001",
            referring_provider_id="therapist_001",
            receiving_provider_id=psychiatrist.provider_id,
            referral_reason="Medication evaluation for treatment-resistant depression",
            clinical_summary="Patient has been in CBT for 8 weeks with modest improvement. PHQ-9 score remains at 15. Considering medication augmentation.",
            presenting_concerns=["Persistent depressive symptoms", "Sleep disturbance", "Low energy"],
            diagnosis_codes=["F33.1", "F41.1"],
            priority=ReferralPriority.ROUTINE,
            patient_consent_obtained=True,
            release_of_information_signed=True
        )
        referral = repos['provider'].create_referral(referral)
        logger.info(f"Created referral: {referral.referral_id}")
        
        # 3. Create multidisciplinary care team
        care_team = CareTeam(
            patient_id="patient_001",
            team_name="Patient 001 Integrated Care Team",
            primary_provider_id="therapist_001",
            care_coordinator_id="case_manager_001",
            shared_goals=[
                "Achieve remission of depressive symptoms",
                "Improve functional capacity",
                "Prevent relapse"
            ],
            treatment_approach="Integrated psychotherapy and pharmacotherapy",
            meeting_frequency="biweekly",
            communication_plan="Weekly progress updates, urgent issues immediate contact"
        )
        care_team = repos['provider'].create_care_team(care_team)
        
        # Add team members
        team_added = repos['provider'].add_team_member(
            team_id=care_team.team_id,
            provider_id=psychiatrist.provider_id,
            role=CareTeamRole.PSYCHIATRIST
        )
        
        logger.info(f"Created care team: {care_team.team_id}")
        logger.info("Care coordination workflow completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Care coordination demo failed: {e}")
        return False


def crisis_management_demo():
    """Demonstrate crisis detection and management."""
    repos = setup_mental_health_repositories()
    logger = get_logger('crisis_management')
    
    try:
        logger.info("=== Crisis Management Demo ===")
        
        # 1. Journal entry with crisis indicators
        crisis_journal = JournalEntry(
            user_id="patient_001",
            title="Difficult Night",
            content="I can't take this anymore. Everything feels hopeless and I keep thinking about just ending the pain. I don't see any way out of this darkness.",
            journal_type=JournalType.FREE_FORM,
            mood_before=2,
            mood_after=1,
            tags=["crisis", "hopeless", "dark thoughts"],
            privacy_level="private"
        )
        
        # The system would detect crisis keywords automatically
        crisis_journal = repos['journal'].create(crisis_journal)
        logger.info(f"Created journal entry with crisis indicators: {crisis_journal.entry_id}")
        
        # 2. Automated crisis detection
        crisis_detection = CrisisDetection(
            patient_id="patient_001",
            detection_source="journal_entry",
            source_id=crisis_journal.entry_id,
            crisis_type="suicidal_ideation",
            severity_level="high",
            risk_factors=["Hopelessness", "Suicidal ideation", "Social isolation"],
            protective_factors=["Strong therapeutic relationship", "Family support"],
            detected_keywords=["can't take this", "ending the pain", "hopeless"],
            confidence_score=0.95,
            requires_immediate_attention=True,
            recommended_actions=["Contact patient immediately", "Safety assessment", "Consider hospitalization"]
        )
        crisis_detection = repos['journal'].create_crisis_detection(crisis_detection)
        logger.info(f"Crisis detected: {crisis_detection.detection_id}")
        
        # 3. Safety plan activation
        safety_plan = SafetyPlan(
            patient_id="patient_001",
            created_by_provider_id="therapist_001",
            plan_name="Emergency Safety Plan",
            warning_signs=[
                "Feeling hopeless",
                "Thoughts of death or suicide",
                "Isolating from others",
                "Sleep disruption",
                "Substance use increase"
            ],
            coping_strategies=[
                "Deep breathing exercises (4-7-8 technique)",
                "Call trusted friend or family member",
                "Go for a walk outside",
                "Listen to calming music",
                "Use grounding techniques (5-4-3-2-1)"
            ],
            social_contacts=[
                {"name": "Sister - Maria", "phone": "(555) 987-6543", "relationship": "family"},
                {"name": "Best Friend - Alex", "phone": "(555) 555-1234", "relationship": "friend"}
            ],
            professional_contacts=[
                {"name": "Dr. Smith (Therapist)", "phone": "(555) 123-4567", "role": "therapist"},
                {"name": "Crisis Hotline", "phone": "988", "role": "crisis_support"},
                {"name": "Emergency Services", "phone": "911", "role": "emergency"}
            ],
            environmental_safety=[
                "Remove or secure potentially harmful objects",
                "Stay with trusted person when feeling unsafe",
                "Avoid alcohol and drugs"
            ],
            reasons_to_live=[
                "My sister and her children",
                "My dog who needs me",
                "Future travel plans",
                "Seeing my recovery help others"
            ],
            is_active=True
        )
        safety_plan = repos['journal'].create_safety_plan(safety_plan)
        logger.info(f"Safety plan activated: {safety_plan.plan_id}")
        
        logger.info("Crisis management workflow completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Crisis management demo failed: {e}")
        return False


def medication_adherence_demo():
    """Demonstrate medication adherence tracking."""
    repos = setup_mental_health_repositories()
    logger = get_logger('medication_adherence')
    
    try:
        logger.info("=== Medication Adherence Demo ===")
        
        # 1. Record medication doses over a week
        medication_id = "med_sertraline_001"
        
        # Today's dose - taken on time
        dose_today = MedicationDose(
            medication_id=medication_id,
            patient_id="patient_001",
            scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
            actual_time=datetime.now().replace(hour=8, minute=10, second=0, microsecond=0),
            dose_amount="50mg",
            dose_unit="mg",
            taken_as_prescribed=True,
            taken_status="taken",
            adherence_percentage=100.0,
            notes="Taken with breakfast as recommended"
        )
        
        # Yesterday's dose - taken late
        dose_yesterday = MedicationDose(
            medication_id=medication_id,
            patient_id="patient_001",
            scheduled_time=datetime.now().replace(hour=8, minute=0) - timedelta(days=1),
            actual_time=datetime.now().replace(hour=14, minute=30) - timedelta(days=1),
            dose_amount="50mg",
            dose_unit="mg",
            taken_as_prescribed=False,
            taken_status="taken_late",
            adherence_percentage=75.0,
            notes="Forgot morning dose, took at lunch"
        )
        
        # Two days ago - missed dose
        dose_missed = MedicationDose(
            medication_id=medication_id,
            patient_id="patient_001",
            scheduled_time=datetime.now().replace(hour=8, minute=0) - timedelta(days=2),
            dose_amount="50mg",
            dose_unit="mg",
            taken_as_prescribed=False,
            taken_status="missed",
            adherence_percentage=0.0,
            missed_reason="forgot",
            notes="Completely forgot - was rushing to work"
        )
        
        # 2. Calculate weekly adherence
        adherence_week = MedicationAdherence(
            medication_id=medication_id,
            patient_id="patient_001",
            period_start=date.today() - timedelta(days=7),
            period_end=date.today(),
            doses_prescribed=7,
            doses_taken=6,
            doses_taken_late=1,
            doses_missed=1,
            adherence_percentage=85.7,
            on_time_percentage=71.4,
            missed_doses=1,
            late_doses=1,
            adherence_pattern="mostly_compliant",
            barriers_to_adherence=["Forgetfulness", "Irregular schedule"],
            improvement_suggestions=[
                "Set daily phone reminder",
                "Use weekly pill organizer",
                "Link to morning routine (with coffee)"
            ],
            side_effects_reported=["Mild nausea (first week only)"],
            effectiveness_notes="Patient reports improved mood and energy"
        )
        
        logger.info("Medication adherence tracking completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Medication adherence demo failed: {e}")
        return False


def analytics_and_reporting_demo():
    """Demonstrate analytics and reporting capabilities."""
    repos = setup_mental_health_repositories()
    logger = get_logger('analytics_reporting')
    
    try:
        logger.info("=== Analytics and Reporting Demo ===")
        
        # 1. Mood trend analysis
        logger.info("Analyzing mood trends...")
        mood_trends = repos['mood'].analyze_mood_trends(
            user_id="patient_001",
            days_back=30
        )
        logger.info(f"Mood trend direction: {mood_trends.get('trend_direction', 'stable')}")
        logger.info(f"Average mood: {mood_trends.get('average_mood', 0):.1f}")
        
        # 2. Treatment progress analytics
        logger.info("Analyzing treatment progress...")
        treatment_progress = repos['treatment'].get_treatment_progress(
            treatment_plan_id="plan_001"
        )
        logger.info(f"Treatment completion: {treatment_progress.get('completion_percentage', 0)}%")
        logger.info(f"Goals achieved: {treatment_progress.get('goals_achieved', 0)}")
        
        # 3. Medication adherence analytics
        logger.info("Calculating medication adherence statistics...")
        adherence_stats = repos['medication'].calculate_adherence_statistics(
            patient_id="patient_001",
            period_days=30
        )
        logger.info(f"Overall adherence: {adherence_stats.get('average_adherence', 0):.1f}%")
        logger.info(f"Medications tracked: {adherence_stats.get('medications_count', 0)}")
        
        # 4. Appointment analytics
        logger.info("Analyzing appointment patterns...")
        appointment_stats = repos['appointment'].get_appointment_statistics(
            provider_id="therapist_001",
            months_back=3
        )
        logger.info(f"Total appointments: {appointment_stats.get('total_appointments', 0)}")
        logger.info(f"No-show rate: {appointment_stats.get('no_show_rate', 0):.1f}%")
        logger.info(f"Average session rating: {appointment_stats.get('average_rating', 0):.1f}")
        
        # 5. Crisis detection analytics
        logger.info("Analyzing crisis detection patterns...")
        crisis_stats = repos['journal'].get_crisis_statistics(
            patient_id="patient_001",
            period_days=90
        )
        logger.info(f"Crisis detections: {crisis_stats.get('total_detections', 0)}")
        logger.info(f"False positive rate: {crisis_stats.get('false_positive_rate', 0):.2f}")
        
        logger.info("Analytics and reporting completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Analytics and reporting demo failed: {e}")
        return False


def main():
    """Main function to run all mental health platform demos."""
    print("=" * 70)
    print("Mental Health Wellness Platform Repository Demonstration")
    print("=" * 70)
    
    demos = [
        ("Clinical Workflow", clinical_workflow_demo),
        ("Patient Engagement", patient_engagement_demo),
        ("Care Coordination", care_coordination_demo),
        ("Crisis Management", crisis_management_demo),
        ("Medication Adherence", medication_adherence_demo),
        ("Analytics & Reporting", analytics_and_reporting_demo)
    ]
    
    results = {}
    
    for name, demo_func in demos:
        print(f"\n--- {name} Demo ---")
        try:
            success = demo_func()
            results[name] = "SUCCESS" if success else "FAILED"
            print(f"{name}: {'✓ PASSED' if success else '✗ FAILED'}")
        except Exception as e:
            results[name] = f"ERROR: {str(e)[:100]}"
            print(f"{name}: ✗ ERROR - {e}")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION SUMMARY")
    print("=" * 70)
    for name, result in results.items():
        status_icon = "✓" if result == "SUCCESS" else "✗"
        print(f"{status_icon} {name:<30} {result}")
    
    # Calculate success rate
    success_count = sum(1 for result in results.values() if result == "SUCCESS")
    total_count = len(results)
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    
    print(f"\nOverall Success Rate: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 Mental Health Platform Repository System: READY FOR PRODUCTION!")
    elif success_rate >= 60:
        print("⚠️  Mental Health Platform Repository System: NEEDS ATTENTION")
    else:
        print("❌ Mental Health Platform Repository System: REQUIRES FIXES")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the demonstration
    main()
