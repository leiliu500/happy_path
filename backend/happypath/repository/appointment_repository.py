"""
Appointment Scheduling Repository

Repository implementation for appointment scheduling, provider calendars,
and appointment management functionality.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, time, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class AppointmentType(Enum):
    """Appointment type enumeration."""
    INITIAL_CONSULTATION = "initial_consultation"
    FOLLOW_UP = "follow_up"
    THERAPY_SESSION = "therapy_session"
    PSYCHIATRIC_EVALUATION = "psychiatric_evaluation"
    MEDICATION_MANAGEMENT = "medication_management"
    CRISIS_INTERVENTION = "crisis_intervention"
    GROUP_THERAPY = "group_therapy"
    FAMILY_THERAPY = "family_therapy"
    COUPLES_THERAPY = "couples_therapy"
    PSYCHOLOGICAL_TESTING = "psychological_testing"
    TELEHEALTH = "telehealth"
    PHONE_CONSULTATION = "phone_consultation"
    CHECK_IN = "check_in"
    ADMINISTRATIVE = "administrative"


class AppointmentStatus(Enum):
    """Appointment status enumeration."""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    ARRIVED = "arrived"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED_BY_PATIENT = "cancelled_by_patient"
    CANCELLED_BY_PROVIDER = "cancelled_by_provider"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"
    LATE_CANCELLATION = "late_cancellation"


class AppointmentModality(Enum):
    """Appointment modality enumeration."""
    IN_PERSON = "in_person"
    TELEHEALTH = "telehealth"
    PHONE = "phone"
    HYBRID = "hybrid"


class ReminderType(Enum):
    """Reminder type enumeration."""
    EMAIL = "email"
    SMS = "sms"
    PHONE_CALL = "phone_call"
    PUSH_NOTIFICATION = "push_notification"
    POSTAL_MAIL = "postal_mail"


@dataclass
class ProviderCalendar:
    """Provider calendar entity."""
    calendar_id: Optional[str] = None
    provider_id: Optional[str] = None
    
    # Calendar settings
    calendar_name: str = ""
    time_zone: str = "UTC"
    default_appointment_duration: int = 50  # minutes
    
    # Weekly availability
    monday_start_time: Optional[time] = None
    monday_end_time: Optional[time] = None
    tuesday_start_time: Optional[time] = None
    tuesday_end_time: Optional[time] = None
    wednesday_start_time: Optional[time] = None
    wednesday_end_time: Optional[time] = None
    thursday_start_time: Optional[time] = None
    thursday_end_time: Optional[time] = None
    friday_start_time: Optional[time] = None
    friday_end_time: Optional[time] = None
    saturday_start_time: Optional[time] = None
    saturday_end_time: Optional[time] = None
    sunday_start_time: Optional[time] = None
    sunday_end_time: Optional[time] = None
    
    # Booking settings
    advance_booking_days: int = 30
    minimum_notice_hours: int = 24
    buffer_time_minutes: int = 10
    
    # Cancellation policy
    cancellation_notice_hours: int = 24
    late_cancellation_fee: Optional[Decimal] = None
    no_show_fee: Optional[Decimal] = None
    
    # Auto-scheduling settings
    auto_confirm_appointments: bool = False
    max_daily_appointments: Optional[int] = None
    lunch_break_start: Optional[time] = None
    lunch_break_end: Optional[time] = None
    
    # Availability preferences
    preferred_appointment_types: Optional[List[AppointmentType]] = None
    blocked_dates: Optional[List[date]] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Appointment:
    """Appointment entity."""
    appointment_id: Optional[str] = None
    provider_id: Optional[str] = None
    patient_id: Optional[str] = None
    
    # Appointment details
    appointment_type: AppointmentType = AppointmentType.THERAPY_SESSION
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    modality: AppointmentModality = AppointmentModality.IN_PERSON
    
    # Scheduling
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    duration_minutes: int = 50
    
    # Location and access
    location: Optional[str] = None
    room_number: Optional[str] = None
    telehealth_link: Optional[str] = None
    phone_number: Optional[str] = None
    access_instructions: Optional[str] = None
    
    # Appointment content
    agenda: Optional[List[str]] = None
    preparation_notes: Optional[str] = None
    goals: Optional[List[str]] = None
    
    # Follow-up from previous
    previous_appointment_id: Optional[str] = None
    follow_up_from_session: Optional[str] = None
    
    # Administrative
    insurance_authorization: Optional[str] = None
    billing_code: Optional[str] = None
    billing_status: str = "pending"
    
    # Confirmation and reminders
    confirmed_by_patient: bool = False
    confirmed_at: Optional[datetime] = None
    reminder_sent: bool = False
    reminder_methods: Optional[List[ReminderType]] = None
    
    # Cancellation and rescheduling
    cancellation_reason: Optional[str] = None
    cancelled_at: Optional[datetime] = None
    cancelled_by: Optional[str] = None
    reschedule_count: int = 0
    original_appointment_id: Optional[str] = None
    
    # Technical details (for telehealth)
    platform_used: Optional[str] = None
    connection_quality: Optional[str] = None
    technical_issues: Optional[List[str]] = None
    
    # Notes and outcomes
    provider_notes: Optional[str] = None
    patient_feedback: Optional[str] = None
    session_rating: Optional[int] = None  # 1-10 scale
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class AppointmentReminder:
    """Appointment reminder entity."""
    reminder_id: Optional[str] = None
    appointment_id: Optional[str] = None
    patient_id: Optional[str] = None
    
    # Reminder details
    reminder_type: ReminderType = ReminderType.EMAIL
    scheduled_time: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    
    # Content
    subject: Optional[str] = None
    message: str = ""
    
    # Delivery status
    delivery_status: str = "pending"  # pending, sent, delivered, failed
    delivery_attempts: int = 0
    delivery_error: Optional[str] = None
    
    # Response tracking
    opened: bool = False
    clicked: bool = False
    responded: bool = False
    
    created_at: Optional[datetime] = None


@dataclass
class ProviderAvailability:
    """Provider availability entity."""
    availability_id: Optional[str] = None
    provider_id: Optional[str] = None
    
    # Date and time
    availability_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    # Availability type
    availability_type: str = "regular"  # regular, exception, blocked, emergency
    is_available: bool = True
    
    # Override settings
    appointment_types_allowed: Optional[List[AppointmentType]] = None
    max_appointments: Optional[int] = None
    
    # Reason for exception
    reason: Optional[str] = None
    notes: Optional[str] = None
    
    # Recurring settings
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # weekly, biweekly, monthly
    recurrence_end_date: Optional[date] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProviderCalendarRepository(BaseRepository[ProviderCalendar, str]):
    """Repository for provider calendar management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "provider_calendars", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> ProviderCalendar:
        """Convert database row to ProviderCalendar entity."""
        return ProviderCalendar(
            calendar_id=row.get('calendar_id'),
            provider_id=row.get('provider_id'),
            calendar_name=row.get('calendar_name', ''),
            time_zone=row.get('time_zone', 'UTC'),
            default_appointment_duration=row.get('default_appointment_duration', 50),
            monday_start_time=row.get('monday_start_time'),
            monday_end_time=row.get('monday_end_time'),
            tuesday_start_time=row.get('tuesday_start_time'),
            tuesday_end_time=row.get('tuesday_end_time'),
            wednesday_start_time=row.get('wednesday_start_time'),
            wednesday_end_time=row.get('wednesday_end_time'),
            thursday_start_time=row.get('thursday_start_time'),
            thursday_end_time=row.get('thursday_end_time'),
            friday_start_time=row.get('friday_start_time'),
            friday_end_time=row.get('friday_end_time'),
            saturday_start_time=row.get('saturday_start_time'),
            saturday_end_time=row.get('saturday_end_time'),
            sunday_start_time=row.get('sunday_start_time'),
            sunday_end_time=row.get('sunday_end_time'),
            advance_booking_days=row.get('advance_booking_days', 30),
            minimum_notice_hours=row.get('minimum_notice_hours', 24),
            buffer_time_minutes=row.get('buffer_time_minutes', 10),
            cancellation_notice_hours=row.get('cancellation_notice_hours', 24),
            late_cancellation_fee=Decimal(str(row['late_cancellation_fee'])) if row.get('late_cancellation_fee') else None,
            no_show_fee=Decimal(str(row['no_show_fee'])) if row.get('no_show_fee') else None,
            auto_confirm_appointments=row.get('auto_confirm_appointments', False),
            max_daily_appointments=row.get('max_daily_appointments'),
            lunch_break_start=row.get('lunch_break_start'),
            lunch_break_end=row.get('lunch_break_end'),
            preferred_appointment_types=[AppointmentType(t) for t in row.get('preferred_appointment_types', [])],
            blocked_dates=row.get('blocked_dates', []),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: ProviderCalendar) -> Dict[str, Any]:
        """Convert ProviderCalendar entity to dictionary."""
        return {
            'calendar_id': entity.calendar_id,
            'provider_id': entity.provider_id,
            'calendar_name': entity.calendar_name,
            'time_zone': entity.time_zone,
            'default_appointment_duration': entity.default_appointment_duration,
            'monday_start_time': entity.monday_start_time,
            'monday_end_time': entity.monday_end_time,
            'tuesday_start_time': entity.tuesday_start_time,
            'tuesday_end_time': entity.tuesday_end_time,
            'wednesday_start_time': entity.wednesday_start_time,
            'wednesday_end_time': entity.wednesday_end_time,
            'thursday_start_time': entity.thursday_start_time,
            'thursday_end_time': entity.thursday_end_time,
            'friday_start_time': entity.friday_start_time,
            'friday_end_time': entity.friday_end_time,
            'saturday_start_time': entity.saturday_start_time,
            'saturday_end_time': entity.saturday_end_time,
            'sunday_start_time': entity.sunday_start_time,
            'sunday_end_time': entity.sunday_end_time,
            'advance_booking_days': entity.advance_booking_days,
            'minimum_notice_hours': entity.minimum_notice_hours,
            'buffer_time_minutes': entity.buffer_time_minutes,
            'cancellation_notice_hours': entity.cancellation_notice_hours,
            'late_cancellation_fee': entity.late_cancellation_fee,
            'no_show_fee': entity.no_show_fee,
            'auto_confirm_appointments': entity.auto_confirm_appointments,
            'max_daily_appointments': entity.max_daily_appointments,
            'lunch_break_start': entity.lunch_break_start,
            'lunch_break_end': entity.lunch_break_end,
            'preferred_appointment_types': [t.value for t in entity.preferred_appointment_types] if entity.preferred_appointment_types else [],
            'blocked_dates': entity.blocked_dates,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: ProviderCalendar, is_update: bool = False) -> None:
        """Validate ProviderCalendar entity."""
        if not entity.provider_id:
            raise ValidationError("Provider ID is required")
        
        if not entity.calendar_name:
            raise ValidationError("Calendar name is required")
        
        if entity.default_appointment_duration <= 0:
            raise ValidationError("Default appointment duration must be positive")
        
        if entity.advance_booking_days < 0:
            raise ValidationError("Advance booking days must be non-negative")
        
        if entity.minimum_notice_hours < 0:
            raise ValidationError("Minimum notice hours must be non-negative")
        
        if entity.buffer_time_minutes < 0:
            raise ValidationError("Buffer time must be non-negative")
        
        if not entity.calendar_id and not is_update:
            import uuid
            entity.calendar_id = str(uuid.uuid4())
    
    def get_provider_calendar(self, provider_id: str) -> Optional[ProviderCalendar]:
        """Get calendar for a provider."""
        return self.find_one_by(provider_id=provider_id)


class AppointmentRepository(BaseRepository[Appointment, str]):
    """Repository for appointment management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "appointments", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> Appointment:
        """Convert database row to Appointment entity."""
        return Appointment(
            appointment_id=row.get('appointment_id'),
            provider_id=row.get('provider_id'),
            patient_id=row.get('patient_id'),
            appointment_type=AppointmentType(row['appointment_type']) if row.get('appointment_type') else AppointmentType.THERAPY_SESSION,
            status=AppointmentStatus(row['status']) if row.get('status') else AppointmentStatus.SCHEDULED,
            modality=AppointmentModality(row['modality']) if row.get('modality') else AppointmentModality.IN_PERSON,
            scheduled_start=row.get('scheduled_start'),
            scheduled_end=row.get('scheduled_end'),
            actual_start=row.get('actual_start'),
            actual_end=row.get('actual_end'),
            duration_minutes=row.get('duration_minutes', 50),
            location=row.get('location'),
            room_number=row.get('room_number'),
            telehealth_link=row.get('telehealth_link'),
            phone_number=row.get('phone_number'),
            access_instructions=row.get('access_instructions'),
            agenda=row.get('agenda', []),
            preparation_notes=row.get('preparation_notes'),
            goals=row.get('goals', []),
            previous_appointment_id=row.get('previous_appointment_id'),
            follow_up_from_session=row.get('follow_up_from_session'),
            insurance_authorization=row.get('insurance_authorization'),
            billing_code=row.get('billing_code'),
            billing_status=row.get('billing_status', 'pending'),
            confirmed_by_patient=row.get('confirmed_by_patient', False),
            confirmed_at=row.get('confirmed_at'),
            reminder_sent=row.get('reminder_sent', False),
            reminder_methods=[ReminderType(r) for r in row.get('reminder_methods', [])],
            cancellation_reason=row.get('cancellation_reason'),
            cancelled_at=row.get('cancelled_at'),
            cancelled_by=row.get('cancelled_by'),
            reschedule_count=row.get('reschedule_count', 0),
            original_appointment_id=row.get('original_appointment_id'),
            platform_used=row.get('platform_used'),
            connection_quality=row.get('connection_quality'),
            technical_issues=row.get('technical_issues', []),
            provider_notes=row.get('provider_notes'),
            patient_feedback=row.get('patient_feedback'),
            session_rating=row.get('session_rating'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: Appointment) -> Dict[str, Any]:
        """Convert Appointment entity to dictionary."""
        return {
            'appointment_id': entity.appointment_id,
            'provider_id': entity.provider_id,
            'patient_id': entity.patient_id,
            'appointment_type': entity.appointment_type.value,
            'status': entity.status.value,
            'modality': entity.modality.value,
            'scheduled_start': entity.scheduled_start,
            'scheduled_end': entity.scheduled_end,
            'actual_start': entity.actual_start,
            'actual_end': entity.actual_end,
            'duration_minutes': entity.duration_minutes,
            'location': entity.location,
            'room_number': entity.room_number,
            'telehealth_link': entity.telehealth_link,
            'phone_number': entity.phone_number,
            'access_instructions': entity.access_instructions,
            'agenda': entity.agenda,
            'preparation_notes': entity.preparation_notes,
            'goals': entity.goals,
            'previous_appointment_id': entity.previous_appointment_id,
            'follow_up_from_session': entity.follow_up_from_session,
            'insurance_authorization': entity.insurance_authorization,
            'billing_code': entity.billing_code,
            'billing_status': entity.billing_status,
            'confirmed_by_patient': entity.confirmed_by_patient,
            'confirmed_at': entity.confirmed_at,
            'reminder_sent': entity.reminder_sent,
            'reminder_methods': [r.value for r in entity.reminder_methods] if entity.reminder_methods else [],
            'cancellation_reason': entity.cancellation_reason,
            'cancelled_at': entity.cancelled_at,
            'cancelled_by': entity.cancelled_by,
            'reschedule_count': entity.reschedule_count,
            'original_appointment_id': entity.original_appointment_id,
            'platform_used': entity.platform_used,
            'connection_quality': entity.connection_quality,
            'technical_issues': entity.technical_issues,
            'provider_notes': entity.provider_notes,
            'patient_feedback': entity.patient_feedback,
            'session_rating': entity.session_rating,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: Appointment, is_update: bool = False) -> None:
        """Validate Appointment entity."""
        if not entity.provider_id:
            raise ValidationError("Provider ID is required")
        
        if not entity.patient_id:
            raise ValidationError("Patient ID is required")
        
        if not entity.scheduled_start:
            raise ValidationError("Scheduled start time is required")
        
        if entity.duration_minutes <= 0:
            raise ValidationError("Duration must be positive")
        
        if entity.reschedule_count < 0:
            raise ValidationError("Reschedule count must be non-negative")
        
        if entity.session_rating and (entity.session_rating < 1 or entity.session_rating > 10):
            raise ValidationError("Session rating must be between 1 and 10")
        
        # Calculate scheduled end if not provided
        if not entity.scheduled_end and entity.scheduled_start:
            entity.scheduled_end = entity.scheduled_start + timedelta(minutes=entity.duration_minutes)
        
        if not entity.appointment_id and not is_update:
            import uuid
            entity.appointment_id = str(uuid.uuid4())
    
    def get_patient_appointments(self, patient_id: str, start_date: date = None, 
                               end_date: date = None, status: AppointmentStatus = None) -> List[Appointment]:
        """Get appointments for a patient."""
        filters = {'patient_id': patient_id}
        
        if start_date:
            filters['scheduled_start__gte'] = datetime.combine(start_date, datetime.min.time())
        if end_date:
            filters['scheduled_start__lte'] = datetime.combine(end_date, datetime.max.time())
        if status:
            filters['status'] = status.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['-scheduled_start']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_provider_appointments(self, provider_id: str, appointment_date: date) -> List[Appointment]:
        """Get appointments for a provider on a specific date."""
        start_datetime = datetime.combine(appointment_date, datetime.min.time())
        end_datetime = datetime.combine(appointment_date, datetime.max.time())
        
        options = QueryOptions(
            filters={
                'provider_id': provider_id,
                'scheduled_start__gte': start_datetime,
                'scheduled_start__lte': end_datetime
            },
            order_by=['scheduled_start']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_upcoming_appointments(self, provider_id: str = None, patient_id: str = None, 
                                days_ahead: int = 7) -> List[Appointment]:
        """Get upcoming appointments."""
        start_datetime = datetime.now()
        end_datetime = start_datetime + timedelta(days=days_ahead)
        
        filters = {
            'scheduled_start__gte': start_datetime,
            'scheduled_start__lte': end_datetime,
            'status__in': ['scheduled', 'confirmed']
        }
        
        if provider_id:
            filters['provider_id'] = provider_id
        if patient_id:
            filters['patient_id'] = patient_id
        
        options = QueryOptions(
            filters=filters,
            order_by=['scheduled_start']
        )
        
        result = self.list_all(options)
        return result.data
    
    def confirm_appointment(self, appointment_id: str) -> bool:
        """Confirm an appointment."""
        try:
            appointment = self.get_by_id(appointment_id)
            if not appointment:
                return False
            
            appointment.status = AppointmentStatus.CONFIRMED
            appointment.confirmed_by_patient = True
            appointment.confirmed_at = datetime.now()
            
            self.update(appointment)
            
            self.logger.info(f"Confirmed appointment {appointment_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to confirm appointment {appointment_id}: {e}")
            return False
    
    def cancel_appointment(self, appointment_id: str, reason: str, 
                          cancelled_by: str) -> bool:
        """Cancel an appointment."""
        try:
            appointment = self.get_by_id(appointment_id)
            if not appointment:
                return False
            
            # Determine cancellation type based on timing
            time_until_appointment = appointment.scheduled_start - datetime.now()
            hours_until = time_until_appointment.total_seconds() / 3600
            
            if cancelled_by == 'patient':
                if hours_until < 24:  # Less than 24 hours notice
                    appointment.status = AppointmentStatus.LATE_CANCELLATION
                else:
                    appointment.status = AppointmentStatus.CANCELLED_BY_PATIENT
            else:
                appointment.status = AppointmentStatus.CANCELLED_BY_PROVIDER
            
            appointment.cancellation_reason = reason
            appointment.cancelled_at = datetime.now()
            appointment.cancelled_by = cancelled_by
            
            self.update(appointment)
            
            self.logger.info(f"Cancelled appointment {appointment_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cancel appointment {appointment_id}: {e}")
            return False
    
    def reschedule_appointment(self, appointment_id: str, new_start_time: datetime) -> Optional[Appointment]:
        """Reschedule an appointment."""
        try:
            original_appointment = self.get_by_id(appointment_id)
            if not original_appointment:
                return None
            
            # Create new appointment
            new_appointment_dict = self._to_dict(original_appointment)
            new_appointment_dict['appointment_id'] = None  # Will be auto-generated
            new_appointment_dict['scheduled_start'] = new_start_time
            new_appointment_dict['scheduled_end'] = new_start_time + timedelta(minutes=original_appointment.duration_minutes)
            new_appointment_dict['status'] = AppointmentStatus.SCHEDULED.value
            new_appointment_dict['confirmed_by_patient'] = False
            new_appointment_dict['confirmed_at'] = None
            new_appointment_dict['reschedule_count'] = original_appointment.reschedule_count + 1
            new_appointment_dict['original_appointment_id'] = original_appointment.original_appointment_id or original_appointment.appointment_id
            new_appointment_dict['created_at'] = None
            new_appointment_dict['updated_at'] = None
            
            new_appointment = self._to_entity(new_appointment_dict)
            created_appointment = self.create(new_appointment)
            
            # Update original appointment
            original_appointment.status = AppointmentStatus.RESCHEDULED
            original_appointment.cancelled_at = datetime.now()
            original_appointment.cancellation_reason = "Rescheduled"
            
            self.update(original_appointment)
            
            self.logger.info(f"Rescheduled appointment {appointment_id} to {new_start_time}")
            return created_appointment
            
        except Exception as e:
            self.logger.error(f"Failed to reschedule appointment {appointment_id}: {e}")
            return None
    
    def check_availability(self, provider_id: str, start_time: datetime, 
                          duration_minutes: int = 50) -> bool:
        """Check if provider is available for appointment."""
        try:
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            # Check for overlapping appointments
            overlapping_query = f"""
                SELECT COUNT(*) as count
                FROM {self.table_name}
                WHERE provider_id = %(provider_id)s
                AND status NOT IN ('cancelled_by_patient', 'cancelled_by_provider', 'no_show', 'rescheduled')
                AND (
                    (scheduled_start <= %(start_time)s AND scheduled_end > %(start_time)s) OR
                    (scheduled_start < %(end_time)s AND scheduled_end >= %(end_time)s) OR
                    (scheduled_start >= %(start_time)s AND scheduled_end <= %(end_time)s)
                )
            """
            
            params = {
                'provider_id': provider_id,
                'start_time': start_time,
                'end_time': end_time
            }
            
            result = self.db.execute_query(overlapping_query, params)
            overlap_count = result[0]['count'] if result else 0
            
            return overlap_count == 0
            
        except Exception as e:
            self.logger.error(f"Failed to check availability: {e}")
            return False


class AppointmentReminderRepository(BaseRepository[AppointmentReminder, str]):
    """Repository for appointment reminder management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "appointment_reminders", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> AppointmentReminder:
        """Convert database row to AppointmentReminder entity."""
        return AppointmentReminder(
            reminder_id=row.get('reminder_id'),
            appointment_id=row.get('appointment_id'),
            patient_id=row.get('patient_id'),
            reminder_type=ReminderType(row['reminder_type']) if row.get('reminder_type') else ReminderType.EMAIL,
            scheduled_time=row.get('scheduled_time'),
            sent_at=row.get('sent_at'),
            subject=row.get('subject'),
            message=row.get('message', ''),
            delivery_status=row.get('delivery_status', 'pending'),
            delivery_attempts=row.get('delivery_attempts', 0),
            delivery_error=row.get('delivery_error'),
            opened=row.get('opened', False),
            clicked=row.get('clicked', False),
            responded=row.get('responded', False),
            created_at=row.get('created_at')
        )
    
    def _to_dict(self, entity: AppointmentReminder) -> Dict[str, Any]:
        """Convert AppointmentReminder entity to dictionary."""
        return {
            'reminder_id': entity.reminder_id,
            'appointment_id': entity.appointment_id,
            'patient_id': entity.patient_id,
            'reminder_type': entity.reminder_type.value,
            'scheduled_time': entity.scheduled_time,
            'sent_at': entity.sent_at,
            'subject': entity.subject,
            'message': entity.message,
            'delivery_status': entity.delivery_status,
            'delivery_attempts': entity.delivery_attempts,
            'delivery_error': entity.delivery_error,
            'opened': entity.opened,
            'clicked': entity.clicked,
            'responded': entity.responded,
            'created_at': entity.created_at
        }
    
    def _validate_entity(self, entity: AppointmentReminder, is_update: bool = False) -> None:
        """Validate AppointmentReminder entity."""
        if not entity.appointment_id:
            raise ValidationError("Appointment ID is required")
        
        if not entity.patient_id:
            raise ValidationError("Patient ID is required")
        
        if not entity.message:
            raise ValidationError("Reminder message is required")
        
        if entity.delivery_attempts < 0:
            raise ValidationError("Delivery attempts must be non-negative")
        
        if not entity.reminder_id and not is_update:
            import uuid
            entity.reminder_id = str(uuid.uuid4())
    
    def get_pending_reminders(self, reminder_type: ReminderType = None) -> List[AppointmentReminder]:
        """Get pending reminders to send."""
        current_time = datetime.now()
        
        filters = {
            'delivery_status': 'pending',
            'scheduled_time__lte': current_time
        }
        
        if reminder_type:
            filters['reminder_type'] = reminder_type.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['scheduled_time']
        )
        
        result = self.list_all(options)
        return result.data
    
    def mark_sent(self, reminder_id: str, success: bool, error: str = None) -> bool:
        """Mark reminder as sent."""
        try:
            reminder = self.get_by_id(reminder_id)
            if not reminder:
                return False
            
            reminder.delivery_attempts += 1
            reminder.sent_at = datetime.now()
            
            if success:
                reminder.delivery_status = "sent"
            else:
                reminder.delivery_status = "failed"
                reminder.delivery_error = error
            
            self.update(reminder)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to mark reminder as sent: {e}")
            return False
