"""
Journaling Repository

Repository implementation for journaling entries, prompts, CBT techniques,
and reflection guidance functionality.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class JournalEntryType(Enum):
    """Journal entry type enumeration."""
    FREE_WRITING = "free_writing"
    GUIDED_PROMPT = "guided_prompt"
    GRATITUDE = "gratitude"
    CBT_THOUGHT_RECORD = "cbt_thought_record"
    DAILY_REFLECTION = "daily_reflection"
    GOAL_SETTING = "goal_setting"
    MOOD_EXPLORATION = "mood_exploration"
    TRIGGER_ANALYSIS = "trigger_analysis"
    COPING_STRATEGIES = "coping_strategies"
    THERAPY_HOMEWORK = "therapy_homework"


class CBTTechnique(Enum):
    """CBT technique enumeration."""
    THOUGHT_CHALLENGING = "thought_challenging"
    BEHAVIORAL_ACTIVATION = "behavioral_activation"
    EXPOSURE_THERAPY = "exposure_therapy"
    MINDFULNESS = "mindfulness"
    PROBLEM_SOLVING = "problem_solving"
    COGNITIVE_RESTRUCTURING = "cognitive_restructuring"
    ACTIVITY_SCHEDULING = "activity_scheduling"
    RELAXATION_TECHNIQUES = "relaxation_techniques"
    GROUNDING_EXERCISES = "grounding_exercises"


class IntensityScale(Enum):
    """Emotional intensity scale enumeration."""
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


@dataclass
class JournalEntry:
    """Journal entry entity."""
    entry_id: Optional[str] = None
    user_id: Optional[str] = None
    entry_type: JournalEntryType = JournalEntryType.FREE_WRITING
    
    # Content
    title: Optional[str] = None
    content: str = ""
    word_count: int = 0
    
    # Prompts and guidance
    prompt_id: Optional[str] = None
    prompt_question: Optional[str] = None
    
    # Emotional context
    emotions_before: Optional[List[str]] = None
    emotions_after: Optional[List[str]] = None
    mood_before: Optional[IntensityScale] = None
    mood_after: Optional[IntensityScale] = None
    
    # CBT-specific fields
    cbt_technique: Optional[CBTTechnique] = None
    situation_description: Optional[str] = None
    automatic_thoughts: Optional[str] = None
    cognitive_distortions: Optional[List[str]] = None
    evidence_for: Optional[str] = None
    evidence_against: Optional[str] = None
    balanced_thought: Optional[str] = None
    behavioral_response: Optional[str] = None
    intensity_before: Optional[IntensityScale] = None
    intensity_after: Optional[IntensityScale] = None
    
    # Gratitude-specific fields
    gratitude_items: Optional[List[str]] = None
    gratitude_reasons: Optional[str] = None
    
    # Goal and action items
    goals_mentioned: Optional[List[str]] = None
    action_items: Optional[List[str]] = None
    insights_gained: Optional[str] = None
    
    # Privacy and sharing
    is_private: bool = True
    shared_with_therapist: bool = False
    shared_at: Optional[datetime] = None
    
    # AI analysis
    sentiment_score: Optional[Decimal] = None  # -1 to 1 scale
    emotion_analysis: Optional[Dict[str, Any]] = None
    key_themes: Optional[List[str]] = None
    risk_indicators: Optional[List[str]] = None
    ai_insights: Optional[str] = None
    
    # Metadata
    writing_duration_minutes: Optional[int] = None
    device_type: Optional[str] = None
    location_written: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class JournalPrompt:
    """Journal prompt entity."""
    prompt_id: Optional[str] = None
    category: str = ""
    subcategory: Optional[str] = None
    prompt_type: JournalEntryType = JournalEntryType.GUIDED_PROMPT
    
    # Prompt content
    question: str = ""
    description: Optional[str] = None
    follow_up_questions: Optional[List[str]] = None
    
    # CBT-specific prompt data
    cbt_technique: Optional[CBTTechnique] = None
    therapeutic_goal: Optional[str] = None
    difficulty_level: str = "beginner"  # beginner, intermediate, advanced
    
    # Targeting and personalization
    target_emotions: Optional[List[str]] = None
    target_situations: Optional[List[str]] = None
    age_group: str = "all"  # teen, adult, senior, all
    clinical_conditions: Optional[List[str]] = None  # anxiety, depression, ptsd, etc.
    
    # Usage tracking
    usage_count: int = 0
    effectiveness_rating: Optional[Decimal] = None  # average user rating
    
    # Content management
    is_active: bool = True
    created_by: Optional[str] = None
    approved_by: Optional[str] = None
    language: str = "en"
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserPromptHistory:
    """User prompt history entity."""
    history_id: Optional[str] = None
    user_id: Optional[str] = None
    prompt_id: Optional[str] = None
    
    # Usage data
    presented_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    completed: bool = False
    skipped: bool = False
    
    # User feedback
    user_rating: Optional[int] = None  # 1-5 scale
    user_feedback: Optional[str] = None
    found_helpful: Optional[bool] = None
    
    # Response metrics
    response_time_minutes: Optional[int] = None
    word_count: Optional[int] = None
    mood_improvement: Optional[bool] = None
    
    created_at: Optional[datetime] = None


@dataclass
class JournalAnalytics:
    """Journal analytics data."""
    user_id: str
    period_start: date
    period_end: date
    
    # Writing statistics
    total_entries: int
    total_words: int
    average_words_per_entry: float
    writing_frequency: float  # entries per week
    
    # Emotional insights
    common_emotions: List[str]
    emotion_trends: Dict[str, Any]
    mood_improvement_rate: float
    
    # Content analysis
    common_themes: List[str]
    goal_achievement_rate: float
    cbt_technique_usage: Dict[str, int]
    
    # Engagement metrics
    writing_streak: int
    favorite_prompts: List[Dict[str, Any]]
    preferred_writing_times: List[str]


class JournalEntryRepository(BaseRepository[JournalEntry, str]):
    """Repository for journal entry management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "journal_entries", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> JournalEntry:
        """Convert database row to JournalEntry entity."""
        return JournalEntry(
            entry_id=row.get('entry_id'),
            user_id=row.get('user_id'),
            entry_type=JournalEntryType(row['entry_type']) if row.get('entry_type') else JournalEntryType.FREE_WRITING,
            title=row.get('title'),
            content=row.get('content', ''),
            word_count=row.get('word_count', 0),
            prompt_id=row.get('prompt_id'),
            prompt_question=row.get('prompt_question'),
            emotions_before=row.get('emotions_before', []),
            emotions_after=row.get('emotions_after', []),
            mood_before=IntensityScale(row['mood_before']) if row.get('mood_before') else None,
            mood_after=IntensityScale(row['mood_after']) if row.get('mood_after') else None,
            cbt_technique=CBTTechnique(row['cbt_technique']) if row.get('cbt_technique') else None,
            situation_description=row.get('situation_description'),
            automatic_thoughts=row.get('automatic_thoughts'),
            cognitive_distortions=row.get('cognitive_distortions', []),
            evidence_for=row.get('evidence_for'),
            evidence_against=row.get('evidence_against'),
            balanced_thought=row.get('balanced_thought'),
            behavioral_response=row.get('behavioral_response'),
            intensity_before=IntensityScale(row['intensity_before']) if row.get('intensity_before') else None,
            intensity_after=IntensityScale(row['intensity_after']) if row.get('intensity_after') else None,
            gratitude_items=row.get('gratitude_items', []),
            gratitude_reasons=row.get('gratitude_reasons'),
            goals_mentioned=row.get('goals_mentioned', []),
            action_items=row.get('action_items', []),
            insights_gained=row.get('insights_gained'),
            is_private=row.get('is_private', True),
            shared_with_therapist=row.get('shared_with_therapist', False),
            shared_at=row.get('shared_at'),
            sentiment_score=Decimal(str(row['sentiment_score'])) if row.get('sentiment_score') else None,
            emotion_analysis=row.get('emotion_analysis'),
            key_themes=row.get('key_themes', []),
            risk_indicators=row.get('risk_indicators', []),
            ai_insights=row.get('ai_insights'),
            writing_duration_minutes=row.get('writing_duration_minutes'),
            device_type=row.get('device_type'),
            location_written=row.get('location_written'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: JournalEntry) -> Dict[str, Any]:
        """Convert JournalEntry entity to dictionary."""
        return {
            'entry_id': entity.entry_id,
            'user_id': entity.user_id,
            'entry_type': entity.entry_type.value,
            'title': entity.title,
            'content': entity.content,
            'word_count': entity.word_count,
            'prompt_id': entity.prompt_id,
            'prompt_question': entity.prompt_question,
            'emotions_before': entity.emotions_before,
            'emotions_after': entity.emotions_after,
            'mood_before': entity.mood_before.value if entity.mood_before else None,
            'mood_after': entity.mood_after.value if entity.mood_after else None,
            'cbt_technique': entity.cbt_technique.value if entity.cbt_technique else None,
            'situation_description': entity.situation_description,
            'automatic_thoughts': entity.automatic_thoughts,
            'cognitive_distortions': entity.cognitive_distortions,
            'evidence_for': entity.evidence_for,
            'evidence_against': entity.evidence_against,
            'balanced_thought': entity.balanced_thought,
            'behavioral_response': entity.behavioral_response,
            'intensity_before': entity.intensity_before.value if entity.intensity_before else None,
            'intensity_after': entity.intensity_after.value if entity.intensity_after else None,
            'gratitude_items': entity.gratitude_items,
            'gratitude_reasons': entity.gratitude_reasons,
            'goals_mentioned': entity.goals_mentioned,
            'action_items': entity.action_items,
            'insights_gained': entity.insights_gained,
            'is_private': entity.is_private,
            'shared_with_therapist': entity.shared_with_therapist,
            'shared_at': entity.shared_at,
            'sentiment_score': entity.sentiment_score,
            'emotion_analysis': entity.emotion_analysis,
            'key_themes': entity.key_themes,
            'risk_indicators': entity.risk_indicators,
            'ai_insights': entity.ai_insights,
            'writing_duration_minutes': entity.writing_duration_minutes,
            'device_type': entity.device_type,
            'location_written': entity.location_written,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: JournalEntry, is_update: bool = False) -> None:
        """Validate JournalEntry entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.content.strip():
            raise ValidationError("Entry content is required")
        
        # Calculate word count if not provided
        if entity.word_count == 0:
            entity.word_count = len(entity.content.split())
        
        if entity.word_count < 0:
            raise ValidationError("Word count must be non-negative")
        
        if entity.sentiment_score and (entity.sentiment_score < -1 or entity.sentiment_score > 1):
            raise ValidationError("Sentiment score must be between -1 and 1")
        
        if entity.writing_duration_minutes and entity.writing_duration_minutes < 0:
            raise ValidationError("Writing duration must be non-negative")
        
        if not entity.entry_id and not is_update:
            import uuid
            entity.entry_id = str(uuid.uuid4())
    
    def get_user_entries(self, user_id: str, start_date: date = None, 
                        end_date: date = None, entry_type: JournalEntryType = None,
                        limit: Optional[int] = None) -> List[JournalEntry]:
        """Get journal entries for a user."""
        filters = {'user_id': user_id}
        
        if start_date:
            filters['created_at__gte'] = datetime.combine(start_date, datetime.min.time())
        if end_date:
            filters['created_at__lte'] = datetime.combine(end_date, datetime.max.time())
        if entry_type:
            filters['entry_type'] = entry_type.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['-created_at'],
            limit=limit
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_recent_entries(self, user_id: str, days: int = 7) -> List[JournalEntry]:
        """Get recent journal entries for a user."""
        start_date = date.today() - timedelta(days=days)
        return self.get_user_entries(user_id, start_date)
    
    def get_shared_entries(self, user_id: str, therapist_id: str = None) -> List[JournalEntry]:
        """Get entries shared with therapist."""
        filters = {
            'user_id': user_id,
            'shared_with_therapist': True
        }
        
        options = QueryOptions(
            filters=filters,
            order_by=['-shared_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def share_with_therapist(self, entry_id: str) -> bool:
        """Share journal entry with therapist."""
        try:
            entry = self.get_by_id(entry_id)
            if not entry:
                return False
            
            entry.shared_with_therapist = True
            entry.shared_at = datetime.now()
            
            self.update(entry)
            
            self.logger.info(f"Shared journal entry {entry_id} with therapist")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to share entry {entry_id}: {e}")
            return False
    
    def calculate_writing_statistics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Calculate writing statistics for a user."""
        try:
            start_date = date.today() - timedelta(days=days)
            entries = self.get_user_entries(user_id, start_date)
            
            if not entries:
                return {}
            
            total_words = sum(entry.word_count for entry in entries)
            avg_words = total_words / len(entries) if entries else 0
            
            # Calculate writing frequency (entries per week)
            writing_frequency = (len(entries) / days) * 7
            
            # Count entry types
            entry_types = {}
            for entry in entries:
                entry_type = entry.entry_type.value
                entry_types[entry_type] = entry_types.get(entry_type, 0) + 1
            
            # Calculate mood improvement
            mood_improvements = 0
            mood_comparisons = 0
            
            for entry in entries:
                if entry.mood_before and entry.mood_after:
                    mood_comparisons += 1
                    if int(entry.mood_after.value) > int(entry.mood_before.value):
                        mood_improvements += 1
            
            mood_improvement_rate = (mood_improvements / mood_comparisons) if mood_comparisons > 0 else 0
            
            return {
                'total_entries': len(entries),
                'total_words': total_words,
                'average_words_per_entry': round(avg_words, 1),
                'writing_frequency': round(writing_frequency, 2),
                'entry_types': entry_types,
                'mood_improvement_rate': round(mood_improvement_rate * 100, 1),
                'period_days': days
            }
            
        except Exception as e:
            self.logger.error(f"Failed to calculate writing statistics: {e}")
            return {}
    
    def get_entries_with_risk_indicators(self, user_id: str = None) -> List[JournalEntry]:
        """Get entries that contain risk indicators."""
        filters = {}
        if user_id:
            filters['user_id'] = user_id
        
        # Filter for entries with risk indicators
        query = f"""
            SELECT * FROM {self.table_name}
            WHERE risk_indicators IS NOT NULL 
            AND array_length(risk_indicators, 1) > 0
        """
        
        if user_id:
            query += " AND user_id = %(user_id)s"
        
        query += " ORDER BY created_at DESC"
        
        try:
            params = {'user_id': user_id} if user_id else {}
            result = self.db.execute_query(query, params)
            
            return [self._to_entity(row) for row in result] if result else []
            
        except Exception as e:
            self.logger.error(f"Failed to get entries with risk indicators: {e}")
            return []


class JournalPromptRepository(BaseRepository[JournalPrompt, str]):
    """Repository for journal prompt management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "journal_prompts", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> JournalPrompt:
        """Convert database row to JournalPrompt entity."""
        return JournalPrompt(
            prompt_id=row.get('prompt_id'),
            category=row.get('category', ''),
            subcategory=row.get('subcategory'),
            prompt_type=JournalEntryType(row['prompt_type']) if row.get('prompt_type') else JournalEntryType.GUIDED_PROMPT,
            question=row.get('question', ''),
            description=row.get('description'),
            follow_up_questions=row.get('follow_up_questions', []),
            cbt_technique=CBTTechnique(row['cbt_technique']) if row.get('cbt_technique') else None,
            therapeutic_goal=row.get('therapeutic_goal'),
            difficulty_level=row.get('difficulty_level', 'beginner'),
            target_emotions=row.get('target_emotions', []),
            target_situations=row.get('target_situations', []),
            age_group=row.get('age_group', 'all'),
            clinical_conditions=row.get('clinical_conditions', []),
            usage_count=row.get('usage_count', 0),
            effectiveness_rating=Decimal(str(row['effectiveness_rating'])) if row.get('effectiveness_rating') else None,
            is_active=row.get('is_active', True),
            created_by=row.get('created_by'),
            approved_by=row.get('approved_by'),
            language=row.get('language', 'en'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: JournalPrompt) -> Dict[str, Any]:
        """Convert JournalPrompt entity to dictionary."""
        return {
            'prompt_id': entity.prompt_id,
            'category': entity.category,
            'subcategory': entity.subcategory,
            'prompt_type': entity.prompt_type.value,
            'question': entity.question,
            'description': entity.description,
            'follow_up_questions': entity.follow_up_questions,
            'cbt_technique': entity.cbt_technique.value if entity.cbt_technique else None,
            'therapeutic_goal': entity.therapeutic_goal,
            'difficulty_level': entity.difficulty_level,
            'target_emotions': entity.target_emotions,
            'target_situations': entity.target_situations,
            'age_group': entity.age_group,
            'clinical_conditions': entity.clinical_conditions,
            'usage_count': entity.usage_count,
            'effectiveness_rating': entity.effectiveness_rating,
            'is_active': entity.is_active,
            'created_by': entity.created_by,
            'approved_by': entity.approved_by,
            'language': entity.language,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: JournalPrompt, is_update: bool = False) -> None:
        """Validate JournalPrompt entity."""
        if not entity.category:
            raise ValidationError("Category is required")
        
        if not entity.question:
            raise ValidationError("Prompt question is required")
        
        if entity.effectiveness_rating and (entity.effectiveness_rating < 0 or entity.effectiveness_rating > 5):
            raise ValidationError("Effectiveness rating must be between 0 and 5")
        
        if not entity.prompt_id and not is_update:
            import uuid
            entity.prompt_id = str(uuid.uuid4())
    
    def get_prompts_by_category(self, category: str, active_only: bool = True) -> List[JournalPrompt]:
        """Get prompts by category."""
        filters = {'category': category}
        if active_only:
            filters['is_active'] = True
        
        options = QueryOptions(
            filters=filters,
            order_by=['effectiveness_rating', 'usage_count']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_personalized_prompts(self, user_profile: Dict[str, Any], limit: int = 10) -> List[JournalPrompt]:
        """Get personalized prompts based on user profile."""
        try:
            # This would integrate with user profile data and preferences
            # For now, return popular prompts
            
            filters = {'is_active': True}
            
            options = QueryOptions(
                filters=filters,
                order_by=['-effectiveness_rating', '-usage_count'],
                limit=limit
            )
            
            result = self.list_all(options)
            return result.data
            
        except Exception as e:
            self.logger.error(f"Failed to get personalized prompts: {e}")
            return []
    
    def increment_usage(self, prompt_id: str) -> bool:
        """Increment usage count for a prompt."""
        try:
            query = f"""
                UPDATE {self.table_name}
                SET usage_count = usage_count + 1
                WHERE prompt_id = %(prompt_id)s
            """
            
            self.db.execute_query(query, {'prompt_id': prompt_id})
            return self.db.get_affected_rows() > 0
            
        except Exception as e:
            self.logger.error(f"Failed to increment usage for prompt {prompt_id}: {e}")
            return False


class UserPromptHistoryRepository(BaseRepository[UserPromptHistory, str]):
    """Repository for user prompt history management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "user_prompt_history", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> UserPromptHistory:
        """Convert database row to UserPromptHistory entity."""
        return UserPromptHistory(
            history_id=row.get('history_id'),
            user_id=row.get('user_id'),
            prompt_id=row.get('prompt_id'),
            presented_at=row.get('presented_at'),
            responded_at=row.get('responded_at'),
            completed=row.get('completed', False),
            skipped=row.get('skipped', False),
            user_rating=row.get('user_rating'),
            user_feedback=row.get('user_feedback'),
            found_helpful=row.get('found_helpful'),
            response_time_minutes=row.get('response_time_minutes'),
            word_count=row.get('word_count'),
            mood_improvement=row.get('mood_improvement'),
            created_at=row.get('created_at')
        )
    
    def _to_dict(self, entity: UserPromptHistory) -> Dict[str, Any]:
        """Convert UserPromptHistory entity to dictionary."""
        return {
            'history_id': entity.history_id,
            'user_id': entity.user_id,
            'prompt_id': entity.prompt_id,
            'presented_at': entity.presented_at,
            'responded_at': entity.responded_at,
            'completed': entity.completed,
            'skipped': entity.skipped,
            'user_rating': entity.user_rating,
            'user_feedback': entity.user_feedback,
            'found_helpful': entity.found_helpful,
            'response_time_minutes': entity.response_time_minutes,
            'word_count': entity.word_count,
            'mood_improvement': entity.mood_improvement,
            'created_at': entity.created_at
        }
    
    def _validate_entity(self, entity: UserPromptHistory, is_update: bool = False) -> None:
        """Validate UserPromptHistory entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.prompt_id:
            raise ValidationError("Prompt ID is required")
        
        if entity.user_rating and (entity.user_rating < 1 or entity.user_rating > 5):
            raise ValidationError("User rating must be between 1 and 5")
        
        if not entity.history_id and not is_update:
            import uuid
            entity.history_id = str(uuid.uuid4())
    
    def get_user_history(self, user_id: str, limit: Optional[int] = None) -> List[UserPromptHistory]:
        """Get prompt history for a user."""
        options = QueryOptions(
            filters={'user_id': user_id},
            order_by=['-presented_at'],
            limit=limit
        )
        
        result = self.list_all(options)
        return result.data
    
    def record_prompt_interaction(self, user_id: str, prompt_id: str, 
                                completed: bool = False, skipped: bool = False,
                                rating: Optional[int] = None) -> UserPromptHistory:
        """Record a prompt interaction."""
        history = UserPromptHistory(
            user_id=user_id,
            prompt_id=prompt_id,
            presented_at=datetime.now(),
            completed=completed,
            skipped=skipped,
            user_rating=rating
        )
        
        if completed:
            history.responded_at = datetime.now()
        
        return self.create(history)
