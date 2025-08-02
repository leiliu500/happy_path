"""
Conversational Agent Repository

Repository implementation for AI chat interactions, conversation management,
and conversational agent functionality.
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


class ConversationType(Enum):
    """Conversation type enumeration."""
    GENERAL_CHAT = "general_chat"
    CRISIS_SUPPORT = "crisis_support"
    THERAPY_GUIDED = "therapy_guided"
    MOOD_CHECK_IN = "mood_check_in"
    MEDICATION_REMINDER = "medication_reminder"
    GOAL_SETTING = "goal_setting"
    CBT_EXERCISE = "cbt_exercise"
    MINDFULNESS = "mindfulness"
    JOURNAL_PROMPT = "journal_prompt"
    ASSESSMENT = "assessment"


class MessageType(Enum):
    """Message type enumeration."""
    TEXT = "text"
    QUICK_REPLY = "quick_reply"
    BUTTON = "button"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"
    LOCATION = "location"
    SYSTEM = "system"


class MessageSender(Enum):
    """Message sender enumeration."""
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


class ConversationStatus(Enum):
    """Conversation status enumeration."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ESCALATED = "escalated"
    ARCHIVED = "archived"


class IntentConfidence(Enum):
    """Intent confidence enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class Conversation:
    """Conversation entity."""
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Conversation metadata
    conversation_type: ConversationType = ConversationType.GENERAL_CHAT
    status: ConversationStatus = ConversationStatus.ACTIVE
    title: Optional[str] = None
    
    # Timing
    started_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    # Context and state
    context: Optional[Dict[str, Any]] = None
    session_data: Optional[Dict[str, Any]] = None
    current_topic: Optional[str] = None
    conversation_flow: Optional[str] = None  # structured conversation flow ID
    
    # Escalation and supervision
    escalated_to_human: bool = False
    escalation_reason: Optional[str] = None
    assigned_therapist: Optional[str] = None
    
    # Analytics
    message_count: int = 0
    user_satisfaction_rating: Optional[int] = None  # 1-5 scale
    conversation_outcome: Optional[str] = None
    
    # AI model information
    model_version: Optional[str] = None
    model_parameters: Optional[Dict[str, Any]] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ChatMessage:
    """Chat message entity."""
    message_id: Optional[str] = None
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Message content
    sender: MessageSender = MessageSender.USER
    message_type: MessageType = MessageType.TEXT
    content: str = ""
    
    # Rich content
    attachments: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    # AI processing
    intent: Optional[str] = None
    intent_confidence: Optional[IntentConfidence] = None
    entities: Optional[List[Dict[str, Any]]] = None
    sentiment_score: Optional[Decimal] = None  # -1 to 1
    emotion_analysis: Optional[Dict[str, Any]] = None
    
    # Crisis and safety
    crisis_indicators: Optional[List[str]] = None
    safety_concern_level: Optional[str] = None  # none, low, moderate, high, critical
    
    # Response generation (for agent messages)
    response_template: Optional[str] = None
    response_personalization: Optional[Dict[str, Any]] = None
    
    # Feedback and quality
    user_reaction: Optional[str] = None  # thumbs_up, thumbs_down, helpful, not_helpful
    quality_score: Optional[Decimal] = None
    
    # Technical metadata
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None
    response_source: Optional[str] = None  # template, generated, retrieved
    
    # Message status
    delivered: bool = True
    read: bool = False
    read_at: Optional[datetime] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ConversationIntent:
    """Conversation intent entity."""
    intent_id: Optional[str] = None
    name: str = ""
    description: Optional[str] = None
    
    # Intent configuration
    keywords: Optional[List[str]] = None
    patterns: Optional[List[str]] = None
    examples: Optional[List[str]] = None
    
    # Response handling
    response_templates: Optional[List[str]] = None
    follow_up_prompts: Optional[List[str]] = None
    required_entities: Optional[List[str]] = None
    
    # Context and conditions
    conversation_types: Optional[List[ConversationType]] = None
    prerequisites: Optional[List[str]] = None
    exclusions: Optional[List[str]] = None
    
    # Quality metrics
    confidence_threshold: Decimal = Decimal('0.7')
    accuracy_rate: Optional[Decimal] = None
    usage_count: int = 0
    
    # Management
    is_active: bool = True
    created_by: Optional[str] = None
    last_updated_by: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ConversationAnalytics:
    """Conversation analytics entity."""
    analytics_id: Optional[str] = None
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Time period
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    
    # Engagement metrics
    total_messages: int = 0
    user_messages: int = 0
    agent_messages: int = 0
    average_response_time: Optional[Decimal] = None
    
    # Content analysis
    dominant_emotions: Optional[List[str]] = None
    sentiment_trend: Optional[str] = None  # positive, negative, neutral, mixed
    topics_discussed: Optional[List[str]] = None
    intents_triggered: Optional[Dict[str, int]] = None
    
    # Outcome metrics
    conversation_completion_rate: Optional[Decimal] = None
    user_satisfaction_score: Optional[Decimal] = None
    goal_achievement: Optional[bool] = None
    
    # Crisis and safety
    crisis_detections: int = 0
    escalations: int = 0
    safety_interventions: int = 0
    
    created_at: Optional[datetime] = None


class ConversationRepository(BaseRepository[Conversation, str]):
    """Repository for conversation management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "conversations", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> Conversation:
        """Convert database row to Conversation entity."""
        return Conversation(
            conversation_id=row.get('conversation_id'),
            user_id=row.get('user_id'),
            conversation_type=ConversationType(row['conversation_type']) if row.get('conversation_type') else ConversationType.GENERAL_CHAT,
            status=ConversationStatus(row['status']) if row.get('status') else ConversationStatus.ACTIVE,
            title=row.get('title'),
            started_at=row.get('started_at'),
            last_activity=row.get('last_activity'),
            ended_at=row.get('ended_at'),
            context=row.get('context'),
            session_data=row.get('session_data'),
            current_topic=row.get('current_topic'),
            conversation_flow=row.get('conversation_flow'),
            escalated_to_human=row.get('escalated_to_human', False),
            escalation_reason=row.get('escalation_reason'),
            assigned_therapist=row.get('assigned_therapist'),
            message_count=row.get('message_count', 0),
            user_satisfaction_rating=row.get('user_satisfaction_rating'),
            conversation_outcome=row.get('conversation_outcome'),
            model_version=row.get('model_version'),
            model_parameters=row.get('model_parameters'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: Conversation) -> Dict[str, Any]:
        """Convert Conversation entity to dictionary."""
        return {
            'conversation_id': entity.conversation_id,
            'user_id': entity.user_id,
            'conversation_type': entity.conversation_type.value,
            'status': entity.status.value,
            'title': entity.title,
            'started_at': entity.started_at,
            'last_activity': entity.last_activity,
            'ended_at': entity.ended_at,
            'context': entity.context,
            'session_data': entity.session_data,
            'current_topic': entity.current_topic,
            'conversation_flow': entity.conversation_flow,
            'escalated_to_human': entity.escalated_to_human,
            'escalation_reason': entity.escalation_reason,
            'assigned_therapist': entity.assigned_therapist,
            'message_count': entity.message_count,
            'user_satisfaction_rating': entity.user_satisfaction_rating,
            'conversation_outcome': entity.conversation_outcome,
            'model_version': entity.model_version,
            'model_parameters': entity.model_parameters,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: Conversation, is_update: bool = False) -> None:
        """Validate Conversation entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if entity.message_count < 0:
            raise ValidationError("Message count cannot be negative")
        
        if entity.user_satisfaction_rating and (entity.user_satisfaction_rating < 1 or entity.user_satisfaction_rating > 5):
            raise ValidationError("User satisfaction rating must be between 1 and 5")
        
        if not entity.started_at:
            entity.started_at = datetime.now()
        
        if not entity.last_activity:
            entity.last_activity = entity.started_at
        
        if not entity.conversation_id and not is_update:
            import uuid
            entity.conversation_id = str(uuid.uuid4())
    
    def start_conversation(self, user_id: str, conversation_type: ConversationType = ConversationType.GENERAL_CHAT,
                          title: str = None, context: Dict[str, Any] = None) -> Conversation:
        """Start a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            conversation_type=conversation_type,
            title=title or f"{conversation_type.value.replace('_', ' ').title()} Conversation",
            context=context or {}
        )
        
        created_conversation = self.create(conversation)
        
        self.logger.info(f"Started conversation {created_conversation.conversation_id} for user {user_id}")
        return created_conversation
    
    def get_user_conversations(self, user_id: str, active_only: bool = False, 
                             limit: Optional[int] = None) -> List[Conversation]:
        """Get conversations for a user."""
        filters = {'user_id': user_id}
        if active_only:
            filters['status'] = ConversationStatus.ACTIVE.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['-last_activity'],
            limit=limit
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_active_conversation(self, user_id: str) -> Optional[Conversation]:
        """Get the current active conversation for a user."""
        return self.find_one_by(
            user_id=user_id,
            status=ConversationStatus.ACTIVE.value
        )
    
    def update_activity(self, conversation_id: str) -> bool:
        """Update last activity timestamp."""
        try:
            conversation = self.get_by_id(conversation_id)
            if not conversation:
                return False
            
            conversation.last_activity = datetime.now()
            self.update(conversation)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update conversation activity: {e}")
            return False
    
    def end_conversation(self, conversation_id: str, outcome: str = None) -> bool:
        """End a conversation."""
        try:
            conversation = self.get_by_id(conversation_id)
            if not conversation:
                return False
            
            conversation.status = ConversationStatus.COMPLETED
            conversation.ended_at = datetime.now()
            if outcome:
                conversation.conversation_outcome = outcome
            
            self.update(conversation)
            
            self.logger.info(f"Ended conversation {conversation_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to end conversation: {e}")
            return False
    
    def escalate_conversation(self, conversation_id: str, reason: str, 
                            therapist_id: str = None) -> bool:
        """Escalate conversation to human."""
        try:
            conversation = self.get_by_id(conversation_id)
            if not conversation:
                return False
            
            conversation.escalated_to_human = True
            conversation.escalation_reason = reason
            conversation.assigned_therapist = therapist_id
            conversation.status = ConversationStatus.ESCALATED
            
            self.update(conversation)
            
            self.logger.info(f"Escalated conversation {conversation_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to escalate conversation: {e}")
            return False


class ChatMessageRepository(BaseRepository[ChatMessage, str]):
    """Repository for chat message management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "chat_messages", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> ChatMessage:
        """Convert database row to ChatMessage entity."""
        return ChatMessage(
            message_id=row.get('message_id'),
            conversation_id=row.get('conversation_id'),
            user_id=row.get('user_id'),
            sender=MessageSender(row['sender']) if row.get('sender') else MessageSender.USER,
            message_type=MessageType(row['message_type']) if row.get('message_type') else MessageType.TEXT,
            content=row.get('content', ''),
            attachments=row.get('attachments', []),
            metadata=row.get('metadata'),
            intent=row.get('intent'),
            intent_confidence=IntentConfidence(row['intent_confidence']) if row.get('intent_confidence') else None,
            entities=row.get('entities', []),
            sentiment_score=Decimal(str(row['sentiment_score'])) if row.get('sentiment_score') else None,
            emotion_analysis=row.get('emotion_analysis'),
            crisis_indicators=row.get('crisis_indicators', []),
            safety_concern_level=row.get('safety_concern_level'),
            response_template=row.get('response_template'),
            response_personalization=row.get('response_personalization'),
            user_reaction=row.get('user_reaction'),
            quality_score=Decimal(str(row['quality_score'])) if row.get('quality_score') else None,
            processing_time_ms=row.get('processing_time_ms'),
            model_used=row.get('model_used'),
            response_source=row.get('response_source'),
            delivered=row.get('delivered', True),
            read=row.get('read', False),
            read_at=row.get('read_at'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: ChatMessage) -> Dict[str, Any]:
        """Convert ChatMessage entity to dictionary."""
        return {
            'message_id': entity.message_id,
            'conversation_id': entity.conversation_id,
            'user_id': entity.user_id,
            'sender': entity.sender.value,
            'message_type': entity.message_type.value,
            'content': entity.content,
            'attachments': entity.attachments,
            'metadata': entity.metadata,
            'intent': entity.intent,
            'intent_confidence': entity.intent_confidence.value if entity.intent_confidence else None,
            'entities': entity.entities,
            'sentiment_score': entity.sentiment_score,
            'emotion_analysis': entity.emotion_analysis,
            'crisis_indicators': entity.crisis_indicators,
            'safety_concern_level': entity.safety_concern_level,
            'response_template': entity.response_template,
            'response_personalization': entity.response_personalization,
            'user_reaction': entity.user_reaction,
            'quality_score': entity.quality_score,
            'processing_time_ms': entity.processing_time_ms,
            'model_used': entity.model_used,
            'response_source': entity.response_source,
            'delivered': entity.delivered,
            'read': entity.read,
            'read_at': entity.read_at,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: ChatMessage, is_update: bool = False) -> None:
        """Validate ChatMessage entity."""
        if not entity.conversation_id:
            raise ValidationError("Conversation ID is required")
        
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.content and not entity.attachments:
            raise ValidationError("Message must have content or attachments")
        
        if entity.sentiment_score and (entity.sentiment_score < -1 or entity.sentiment_score > 1):
            raise ValidationError("Sentiment score must be between -1 and 1")
        
        if entity.quality_score and (entity.quality_score < 0 or entity.quality_score > 1):
            raise ValidationError("Quality score must be between 0 and 1")
        
        if entity.processing_time_ms and entity.processing_time_ms < 0:
            raise ValidationError("Processing time cannot be negative")
        
        if not entity.message_id and not is_update:
            import uuid
            entity.message_id = str(uuid.uuid4())
    
    def add_message(self, conversation_id: str, user_id: str, content: str,
                   sender: MessageSender = MessageSender.USER, 
                   message_type: MessageType = MessageType.TEXT,
                   attachments: List[Dict[str, Any]] = None) -> ChatMessage:
        """Add a message to a conversation."""
        message = ChatMessage(
            conversation_id=conversation_id,
            user_id=user_id,
            sender=sender,
            message_type=message_type,
            content=content,
            attachments=attachments or []
        )
        
        created_message = self.create(message)
        
        # Update conversation activity and message count
        try:
            conv_repo = ConversationRepository(self.db, self.logger)
            conversation = conv_repo.get_by_id(conversation_id)
            if conversation:
                conversation.message_count += 1
                conversation.last_activity = datetime.now()
                conv_repo.update(conversation)
        except Exception as e:
            self.logger.error(f"Failed to update conversation stats: {e}")
        
        return created_message
    
    def get_conversation_messages(self, conversation_id: str, 
                                limit: Optional[int] = None,
                                offset: int = 0) -> List[ChatMessage]:
        """Get messages for a conversation."""
        options = QueryOptions(
            filters={'conversation_id': conversation_id},
            order_by=['created_at'],
            limit=limit,
            offset=offset
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_recent_messages(self, conversation_id: str, count: int = 10) -> List[ChatMessage]:
        """Get recent messages from a conversation."""
        options = QueryOptions(
            filters={'conversation_id': conversation_id},
            order_by=['-created_at'],
            limit=count
        )
        
        result = self.list_all(options)
        return list(reversed(result.data))  # Return in chronological order
    
    def mark_as_read(self, message_id: str) -> bool:
        """Mark message as read."""
        try:
            message = self.get_by_id(message_id)
            if not message:
                return False
            
            message.read = True
            message.read_at = datetime.now()
            
            self.update(message)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to mark message as read: {e}")
            return False
    
    def add_user_reaction(self, message_id: str, reaction: str) -> bool:
        """Add user reaction to a message."""
        try:
            message = self.get_by_id(message_id)
            if not message:
                return False
            
            message.user_reaction = reaction
            self.update(message)
            
            self.logger.info(f"Added reaction '{reaction}' to message {message_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add reaction: {e}")
            return False
    
    def get_messages_with_crisis_indicators(self, user_id: str = None, 
                                          days_back: int = 7) -> List[ChatMessage]:
        """Get messages that contain crisis indicators."""
        start_date = datetime.now() - timedelta(days=days_back)
        
        filters = {
            'created_at__gte': start_date
        }
        
        if user_id:
            filters['user_id'] = user_id
        
        # Filter for messages with crisis indicators
        query = f"""
            SELECT * FROM {self.table_name}
            WHERE crisis_indicators IS NOT NULL 
            AND array_length(crisis_indicators, 1) > 0
        """
        
        if user_id:
            query += " AND user_id = %(user_id)s"
        
        query += f" AND created_at >= %(start_date)s ORDER BY created_at DESC"
        
        try:
            params = {'start_date': start_date}
            if user_id:
                params['user_id'] = user_id
            
            result = self.db.execute_query(query, params)
            return [self._to_entity(row) for row in result] if result else []
            
        except Exception as e:
            self.logger.error(f"Failed to get messages with crisis indicators: {e}")
            return []


class ConversationIntentRepository(BaseRepository[ConversationIntent, str]):
    """Repository for conversation intent management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "conversation_intents", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> ConversationIntent:
        """Convert database row to ConversationIntent entity."""
        return ConversationIntent(
            intent_id=row.get('intent_id'),
            name=row.get('name', ''),
            description=row.get('description'),
            keywords=row.get('keywords', []),
            patterns=row.get('patterns', []),
            examples=row.get('examples', []),
            response_templates=row.get('response_templates', []),
            follow_up_prompts=row.get('follow_up_prompts', []),
            required_entities=row.get('required_entities', []),
            conversation_types=[ConversationType(t) for t in row.get('conversation_types', [])],
            prerequisites=row.get('prerequisites', []),
            exclusions=row.get('exclusions', []),
            confidence_threshold=Decimal(str(row['confidence_threshold'])) if row.get('confidence_threshold') else Decimal('0.7'),
            accuracy_rate=Decimal(str(row['accuracy_rate'])) if row.get('accuracy_rate') else None,
            usage_count=row.get('usage_count', 0),
            is_active=row.get('is_active', True),
            created_by=row.get('created_by'),
            last_updated_by=row.get('last_updated_by'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: ConversationIntent) -> Dict[str, Any]:
        """Convert ConversationIntent entity to dictionary."""
        return {
            'intent_id': entity.intent_id,
            'name': entity.name,
            'description': entity.description,
            'keywords': entity.keywords,
            'patterns': entity.patterns,
            'examples': entity.examples,
            'response_templates': entity.response_templates,
            'follow_up_prompts': entity.follow_up_prompts,
            'required_entities': entity.required_entities,
            'conversation_types': [t.value for t in entity.conversation_types] if entity.conversation_types else [],
            'prerequisites': entity.prerequisites,
            'exclusions': entity.exclusions,
            'confidence_threshold': entity.confidence_threshold,
            'accuracy_rate': entity.accuracy_rate,
            'usage_count': entity.usage_count,
            'is_active': entity.is_active,
            'created_by': entity.created_by,
            'last_updated_by': entity.last_updated_by,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: ConversationIntent, is_update: bool = False) -> None:
        """Validate ConversationIntent entity."""
        if not entity.name:
            raise ValidationError("Intent name is required")
        
        if entity.confidence_threshold < 0 or entity.confidence_threshold > 1:
            raise ValidationError("Confidence threshold must be between 0 and 1")
        
        if entity.accuracy_rate and (entity.accuracy_rate < 0 or entity.accuracy_rate > 1):
            raise ValidationError("Accuracy rate must be between 0 and 1")
        
        if entity.usage_count < 0:
            raise ValidationError("Usage count cannot be negative")
        
        if not entity.intent_id and not is_update:
            import uuid
            entity.intent_id = str(uuid.uuid4())
    
    def get_active_intents(self, conversation_type: ConversationType = None) -> List[ConversationIntent]:
        """Get active intents."""
        filters = {'is_active': True}
        
        options = QueryOptions(
            filters=filters,
            order_by=['-usage_count', 'name']
        )
        
        result = self.list_all(options)
        intents = result.data
        
        # Filter by conversation type if specified
        if conversation_type:
            intents = [i for i in intents if not i.conversation_types or conversation_type in i.conversation_types]
        
        return intents
    
    def increment_usage(self, intent_id: str) -> bool:
        """Increment usage count for an intent."""
        try:
            intent = self.get_by_id(intent_id)
            if not intent:
                return False
            
            intent.usage_count += 1
            self.update(intent)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to increment intent usage: {e}")
            return False
