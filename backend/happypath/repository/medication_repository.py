"""
Medication Management Repository

Repository implementation for medication tracking, adherence monitoring,
and medication management functionality.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, time, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class MedicationStatus(Enum):
    """Medication status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    PAUSED = "paused"
    COMPLETED = "completed"


class MedicationFormulation(Enum):
    """Medication formulation enumeration."""
    TABLET = "tablet"
    CAPSULE = "capsule"
    LIQUID = "liquid"
    INJECTION = "injection"
    PATCH = "patch"
    CREAM = "cream"
    INHALER = "inhaler"
    DROPS = "drops"
    SPRAY = "spray"
    OTHER = "other"


class DosageFrequency(Enum):
    """Dosage frequency enumeration."""
    ONCE_DAILY = "once_daily"
    TWICE_DAILY = "twice_daily"
    THREE_TIMES_DAILY = "three_times_daily"
    FOUR_TIMES_DAILY = "four_times_daily"
    AS_NEEDED = "as_needed"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class AdherenceStatus(Enum):
    """Adherence status enumeration."""
    TAKEN = "taken"
    MISSED = "missed"
    LATE = "late"
    PARTIAL = "partial"
    SKIPPED = "skipped"


@dataclass
class Medication:
    """Medication entity."""
    medication_id: Optional[str] = None
    user_id: Optional[str] = None
    prescribed_by: Optional[str] = None  # Provider ID
    
    # Medication details
    name: str = ""
    generic_name: Optional[str] = None
    brand_name: Optional[str] = None
    ndc_code: Optional[str] = None  # National Drug Code
    
    # Formulation and dosage
    formulation: MedicationFormulation = MedicationFormulation.TABLET
    strength: Optional[str] = None  # e.g., "10mg", "5mg/ml"
    dosage_amount: Optional[Decimal] = None
    dosage_unit: Optional[str] = None  # mg, ml, units, etc.
    
    # Frequency and timing
    frequency: DosageFrequency = DosageFrequency.ONCE_DAILY
    frequency_details: Optional[str] = None  # custom frequency description
    times_per_day: Optional[int] = None
    specific_times: Optional[List[time]] = None  # [08:00, 20:00]
    
    # Administration instructions
    administration_route: Optional[str] = None  # oral, topical, injection, etc.
    instructions: Optional[str] = None
    food_instructions: Optional[str] = None  # take with food, empty stomach, etc.
    
    # Prescription details
    prescribed_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    prescription_number: Optional[str] = None
    pharmacy_info: Optional[Dict[str, Any]] = None
    
    # Status and monitoring
    status: MedicationStatus = MedicationStatus.ACTIVE
    reason_for_prescription: Optional[str] = None
    indication: Optional[str] = None  # condition being treated
    
    # Side effects and monitoring
    common_side_effects: Optional[List[str]] = None
    serious_side_effects: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None
    drug_interactions: Optional[List[str]] = None
    
    # Refill and inventory
    quantity_prescribed: Optional[int] = None
    quantity_remaining: Optional[int] = None
    refills_remaining: Optional[int] = None
    last_refill_date: Optional[date] = None
    next_refill_due: Optional[date] = None
    
    # Cost and insurance
    cost_per_dose: Optional[Decimal] = None
    insurance_coverage: Optional[str] = None
    copay_amount: Optional[Decimal] = None
    
    # Monitoring and alerts
    adherence_target: Optional[Decimal] = None  # target adherence percentage
    low_inventory_threshold: Optional[int] = None
    reminder_enabled: bool = True
    reminder_times: Optional[List[time]] = None
    
    # Clinical notes
    prescriber_notes: Optional[str] = None
    patient_notes: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class MedicationDose:
    """Medication dose entity."""
    dose_id: Optional[str] = None
    medication_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Dose details
    scheduled_time: Optional[datetime] = None
    actual_time: Optional[datetime] = None
    amount_taken: Optional[Decimal] = None
    amount_prescribed: Optional[Decimal] = None
    
    # Status
    adherence_status: AdherenceStatus = AdherenceStatus.TAKEN
    
    # Context
    taken_with_food: Optional[bool] = None
    notes: Optional[str] = None
    side_effects_experienced: Optional[List[str]] = None
    mood_before: Optional[int] = None  # 1-10 scale
    mood_after: Optional[int] = None
    
    # Tracking method
    recorded_by: str = "patient"  # patient, caregiver, system
    verification_method: Optional[str] = None  # self_report, photo, smart_pill, etc.
    
    # Reminders
    reminder_sent: bool = False
    reminder_acknowledged: bool = False
    late_threshold_minutes: int = 30
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class MedicationAdherence:
    """Medication adherence summary entity."""
    adherence_id: Optional[str] = None
    medication_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Time period
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    period_type: str = "weekly"  # daily, weekly, monthly, custom
    
    # Adherence metrics
    total_doses_scheduled: int = 0
    total_doses_taken: int = 0
    doses_taken_on_time: int = 0
    doses_taken_late: int = 0
    doses_missed: int = 0
    doses_skipped: int = 0
    
    # Calculated percentages
    adherence_percentage: Optional[Decimal] = None
    on_time_percentage: Optional[Decimal] = None
    
    # Timing analysis
    average_delay_minutes: Optional[Decimal] = None
    longest_gap_hours: Optional[Decimal] = None
    
    # Patterns
    missed_dose_patterns: Optional[List[str]] = None  # weekend, morning, evening
    adherence_trend: Optional[str] = None  # improving, declining, stable
    
    # Clinical correlation
    mood_correlation: Optional[Decimal] = None
    side_effect_correlation: Optional[Decimal] = None
    
    created_at: Optional[datetime] = None


@dataclass
class MedicationReminder:
    """Medication reminder entity."""
    reminder_id: Optional[str] = None
    medication_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Reminder scheduling
    scheduled_time: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    
    # Reminder content
    message: str = ""
    reminder_type: str = "dose"  # dose, refill, appointment, lab_work
    
    # Delivery settings
    delivery_methods: Optional[List[str]] = None  # push, email, sms, phone
    delivery_status: str = "pending"  # pending, sent, delivered, failed
    delivery_attempts: int = 0
    
    # Escalation
    escalation_enabled: bool = False
    escalation_delay_minutes: int = 15
    escalation_contacts: Optional[List[str]] = None
    
    # Response tracking
    responded: bool = False
    response_time_minutes: Optional[int] = None
    
    created_at: Optional[datetime] = None


class MedicationRepository(BaseRepository[Medication, str]):
    """Repository for medication management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "medications", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> Medication:
        """Convert database row to Medication entity."""
        return Medication(
            medication_id=row.get('medication_id'),
            user_id=row.get('user_id'),
            prescribed_by=row.get('prescribed_by'),
            name=row.get('name', ''),
            generic_name=row.get('generic_name'),
            brand_name=row.get('brand_name'),
            ndc_code=row.get('ndc_code'),
            formulation=MedicationFormulation(row['formulation']) if row.get('formulation') else MedicationFormulation.TABLET,
            strength=row.get('strength'),
            dosage_amount=Decimal(str(row['dosage_amount'])) if row.get('dosage_amount') else None,
            dosage_unit=row.get('dosage_unit'),
            frequency=DosageFrequency(row['frequency']) if row.get('frequency') else DosageFrequency.ONCE_DAILY,
            frequency_details=row.get('frequency_details'),
            times_per_day=row.get('times_per_day'),
            specific_times=row.get('specific_times', []),
            administration_route=row.get('administration_route'),
            instructions=row.get('instructions'),
            food_instructions=row.get('food_instructions'),
            prescribed_date=row.get('prescribed_date'),
            start_date=row.get('start_date'),
            end_date=row.get('end_date'),
            prescription_number=row.get('prescription_number'),
            pharmacy_info=row.get('pharmacy_info'),
            status=MedicationStatus(row['status']) if row.get('status') else MedicationStatus.ACTIVE,
            reason_for_prescription=row.get('reason_for_prescription'),
            indication=row.get('indication'),
            common_side_effects=row.get('common_side_effects', []),
            serious_side_effects=row.get('serious_side_effects', []),
            contraindications=row.get('contraindications', []),
            drug_interactions=row.get('drug_interactions', []),
            quantity_prescribed=row.get('quantity_prescribed'),
            quantity_remaining=row.get('quantity_remaining'),
            refills_remaining=row.get('refills_remaining'),
            last_refill_date=row.get('last_refill_date'),
            next_refill_due=row.get('next_refill_due'),
            cost_per_dose=Decimal(str(row['cost_per_dose'])) if row.get('cost_per_dose') else None,
            insurance_coverage=row.get('insurance_coverage'),
            copay_amount=Decimal(str(row['copay_amount'])) if row.get('copay_amount') else None,
            adherence_target=Decimal(str(row['adherence_target'])) if row.get('adherence_target') else None,
            low_inventory_threshold=row.get('low_inventory_threshold'),
            reminder_enabled=row.get('reminder_enabled', True),
            reminder_times=row.get('reminder_times', []),
            prescriber_notes=row.get('prescriber_notes'),
            patient_notes=row.get('patient_notes'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: Medication) -> Dict[str, Any]:
        """Convert Medication entity to dictionary."""
        return {
            'medication_id': entity.medication_id,
            'user_id': entity.user_id,
            'prescribed_by': entity.prescribed_by,
            'name': entity.name,
            'generic_name': entity.generic_name,
            'brand_name': entity.brand_name,
            'ndc_code': entity.ndc_code,
            'formulation': entity.formulation.value,
            'strength': entity.strength,
            'dosage_amount': entity.dosage_amount,
            'dosage_unit': entity.dosage_unit,
            'frequency': entity.frequency.value,
            'frequency_details': entity.frequency_details,
            'times_per_day': entity.times_per_day,
            'specific_times': entity.specific_times,
            'administration_route': entity.administration_route,
            'instructions': entity.instructions,
            'food_instructions': entity.food_instructions,
            'prescribed_date': entity.prescribed_date,
            'start_date': entity.start_date,
            'end_date': entity.end_date,
            'prescription_number': entity.prescription_number,
            'pharmacy_info': entity.pharmacy_info,
            'status': entity.status.value,
            'reason_for_prescription': entity.reason_for_prescription,
            'indication': entity.indication,
            'common_side_effects': entity.common_side_effects,
            'serious_side_effects': entity.serious_side_effects,
            'contraindications': entity.contraindications,
            'drug_interactions': entity.drug_interactions,
            'quantity_prescribed': entity.quantity_prescribed,
            'quantity_remaining': entity.quantity_remaining,
            'refills_remaining': entity.refills_remaining,
            'last_refill_date': entity.last_refill_date,
            'next_refill_due': entity.next_refill_due,
            'cost_per_dose': entity.cost_per_dose,
            'insurance_coverage': entity.insurance_coverage,
            'copay_amount': entity.copay_amount,
            'adherence_target': entity.adherence_target,
            'low_inventory_threshold': entity.low_inventory_threshold,
            'reminder_enabled': entity.reminder_enabled,
            'reminder_times': entity.reminder_times,
            'prescriber_notes': entity.prescriber_notes,
            'patient_notes': entity.patient_notes,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: Medication, is_update: bool = False) -> None:
        """Validate Medication entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.name:
            raise ValidationError("Medication name is required")
        
        if entity.dosage_amount and entity.dosage_amount <= 0:
            raise ValidationError("Dosage amount must be positive")
        
        if entity.times_per_day and entity.times_per_day <= 0:
            raise ValidationError("Times per day must be positive")
        
        if entity.quantity_prescribed and entity.quantity_prescribed <= 0:
            raise ValidationError("Quantity prescribed must be positive")
        
        if entity.quantity_remaining and entity.quantity_remaining < 0:
            raise ValidationError("Quantity remaining cannot be negative")
        
        if entity.refills_remaining and entity.refills_remaining < 0:
            raise ValidationError("Refills remaining cannot be negative")
        
        if entity.adherence_target and (entity.adherence_target < 0 or entity.adherence_target > 100):
            raise ValidationError("Adherence target must be between 0 and 100")
        
        if not entity.start_date:
            entity.start_date = date.today()
        
        if not entity.medication_id and not is_update:
            import uuid
            entity.medication_id = str(uuid.uuid4())
    
    def get_user_medications(self, user_id: str, active_only: bool = True) -> List[Medication]:
        """Get medications for a user."""
        filters = {'user_id': user_id}
        if active_only:
            filters['status'] = MedicationStatus.ACTIVE.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['-start_date', 'name']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_medications_due_for_refill(self, days_ahead: int = 7) -> List[Medication]:
        """Get medications that need refills soon."""
        refill_date = date.today() + timedelta(days=days_ahead)
        
        options = QueryOptions(
            filters={
                'status': MedicationStatus.ACTIVE.value,
                'next_refill_due__lte': refill_date
            },
            order_by=['next_refill_due']
        )
        
        result = self.list_all(options)
        return result.data
    
    def update_inventory(self, medication_id: str, quantity_change: int, 
                        refill: bool = False) -> bool:
        """Update medication inventory."""
        try:
            medication = self.get_by_id(medication_id)
            if not medication:
                return False
            
            if refill:
                # Refill - add to inventory
                medication.quantity_remaining = (medication.quantity_remaining or 0) + quantity_change
                medication.last_refill_date = date.today()
                
                # Calculate next refill date (estimate based on daily usage)
                if medication.times_per_day and medication.quantity_remaining:
                    days_supply = medication.quantity_remaining / medication.times_per_day
                    medication.next_refill_due = date.today() + timedelta(days=int(days_supply * 0.8))  # 80% threshold
            else:
                # Dose taken - subtract from inventory
                medication.quantity_remaining = max(0, (medication.quantity_remaining or 0) - abs(quantity_change))
            
            self.update(medication)
            
            self.logger.info(f"Updated inventory for medication {medication_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update medication inventory: {e}")
            return False
    
    def discontinue_medication(self, medication_id: str, reason: str) -> bool:
        """Discontinue a medication."""
        try:
            medication = self.get_by_id(medication_id)
            if not medication:
                return False
            
            medication.status = MedicationStatus.DISCONTINUED
            medication.end_date = date.today()
            medication.prescriber_notes = f"{medication.prescriber_notes or ''}\nDiscontinued: {reason}".strip()
            
            self.update(medication)
            
            self.logger.info(f"Discontinued medication {medication_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to discontinue medication: {e}")
            return False


class MedicationDoseRepository(BaseRepository[MedicationDose, str]):
    """Repository for medication dose tracking."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "medication_doses", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> MedicationDose:
        """Convert database row to MedicationDose entity."""
        return MedicationDose(
            dose_id=row.get('dose_id'),
            medication_id=row.get('medication_id'),
            user_id=row.get('user_id'),
            scheduled_time=row.get('scheduled_time'),
            actual_time=row.get('actual_time'),
            amount_taken=Decimal(str(row['amount_taken'])) if row.get('amount_taken') else None,
            amount_prescribed=Decimal(str(row['amount_prescribed'])) if row.get('amount_prescribed') else None,
            adherence_status=AdherenceStatus(row['adherence_status']) if row.get('adherence_status') else AdherenceStatus.TAKEN,
            taken_with_food=row.get('taken_with_food'),
            notes=row.get('notes'),
            side_effects_experienced=row.get('side_effects_experienced', []),
            mood_before=row.get('mood_before'),
            mood_after=row.get('mood_after'),
            recorded_by=row.get('recorded_by', 'patient'),
            verification_method=row.get('verification_method'),
            reminder_sent=row.get('reminder_sent', False),
            reminder_acknowledged=row.get('reminder_acknowledged', False),
            late_threshold_minutes=row.get('late_threshold_minutes', 30),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: MedicationDose) -> Dict[str, Any]:
        """Convert MedicationDose entity to dictionary."""
        return {
            'dose_id': entity.dose_id,
            'medication_id': entity.medication_id,
            'user_id': entity.user_id,
            'scheduled_time': entity.scheduled_time,
            'actual_time': entity.actual_time,
            'amount_taken': entity.amount_taken,
            'amount_prescribed': entity.amount_prescribed,
            'adherence_status': entity.adherence_status.value,
            'taken_with_food': entity.taken_with_food,
            'notes': entity.notes,
            'side_effects_experienced': entity.side_effects_experienced,
            'mood_before': entity.mood_before,
            'mood_after': entity.mood_after,
            'recorded_by': entity.recorded_by,
            'verification_method': entity.verification_method,
            'reminder_sent': entity.reminder_sent,
            'reminder_acknowledged': entity.reminder_acknowledged,
            'late_threshold_minutes': entity.late_threshold_minutes,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: MedicationDose, is_update: bool = False) -> None:
        """Validate MedicationDose entity."""
        if not entity.medication_id:
            raise ValidationError("Medication ID is required")
        
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if entity.amount_taken and entity.amount_taken < 0:
            raise ValidationError("Amount taken cannot be negative")
        
        if entity.amount_prescribed and entity.amount_prescribed <= 0:
            raise ValidationError("Amount prescribed must be positive")
        
        if entity.mood_before and (entity.mood_before < 1 or entity.mood_before > 10):
            raise ValidationError("Mood before must be between 1 and 10")
        
        if entity.mood_after and (entity.mood_after < 1 or entity.mood_after > 10):
            raise ValidationError("Mood after must be between 1 and 10")
        
        if entity.late_threshold_minutes < 0:
            raise ValidationError("Late threshold must be non-negative")
        
        if not entity.dose_id and not is_update:
            import uuid
            entity.dose_id = str(uuid.uuid4())
    
    def record_dose_taken(self, medication_id: str, user_id: str, 
                         scheduled_time: datetime, actual_time: datetime = None,
                         amount_taken: Decimal = None, notes: str = None) -> MedicationDose:
        """Record a medication dose as taken."""
        if not actual_time:
            actual_time = datetime.now()
        
        # Determine adherence status based on timing
        time_diff = actual_time - scheduled_time
        minutes_late = time_diff.total_seconds() / 60
        
        if minutes_late <= 30:  # Within 30 minutes
            status = AdherenceStatus.TAKEN
        elif minutes_late <= 120:  # Within 2 hours
            status = AdherenceStatus.LATE
        else:
            status = AdherenceStatus.LATE
        
        dose = MedicationDose(
            medication_id=medication_id,
            user_id=user_id,
            scheduled_time=scheduled_time,
            actual_time=actual_time,
            amount_taken=amount_taken,
            adherence_status=status,
            notes=notes
        )
        
        return self.create(dose)
    
    def get_medication_doses(self, medication_id: str, start_date: date = None,
                           end_date: date = None) -> List[MedicationDose]:
        """Get doses for a medication."""
        filters = {'medication_id': medication_id}
        
        if start_date:
            filters['scheduled_time__gte'] = datetime.combine(start_date, datetime.min.time())
        if end_date:
            filters['scheduled_time__lte'] = datetime.combine(end_date, datetime.max.time())
        
        options = QueryOptions(
            filters=filters,
            order_by=['-scheduled_time']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_missed_doses(self, user_id: str, hours_overdue: int = 2) -> List[MedicationDose]:
        """Get missed doses that are overdue."""
        cutoff_time = datetime.now() - timedelta(hours=hours_overdue)
        
        options = QueryOptions(
            filters={
                'user_id': user_id,
                'scheduled_time__lte': cutoff_time,
                'adherence_status': AdherenceStatus.MISSED.value
            },
            order_by=['scheduled_time']
        )
        
        result = self.list_all(options)
        return result.data


class MedicationAdherenceRepository(BaseRepository[MedicationAdherence, str]):
    """Repository for medication adherence analysis."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "medication_adherence", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> MedicationAdherence:
        """Convert database row to MedicationAdherence entity."""
        return MedicationAdherence(
            adherence_id=row.get('adherence_id'),
            medication_id=row.get('medication_id'),
            user_id=row.get('user_id'),
            period_start=row.get('period_start'),
            period_end=row.get('period_end'),
            period_type=row.get('period_type', 'weekly'),
            total_doses_scheduled=row.get('total_doses_scheduled', 0),
            total_doses_taken=row.get('total_doses_taken', 0),
            doses_taken_on_time=row.get('doses_taken_on_time', 0),
            doses_taken_late=row.get('doses_taken_late', 0),
            doses_missed=row.get('doses_missed', 0),
            doses_skipped=row.get('doses_skipped', 0),
            adherence_percentage=Decimal(str(row['adherence_percentage'])) if row.get('adherence_percentage') else None,
            on_time_percentage=Decimal(str(row['on_time_percentage'])) if row.get('on_time_percentage') else None,
            average_delay_minutes=Decimal(str(row['average_delay_minutes'])) if row.get('average_delay_minutes') else None,
            longest_gap_hours=Decimal(str(row['longest_gap_hours'])) if row.get('longest_gap_hours') else None,
            missed_dose_patterns=row.get('missed_dose_patterns', []),
            adherence_trend=row.get('adherence_trend'),
            mood_correlation=Decimal(str(row['mood_correlation'])) if row.get('mood_correlation') else None,
            side_effect_correlation=Decimal(str(row['side_effect_correlation'])) if row.get('side_effect_correlation') else None,
            created_at=row.get('created_at')
        )
    
    def _to_dict(self, entity: MedicationAdherence) -> Dict[str, Any]:
        """Convert MedicationAdherence entity to dictionary."""
        return {
            'adherence_id': entity.adherence_id,
            'medication_id': entity.medication_id,
            'user_id': entity.user_id,
            'period_start': entity.period_start,
            'period_end': entity.period_end,
            'period_type': entity.period_type,
            'total_doses_scheduled': entity.total_doses_scheduled,
            'total_doses_taken': entity.total_doses_taken,
            'doses_taken_on_time': entity.doses_taken_on_time,
            'doses_taken_late': entity.doses_taken_late,
            'doses_missed': entity.doses_missed,
            'doses_skipped': entity.doses_skipped,
            'adherence_percentage': entity.adherence_percentage,
            'on_time_percentage': entity.on_time_percentage,
            'average_delay_minutes': entity.average_delay_minutes,
            'longest_gap_hours': entity.longest_gap_hours,
            'missed_dose_patterns': entity.missed_dose_patterns,
            'adherence_trend': entity.adherence_trend,
            'mood_correlation': entity.mood_correlation,
            'side_effect_correlation': entity.side_effect_correlation,
            'created_at': entity.created_at
        }
    
    def _validate_entity(self, entity: MedicationAdherence, is_update: bool = False) -> None:
        """Validate MedicationAdherence entity."""
        if not entity.medication_id:
            raise ValidationError("Medication ID is required")
        
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if entity.total_doses_scheduled < 0:
            raise ValidationError("Total doses scheduled cannot be negative")
        
        if entity.total_doses_taken > entity.total_doses_scheduled:
            raise ValidationError("Doses taken cannot exceed scheduled")
        
        if entity.adherence_percentage and (entity.adherence_percentage < 0 or entity.adherence_percentage > 100):
            raise ValidationError("Adherence percentage must be between 0 and 100")
        
        if not entity.adherence_id and not is_update:
            import uuid
            entity.adherence_id = str(uuid.uuid4())
    
    def calculate_adherence(self, medication_id: str, start_date: date, 
                          end_date: date) -> MedicationAdherence:
        """Calculate adherence metrics for a medication over a period."""
        try:
            # Get all scheduled doses in the period
            dose_repo = MedicationDoseRepository(self.db, self.logger)
            doses = dose_repo.get_medication_doses(medication_id, start_date, end_date)
            
            total_scheduled = len(doses)
            taken = len([d for d in doses if d.adherence_status == AdherenceStatus.TAKEN])
            late = len([d for d in doses if d.adherence_status == AdherenceStatus.LATE])
            missed = len([d for d in doses if d.adherence_status == AdherenceStatus.MISSED])
            skipped = len([d for d in doses if d.adherence_status == AdherenceStatus.SKIPPED])
            
            total_taken = taken + late
            
            # Calculate percentages
            adherence_pct = (total_taken / total_scheduled * 100) if total_scheduled > 0 else 0
            on_time_pct = (taken / total_scheduled * 100) if total_scheduled > 0 else 0
            
            # Calculate average delay for late doses
            late_doses = [d for d in doses if d.adherence_status == AdherenceStatus.LATE and d.actual_time and d.scheduled_time]
            avg_delay = None
            if late_doses:
                total_delay = sum((d.actual_time - d.scheduled_time).total_seconds() / 60 for d in late_doses)
                avg_delay = Decimal(str(total_delay / len(late_doses)))
            
            adherence = MedicationAdherence(
                medication_id=medication_id,
                user_id=doses[0].user_id if doses else None,
                period_start=start_date,
                period_end=end_date,
                period_type="custom",
                total_doses_scheduled=total_scheduled,
                total_doses_taken=total_taken,
                doses_taken_on_time=taken,
                doses_taken_late=late,
                doses_missed=missed,
                doses_skipped=skipped,
                adherence_percentage=Decimal(str(round(adherence_pct, 2))),
                on_time_percentage=Decimal(str(round(on_time_pct, 2))),
                average_delay_minutes=avg_delay
            )
            
            return self.create(adherence)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate adherence: {e}")
            raise
