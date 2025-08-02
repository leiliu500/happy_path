"""
Mood Tracking Repository

Repository implementation for mood tracking, patterns analysis,
and mood-related goal management.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class MoodScale(Enum):
    """Mood scale enumeration (1-10)."""
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"


class AnxietyLevel(Enum):
    """Anxiety level enumeration."""
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"


class EnergyLevel(Enum):
    """Energy level enumeration."""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class SleepQuality(Enum):
    """Sleep quality enumeration."""
    VERY_POOR = "very_poor"
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


class StressLevel(Enum):
    """Stress level enumeration."""
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    OVERWHELMING = "overwhelming"


@dataclass
class MoodEntry:
    """Mood entry entity."""
    entry_id: Optional[str] = None
    user_id: Optional[str] = None
    entry_date: Optional[date] = None
    entry_time: Optional[datetime] = None
    
    # Core mood metrics
    overall_mood: Optional[MoodScale] = None
    anxiety_level: Optional[AnxietyLevel] = None
    stress_level: Optional[StressLevel] = None
    energy_level: Optional[EnergyLevel] = None
    sleep_quality: Optional[SleepQuality] = None
    sleep_hours: Optional[Decimal] = None
    
    # Additional metrics
    medication_taken: Optional[bool] = None
    medication_notes: Optional[str] = None
    exercise_minutes: int = 0
    social_interaction_quality: Optional[MoodScale] = None
    productivity_level: Optional[MoodScale] = None
    
    # Emotional state tags
    emotions: Optional[List[str]] = None
    triggers: Optional[List[str]] = None
    coping_strategies: Optional[List[str]] = None
    
    # Contextual information
    weather: Optional[str] = None
    location_type: Optional[str] = None
    
    # Free text for additional context
    notes: Optional[str] = None
    gratitude_note: Optional[str] = None
    
    # Goal tracking
    daily_goals_met: int = 0
    daily_goals_total: int = 0
    
    # Metadata
    data_source: str = "manual"  # manual, wearable, ai_prompt
    confidence_score: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def mood_improvement(self) -> Optional[bool]:
        """Check if mood improved from previous entry."""
        # This would require comparison with previous entry
        return None


@dataclass
class MoodPattern:
    """Mood pattern entity."""
    pattern_id: Optional[str] = None
    user_id: Optional[str] = None
    pattern_type: str = ""  # weekly, monthly, seasonal, trigger_based
    pattern_name: str = ""
    description: Optional[str] = None
    
    # Pattern metrics
    average_mood: Optional[Decimal] = None
    mood_variance: Optional[Decimal] = None
    trend_direction: Optional[str] = None  # improving, declining, stable, volatile
    
    # Time-based patterns
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days_of_week: Optional[List[int]] = None  # [1,2,3,4,5] for weekdays
    time_of_day_start: Optional[datetime] = None
    time_of_day_end: Optional[datetime] = None
    
    # Pattern triggers and correlations
    common_triggers: Optional[List[str]] = None
    common_emotions: Optional[List[str]] = None
    effective_coping_strategies: Optional[List[str]] = None
    
    # Statistical data
    sample_size: int = 0
    confidence_level: Optional[Decimal] = None
    
    # Metadata
    detected_by: str = "ai_analysis"  # ai_analysis, manual, therapist
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class MoodGoal:
    """Mood goal entity."""
    goal_id: Optional[str] = None
    user_id: Optional[str] = None
    goal_type: str = ""  # mood_stability, anxiety_reduction, sleep_improvement
    goal_name: str = ""
    description: Optional[str] = None
    
    # Goal metrics
    target_metric: str = ""  # overall_mood, anxiety_level, sleep_hours
    target_value: Decimal = Decimal('0')
    target_operator: str = ">="  # >=, <=, =, between
    target_frequency: Optional[str] = None  # daily, weekly, 5_days_per_week
    
    # Time frame
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    
    # Progress tracking
    current_streak: int = 0
    best_streak: int = 0
    total_successes: int = 0
    total_attempts: int = 0
    
    # Metadata
    created_by: Optional[str] = None  # therapist or self
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_attempts == 0:
            return 0.0
        return self.total_successes / self.total_attempts


@dataclass
class MoodAnalytics:
    """Mood analytics data."""
    user_id: str
    period_start: date
    period_end: date
    
    # Basic statistics
    total_entries: int
    average_mood: Optional[Decimal]
    mood_variance: Optional[Decimal]
    trend_direction: Optional[str]
    
    # Correlations
    sleep_mood_correlation: Optional[Decimal]
    exercise_mood_correlation: Optional[Decimal]
    
    # Common patterns
    best_days_of_week: List[str]
    worst_days_of_week: List[str]
    common_triggers: List[str]
    effective_strategies: List[str]
    
    # Goal progress
    active_goals: int
    goals_met: int
    goal_success_rate: float


class MoodEntryRepository(BaseRepository[MoodEntry, str]):
    """Repository for mood entry management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "mood_entries", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> MoodEntry:
        """Convert database row to MoodEntry entity."""
        return MoodEntry(
            entry_id=row.get('entry_id'),
            user_id=row.get('user_id'),
            entry_date=row.get('entry_date'),
            entry_time=row.get('entry_time'),
            overall_mood=MoodScale(row['overall_mood']) if row.get('overall_mood') else None,
            anxiety_level=AnxietyLevel(row['anxiety_level']) if row.get('anxiety_level') else None,
            stress_level=StressLevel(row['stress_level']) if row.get('stress_level') else None,
            energy_level=EnergyLevel(row['energy_level']) if row.get('energy_level') else None,
            sleep_quality=SleepQuality(row['sleep_quality']) if row.get('sleep_quality') else None,
            sleep_hours=Decimal(str(row['sleep_hours'])) if row.get('sleep_hours') else None,
            medication_taken=row.get('medication_taken'),
            medication_notes=row.get('medication_notes'),
            exercise_minutes=row.get('exercise_minutes', 0),
            social_interaction_quality=MoodScale(row['social_interaction_quality']) if row.get('social_interaction_quality') else None,
            productivity_level=MoodScale(row['productivity_level']) if row.get('productivity_level') else None,
            emotions=row.get('emotions', []),
            triggers=row.get('triggers', []),
            coping_strategies=row.get('coping_strategies', []),
            weather=row.get('weather'),
            location_type=row.get('location_type'),
            notes=row.get('notes'),
            gratitude_note=row.get('gratitude_note'),
            daily_goals_met=row.get('daily_goals_met', 0),
            daily_goals_total=row.get('daily_goals_total', 0),
            data_source=row.get('data_source', 'manual'),
            confidence_score=Decimal(str(row['confidence_score'])) if row.get('confidence_score') else None,
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: MoodEntry) -> Dict[str, Any]:
        """Convert MoodEntry entity to dictionary."""
        return {
            'entry_id': entity.entry_id,
            'user_id': entity.user_id,
            'entry_date': entity.entry_date,
            'entry_time': entity.entry_time,
            'overall_mood': entity.overall_mood.value if entity.overall_mood else None,
            'anxiety_level': entity.anxiety_level.value if entity.anxiety_level else None,
            'stress_level': entity.stress_level.value if entity.stress_level else None,
            'energy_level': entity.energy_level.value if entity.energy_level else None,
            'sleep_quality': entity.sleep_quality.value if entity.sleep_quality else None,
            'sleep_hours': entity.sleep_hours,
            'medication_taken': entity.medication_taken,
            'medication_notes': entity.medication_notes,
            'exercise_minutes': entity.exercise_minutes,
            'social_interaction_quality': entity.social_interaction_quality.value if entity.social_interaction_quality else None,
            'productivity_level': entity.productivity_level.value if entity.productivity_level else None,
            'emotions': entity.emotions,
            'triggers': entity.triggers,
            'coping_strategies': entity.coping_strategies,
            'weather': entity.weather,
            'location_type': entity.location_type,
            'notes': entity.notes,
            'gratitude_note': entity.gratitude_note,
            'daily_goals_met': entity.daily_goals_met,
            'daily_goals_total': entity.daily_goals_total,
            'data_source': entity.data_source,
            'confidence_score': entity.confidence_score,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: MoodEntry, is_update: bool = False) -> None:
        """Validate MoodEntry entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.overall_mood:
            raise ValidationError("Overall mood is required")
        
        if not entity.entry_date:
            entity.entry_date = date.today()
        
        if not entity.entry_time:
            entity.entry_time = datetime.now()
        
        if entity.sleep_hours and (entity.sleep_hours < 0 or entity.sleep_hours > 24):
            raise ValidationError("Sleep hours must be between 0 and 24")
        
        if entity.exercise_minutes < 0 or entity.exercise_minutes > 1440:
            raise ValidationError("Exercise minutes must be between 0 and 1440")
        
        if entity.daily_goals_met > entity.daily_goals_total:
            raise ValidationError("Goals met cannot exceed total goals")
        
        if entity.confidence_score and (entity.confidence_score < 0 or entity.confidence_score > 1):
            raise ValidationError("Confidence score must be between 0 and 1")
        
        if not entity.entry_id and not is_update:
            import uuid
            entity.entry_id = str(uuid.uuid4())
    
    def get_user_entries(self, user_id: str, start_date: date = None, 
                        end_date: date = None, limit: Optional[int] = None) -> List[MoodEntry]:
        """Get mood entries for a user within date range."""
        filters = {'user_id': user_id}
        
        if start_date:
            filters['entry_date__gte'] = start_date
        if end_date:
            filters['entry_date__lte'] = end_date
        
        options = QueryOptions(
            filters=filters,
            order_by=['-entry_date', '-entry_time'],
            limit=limit
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_daily_entry(self, user_id: str, entry_date: date) -> Optional[MoodEntry]:
        """Get mood entry for a specific date."""
        return self.find_one_by(user_id=user_id, entry_date=entry_date)
    
    def get_recent_entries(self, user_id: str, days: int = 7) -> List[MoodEntry]:
        """Get recent mood entries for a user."""
        start_date = date.today() - timedelta(days=days)
        return self.get_user_entries(user_id, start_date)
    
    def calculate_mood_trends(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Calculate mood trends over specified period."""
        try:
            start_date = date.today() - timedelta(days=days)
            entries = self.get_user_entries(user_id, start_date)
            
            if not entries:
                return {}
            
            # Convert mood values to integers for calculation
            mood_values = [int(entry.overall_mood.value) for entry in entries if entry.overall_mood]
            
            if not mood_values:
                return {}
            
            average_mood = sum(mood_values) / len(mood_values)
            
            # Calculate trend (simple linear regression)
            x_values = list(range(len(mood_values)))
            if len(x_values) > 1:
                x_mean = sum(x_values) / len(x_values)
                y_mean = average_mood
                
                numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, mood_values))
                denominator = sum((x - x_mean) ** 2 for x in x_values)
                
                slope = numerator / denominator if denominator != 0 else 0
                
                if slope > 0.1:
                    trend = "improving"
                elif slope < -0.1:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            return {
                'average_mood': round(average_mood, 2),
                'trend_direction': trend,
                'trend_slope': round(slope, 3) if len(x_values) > 1 else 0,
                'total_entries': len(entries),
                'period_days': days
            }
            
        except Exception as e:
            self.logger.error(f"Failed to calculate mood trends: {e}")
            return {}
    
    def find_mood_correlations(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Find correlations between mood and other factors."""
        try:
            start_date = date.today() - timedelta(days=days)
            entries = self.get_user_entries(user_id, start_date)
            
            if not entries:
                return {}
            
            mood_values = []
            sleep_values = []
            exercise_values = []
            
            for entry in entries:
                if entry.overall_mood:
                    mood_values.append(int(entry.overall_mood.value))
                    sleep_values.append(float(entry.sleep_hours) if entry.sleep_hours else 0)
                    exercise_values.append(entry.exercise_minutes)
            
            correlations = {}
            
            # Calculate sleep-mood correlation
            if len(mood_values) > 2:
                sleep_corr = self._calculate_correlation(mood_values, sleep_values)
                exercise_corr = self._calculate_correlation(mood_values, exercise_values)
                
                correlations = {
                    'sleep_mood_correlation': round(sleep_corr, 3),
                    'exercise_mood_correlation': round(exercise_corr, 3)
                }
            
            return correlations
            
        except Exception as e:
            self.logger.error(f"Failed to find mood correlations: {e}")
            return {}
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        x_var = sum((x[i] - x_mean) ** 2 for i in range(n))
        y_var = sum((y[i] - y_mean) ** 2 for i in range(n))
        
        denominator = (x_var * y_var) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0.0


class MoodPatternRepository(BaseRepository[MoodPattern, str]):
    """Repository for mood pattern management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "mood_patterns", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> MoodPattern:
        """Convert database row to MoodPattern entity."""
        return MoodPattern(
            pattern_id=row.get('pattern_id'),
            user_id=row.get('user_id'),
            pattern_type=row.get('pattern_type', ''),
            pattern_name=row.get('pattern_name', ''),
            description=row.get('description'),
            average_mood=Decimal(str(row['average_mood'])) if row.get('average_mood') else None,
            mood_variance=Decimal(str(row['mood_variance'])) if row.get('mood_variance') else None,
            trend_direction=row.get('trend_direction'),
            start_date=row.get('start_date'),
            end_date=row.get('end_date'),
            days_of_week=row.get('days_of_week', []),
            time_of_day_start=row.get('time_of_day_start'),
            time_of_day_end=row.get('time_of_day_end'),
            common_triggers=row.get('common_triggers', []),
            common_emotions=row.get('common_emotions', []),
            effective_coping_strategies=row.get('effective_coping_strategies', []),
            sample_size=row.get('sample_size', 0),
            confidence_level=Decimal(str(row['confidence_level'])) if row.get('confidence_level') else None,
            detected_by=row.get('detected_by', 'ai_analysis'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: MoodPattern) -> Dict[str, Any]:
        """Convert MoodPattern entity to dictionary."""
        return {
            'pattern_id': entity.pattern_id,
            'user_id': entity.user_id,
            'pattern_type': entity.pattern_type,
            'pattern_name': entity.pattern_name,
            'description': entity.description,
            'average_mood': entity.average_mood,
            'mood_variance': entity.mood_variance,
            'trend_direction': entity.trend_direction,
            'start_date': entity.start_date,
            'end_date': entity.end_date,
            'days_of_week': entity.days_of_week,
            'time_of_day_start': entity.time_of_day_start,
            'time_of_day_end': entity.time_of_day_end,
            'common_triggers': entity.common_triggers,
            'common_emotions': entity.common_emotions,
            'effective_coping_strategies': entity.effective_coping_strategies,
            'sample_size': entity.sample_size,
            'confidence_level': entity.confidence_level,
            'detected_by': entity.detected_by,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: MoodPattern, is_update: bool = False) -> None:
        """Validate MoodPattern entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.pattern_type:
            raise ValidationError("Pattern type is required")
        
        if not entity.pattern_name:
            raise ValidationError("Pattern name is required")
        
        if entity.average_mood and (entity.average_mood < 1 or entity.average_mood > 10):
            raise ValidationError("Average mood must be between 1 and 10")
        
        if entity.sample_size < 0:
            raise ValidationError("Sample size must be non-negative")
        
        if entity.end_date and entity.start_date and entity.end_date < entity.start_date:
            raise ValidationError("End date cannot be before start date")
        
        if not entity.pattern_id and not is_update:
            import uuid
            entity.pattern_id = str(uuid.uuid4())
    
    def get_user_patterns(self, user_id: str) -> List[MoodPattern]:
        """Get mood patterns for a user."""
        options = QueryOptions(
            filters={'user_id': user_id},
            order_by=['-confidence_level', '-created_at']
        )
        
        result = self.list_all(options)
        return result.data


class MoodGoalRepository(BaseRepository[MoodGoal, str]):
    """Repository for mood goal management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "mood_goals", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> MoodGoal:
        """Convert database row to MoodGoal entity."""
        return MoodGoal(
            goal_id=row.get('goal_id'),
            user_id=row.get('user_id'),
            goal_type=row.get('goal_type', ''),
            goal_name=row.get('goal_name', ''),
            description=row.get('description'),
            target_metric=row.get('target_metric', ''),
            target_value=Decimal(str(row['target_value'])) if row.get('target_value') else Decimal('0'),
            target_operator=row.get('target_operator', '>='),
            target_frequency=row.get('target_frequency'),
            start_date=row.get('start_date'),
            end_date=row.get('end_date'),
            is_active=row.get('is_active', True),
            current_streak=row.get('current_streak', 0),
            best_streak=row.get('best_streak', 0),
            total_successes=row.get('total_successes', 0),
            total_attempts=row.get('total_attempts', 0),
            created_by=row.get('created_by'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at'),
            completed_at=row.get('completed_at')
        )
    
    def _to_dict(self, entity: MoodGoal) -> Dict[str, Any]:
        """Convert MoodGoal entity to dictionary."""
        return {
            'goal_id': entity.goal_id,
            'user_id': entity.user_id,
            'goal_type': entity.goal_type,
            'goal_name': entity.goal_name,
            'description': entity.description,
            'target_metric': entity.target_metric,
            'target_value': entity.target_value,
            'target_operator': entity.target_operator,
            'target_frequency': entity.target_frequency,
            'start_date': entity.start_date,
            'end_date': entity.end_date,
            'is_active': entity.is_active,
            'current_streak': entity.current_streak,
            'best_streak': entity.best_streak,
            'total_successes': entity.total_successes,
            'total_attempts': entity.total_attempts,
            'created_by': entity.created_by,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
            'completed_at': entity.completed_at
        }
    
    def _validate_entity(self, entity: MoodGoal, is_update: bool = False) -> None:
        """Validate MoodGoal entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.goal_type:
            raise ValidationError("Goal type is required")
        
        if not entity.goal_name:
            raise ValidationError("Goal name is required")
        
        if not entity.target_metric:
            raise ValidationError("Target metric is required")
        
        if entity.target_operator not in ['>=', '<=', '=', 'between']:
            raise ValidationError("Invalid target operator")
        
        if entity.current_streak < 0 or entity.best_streak < 0:
            raise ValidationError("Streak values must be non-negative")
        
        if entity.total_successes < 0 or entity.total_attempts < 0:
            raise ValidationError("Progress values must be non-negative")
        
        if entity.total_successes > entity.total_attempts:
            raise ValidationError("Successes cannot exceed attempts")
        
        if entity.end_date and entity.start_date and entity.end_date < entity.start_date:
            raise ValidationError("End date cannot be before start date")
        
        if not entity.start_date:
            entity.start_date = date.today()
        
        if not entity.goal_id and not is_update:
            import uuid
            entity.goal_id = str(uuid.uuid4())
    
    def get_user_goals(self, user_id: str, active_only: bool = True) -> List[MoodGoal]:
        """Get mood goals for a user."""
        filters = {'user_id': user_id}
        if active_only:
            filters['is_active'] = True
        
        options = QueryOptions(
            filters=filters,
            order_by=['-start_date']
        )
        
        result = self.list_all(options)
        return result.data
    
    def update_goal_progress(self, goal_id: str, success: bool) -> bool:
        """Update goal progress with success/failure."""
        try:
            goal = self.get_by_id(goal_id)
            if not goal:
                return False
            
            goal.total_attempts += 1
            
            if success:
                goal.total_successes += 1
                goal.current_streak += 1
                goal.best_streak = max(goal.best_streak, goal.current_streak)
            else:
                goal.current_streak = 0
            
            self.update(goal)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update goal progress: {e}")
            return False
