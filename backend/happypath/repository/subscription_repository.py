"""
Subscription Repository

Repository implementation for subscription and billing management.
Handles subscription plans, billing cycles, payments, and usage tracking.
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class SubscriptionStatus(Enum):
    """Subscription status enumeration."""
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class BillingCycle(Enum):
    """Billing cycle enumeration."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


@dataclass
class SubscriptionPlan:
    """Subscription plan definition."""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    price: Decimal = Decimal('0.00')
    currency: str = "USD"
    billing_cycle: str = BillingCycle.MONTHLY.value
    features: Optional[List[str]] = None
    limits: Optional[Dict[str, Any]] = None  # usage limits
    is_active: bool = True
    trial_days: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Subscription:
    """User subscription entity."""
    id: Optional[int] = None
    user_id: int = 0
    plan_id: int = 0
    status: str = SubscriptionStatus.TRIAL.value
    
    # Billing information
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    next_billing_date: Optional[datetime] = None
    
    # Trial information
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    
    # Cancellation
    canceled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    ends_at: Optional[datetime] = None  # When subscription actually ends
    
    # Payment
    payment_method_id: Optional[str] = None
    last_payment_date: Optional[datetime] = None
    next_payment_amount: Optional[Decimal] = None
    
    # Usage tracking
    usage_data: Optional[Dict[str, Any]] = None
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None
    
    def is_active(self) -> bool:
        """Check if subscription is active."""
        return self.status in [SubscriptionStatus.ACTIVE.value, SubscriptionStatus.TRIAL.value]
    
    def is_trial(self) -> bool:
        """Check if subscription is in trial period."""
        if self.status != SubscriptionStatus.TRIAL.value:
            return False
        if not self.trial_end:
            return False
        return datetime.utcnow() <= self.trial_end
    
    def days_until_renewal(self) -> Optional[int]:
        """Get days until next billing."""
        if not self.next_billing_date:
            return None
        delta = self.next_billing_date - datetime.utcnow()
        return max(0, delta.days)
    
    def days_until_trial_end(self) -> Optional[int]:
        """Get days until trial ends."""
        if not self.trial_end:
            return None
        delta = self.trial_end - datetime.utcnow()
        return max(0, delta.days)


@dataclass
class Payment:
    """Payment record."""
    id: Optional[int] = None
    subscription_id: int = 0
    user_id: int = 0
    amount: Decimal = Decimal('0.00')
    currency: str = "USD"
    status: str = PaymentStatus.PENDING.value
    
    # Payment details
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    invoice_id: Optional[str] = None
    
    # Timestamps
    payment_date: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    # Failure information
    failure_reason: Optional[str] = None
    failure_code: Optional[str] = None
    
    # Refund information
    refunded_amount: Optional[Decimal] = None
    refunded_at: Optional[datetime] = None
    refund_reason: Optional[str] = None
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UsageRecord:
    """Usage tracking record."""
    id: Optional[int] = None
    subscription_id: int = 0
    user_id: int = 0
    feature: str = ""  # feature being tracked
    usage_count: int = 0
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    recorded_at: Optional[datetime] = None
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SubscriptionAnalytics:
    """Subscription analytics data."""
    total_subscriptions: int
    active_subscriptions: int
    trial_subscriptions: int
    canceled_subscriptions: int
    revenue_current_month: Decimal
    revenue_previous_month: Decimal
    churn_rate: float
    conversion_rate: float  # trial to paid
    average_revenue_per_user: Decimal
    plan_distribution: Dict[str, int]
    payment_method_distribution: Dict[str, int]
    geographic_distribution: Dict[str, int]


class SubscriptionPlanRepository(BaseRepository[SubscriptionPlan, int]):
    """Repository for subscription plan management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "subscription_plans", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> SubscriptionPlan:
        """Convert database row to SubscriptionPlan entity."""
        return SubscriptionPlan(
            id=row.get('id'),
            name=row.get('name', ''),
            description=row.get('description'),
            price=Decimal(str(row.get('price', '0.00'))),
            currency=row.get('currency', 'USD'),
            billing_cycle=row.get('billing_cycle', BillingCycle.MONTHLY.value),
            features=row.get('features', []),
            limits=row.get('limits'),
            is_active=row.get('is_active', True),
            trial_days=row.get('trial_days', 0),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at'),
            metadata=row.get('metadata')
        )
    
    def _to_dict(self, entity: SubscriptionPlan) -> Dict[str, Any]:
        """Convert SubscriptionPlan entity to dictionary."""
        return {
            'id': entity.id,
            'name': entity.name,
            'description': entity.description,
            'price': float(entity.price),
            'currency': entity.currency,
            'billing_cycle': entity.billing_cycle,
            'features': entity.features,
            'limits': entity.limits,
            'is_active': entity.is_active,
            'trial_days': entity.trial_days,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
            'metadata': entity.metadata
        }
    
    def _validate_entity(self, entity: SubscriptionPlan, is_update: bool = False) -> None:
        """Validate SubscriptionPlan entity."""
        if not entity.name:
            raise ValidationError("Plan name is required")
        
        if entity.price < 0:
            raise ValidationError("Plan price cannot be negative")
        
        if entity.billing_cycle not in [cycle.value for cycle in BillingCycle]:
            raise ValidationError(f"Invalid billing cycle: {entity.billing_cycle}")
        
        if entity.trial_days < 0:
            raise ValidationError("Trial days cannot be negative")
    
    def get_active_plans(self) -> List[SubscriptionPlan]:
        """Get all active subscription plans."""
        options = QueryOptions(
            filters={'is_active': True},
            order_by=['price']
        )
        result = self.list_all(options)
        return result.data
    
    def get_plan_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        """Get plan by name."""
        return self.find_one_by(name=name)


class SubscriptionRepository(BaseRepository[Subscription, int]):
    """Repository for subscription management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "subscriptions", logger)
        self.plan_repo = SubscriptionPlanRepository(db_manager, logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> Subscription:
        """Convert database row to Subscription entity."""
        return Subscription(
            id=row.get('id'),
            user_id=row.get('user_id', 0),
            plan_id=row.get('plan_id', 0),
            status=row.get('status', SubscriptionStatus.TRIAL.value),
            current_period_start=row.get('current_period_start'),
            current_period_end=row.get('current_period_end'),
            next_billing_date=row.get('next_billing_date'),
            trial_start=row.get('trial_start'),
            trial_end=row.get('trial_end'),
            canceled_at=row.get('canceled_at'),
            cancellation_reason=row.get('cancellation_reason'),
            ends_at=row.get('ends_at'),
            payment_method_id=row.get('payment_method_id'),
            last_payment_date=row.get('last_payment_date'),
            next_payment_amount=Decimal(str(row.get('next_payment_amount', '0.00'))) if row.get('next_payment_amount') else None,
            usage_data=row.get('usage_data'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at'),
            metadata=row.get('metadata')
        )
    
    def _to_dict(self, entity: Subscription) -> Dict[str, Any]:
        """Convert Subscription entity to dictionary."""
        return {
            'id': entity.id,
            'user_id': entity.user_id,
            'plan_id': entity.plan_id,
            'status': entity.status,
            'current_period_start': entity.current_period_start,
            'current_period_end': entity.current_period_end,
            'next_billing_date': entity.next_billing_date,
            'trial_start': entity.trial_start,
            'trial_end': entity.trial_end,
            'canceled_at': entity.canceled_at,
            'cancellation_reason': entity.cancellation_reason,
            'ends_at': entity.ends_at,
            'payment_method_id': entity.payment_method_id,
            'last_payment_date': entity.last_payment_date,
            'next_payment_amount': float(entity.next_payment_amount) if entity.next_payment_amount else None,
            'usage_data': entity.usage_data,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
            'metadata': entity.metadata
        }
    
    def _validate_entity(self, entity: Subscription, is_update: bool = False) -> None:
        """Validate Subscription entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.plan_id:
            raise ValidationError("Plan ID is required")
        
        if entity.status not in [status.value for status in SubscriptionStatus]:
            raise ValidationError(f"Invalid subscription status: {entity.status}")
        
        # Validate plan exists
        plan = self.plan_repo.get_by_id(entity.plan_id)
        if not plan:
            raise ValidationError(f"Invalid plan ID: {entity.plan_id}")
    
    def create_subscription(self, user_id: int, plan_id: int, 
                          payment_method_id: Optional[str] = None,
                          start_trial: bool = True) -> Subscription:
        """
        Create a new subscription for a user.
        
        Args:
            user_id: User ID
            plan_id: Subscription plan ID
            payment_method_id: Payment method identifier
            start_trial: Whether to start with trial period
            
        Returns:
            Created Subscription
        """
        # Get plan details
        plan = self.plan_repo.get_by_id_or_raise(plan_id)
        
        now = datetime.utcnow()
        
        # Determine if this should be a trial subscription
        if start_trial and plan.trial_days > 0:
            status = SubscriptionStatus.TRIAL.value
            trial_start = now
            trial_end = now + timedelta(days=plan.trial_days)
            next_billing_date = trial_end
        else:
            status = SubscriptionStatus.ACTIVE.value
            trial_start = None
            trial_end = None
            # Set next billing based on plan cycle
            if plan.billing_cycle == BillingCycle.MONTHLY.value:
                next_billing_date = now + timedelta(days=30)
            elif plan.billing_cycle == BillingCycle.QUARTERLY.value:
                next_billing_date = now + timedelta(days=90)
            elif plan.billing_cycle == BillingCycle.YEARLY.value:
                next_billing_date = now + timedelta(days=365)
            else:  # LIFETIME
                next_billing_date = None
        
        subscription = Subscription(
            user_id=user_id,
            plan_id=plan_id,
            status=status,
            current_period_start=now,
            current_period_end=next_billing_date,
            next_billing_date=next_billing_date,
            trial_start=trial_start,
            trial_end=trial_end,
            payment_method_id=payment_method_id,
            next_payment_amount=plan.price if status == SubscriptionStatus.ACTIVE.value else None
        )
        
        created_subscription = self.create(subscription)
        
        self.logger.info(f"Created subscription for user {user_id}", extra={
            "user_id": user_id,
            "subscription_id": created_subscription.id,
            "plan_id": plan_id,
            "status": status,
            "operation": "create_subscription"
        })
        
        return created_subscription
    
    def get_user_subscription(self, user_id: int) -> Optional[Subscription]:
        """Get active subscription for a user."""
        active_statuses = [
            SubscriptionStatus.TRIAL.value,
            SubscriptionStatus.ACTIVE.value,
            SubscriptionStatus.PAST_DUE.value
        ]
        
        try:
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE user_id = %(user_id)s 
                AND status = ANY(%(statuses)s)
                ORDER BY created_at DESC
                LIMIT 1
            """
            
            params = {
                'user_id': user_id,
                'statuses': active_statuses
            }
            
            result = self.db.execute_query(query, params)
            if result:
                return self._to_entity(result[0])
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get user subscription for {user_id}: {e}")
            return None
    
    def get_user_subscription_history(self, user_id: int) -> List[Subscription]:
        """Get all subscriptions for a user."""
        options = QueryOptions(
            filters={'user_id': user_id},
            order_by=['-created_at']
        )
        result = self.list_all(options)
        return result.data
    
    def cancel_subscription(self, subscription_id: int, reason: str = "user_request",
                          immediate: bool = False) -> Subscription:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: Subscription ID
            reason: Reason for cancellation
            immediate: Whether to cancel immediately or at period end
            
        Returns:
            Updated Subscription
        """
        subscription = self.get_by_id_or_raise(subscription_id)
        
        if subscription.status in [SubscriptionStatus.CANCELED.value, SubscriptionStatus.EXPIRED.value]:
            raise ValidationError("Subscription is already canceled")
        
        now = datetime.utcnow()
        subscription.canceled_at = now
        subscription.cancellation_reason = reason
        
        if immediate:
            subscription.status = SubscriptionStatus.CANCELED.value
            subscription.ends_at = now
        else:
            # Cancel at end of current period
            subscription.ends_at = subscription.current_period_end or now
            # Keep status active until period ends
        
        updated_subscription = self.update(subscription)
        
        self.logger.info(f"Canceled subscription {subscription_id}", extra={
            "subscription_id": subscription_id,
            "user_id": subscription.user_id,
            "reason": reason,
            "immediate": immediate,
            "operation": "cancel_subscription"
        })
        
        return updated_subscription
    
    def reactivate_subscription(self, subscription_id: int) -> Subscription:
        """Reactivate a canceled subscription."""
        subscription = self.get_by_id_or_raise(subscription_id)
        
        if subscription.status not in [SubscriptionStatus.CANCELED.value, SubscriptionStatus.EXPIRED.value]:
            raise ValidationError("Only canceled or expired subscriptions can be reactivated")
        
        # Reset cancellation data
        subscription.canceled_at = None
        subscription.cancellation_reason = None
        subscription.ends_at = None
        subscription.status = SubscriptionStatus.ACTIVE.value
        
        # Set new billing period
        now = datetime.utcnow()
        plan = self.plan_repo.get_by_id_or_raise(subscription.plan_id)
        
        if plan.billing_cycle == BillingCycle.MONTHLY.value:
            next_billing = now + timedelta(days=30)
        elif plan.billing_cycle == BillingCycle.QUARTERLY.value:
            next_billing = now + timedelta(days=90)
        elif plan.billing_cycle == BillingCycle.YEARLY.value:
            next_billing = now + timedelta(days=365)
        else:  # LIFETIME
            next_billing = None
        
        subscription.current_period_start = now
        subscription.current_period_end = next_billing
        subscription.next_billing_date = next_billing
        subscription.next_payment_amount = plan.price
        
        updated_subscription = self.update(subscription)
        
        self.logger.info(f"Reactivated subscription {subscription_id}")
        return updated_subscription
    
    def upgrade_subscription(self, subscription_id: int, new_plan_id: int,
                           prorate: bool = True) -> Subscription:
        """
        Upgrade subscription to a new plan.
        
        Args:
            subscription_id: Current subscription ID
            new_plan_id: New plan ID
            prorate: Whether to prorate the charges
            
        Returns:
            Updated Subscription
        """
        subscription = self.get_by_id_or_raise(subscription_id)
        new_plan = self.plan_repo.get_by_id_or_raise(new_plan_id)
        
        if not subscription.is_active():
            raise ValidationError("Cannot upgrade inactive subscription")
        
        old_plan = self.plan_repo.get_by_id_or_raise(subscription.plan_id)
        
        # Update subscription
        subscription.plan_id = new_plan_id
        subscription.next_payment_amount = new_plan.price
        
        # If prorating, calculate immediate charge
        if prorate and subscription.next_billing_date:
            days_remaining = (subscription.next_billing_date - datetime.utcnow()).days
            if days_remaining > 0:
                # Calculate prorated amount (simplified)
                old_daily_rate = old_plan.price / 30  # Assuming monthly
                new_daily_rate = new_plan.price / 30
                proration_amount = (new_daily_rate - old_daily_rate) * days_remaining
                
                # Store proration info in metadata
                if not subscription.metadata:
                    subscription.metadata = {}
                subscription.metadata['upgrade_proration'] = {
                    'amount': float(proration_amount),
                    'days_remaining': days_remaining,
                    'old_plan_id': old_plan.id,
                    'new_plan_id': new_plan.id,
                    'upgrade_date': datetime.utcnow().isoformat()
                }
        
        updated_subscription = self.update(subscription)
        
        self.logger.info(f"Upgraded subscription {subscription_id} from plan {old_plan.id} to {new_plan.id}")
        return updated_subscription
    
    def process_subscription_renewals(self) -> List[Dict[str, Any]]:
        """
        Process subscription renewals for subscriptions due for billing.
        
        Returns:
            List of renewal results
        """
        try:
            # Get subscriptions due for renewal
            now = datetime.utcnow()
            
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE status = %(status)s 
                AND next_billing_date <= %(now)s
                AND next_billing_date IS NOT NULL
            """
            
            params = {
                'status': SubscriptionStatus.ACTIVE.value,
                'now': now
            }
            
            result = self.db.execute_query(query, params)
            
            renewal_results = []
            
            for row in result or []:
                subscription = self._to_entity(row)
                try:
                    # Process renewal
                    plan = self.plan_repo.get_by_id(subscription.plan_id)
                    if not plan:
                        continue
                    
                    # Update billing period
                    if plan.billing_cycle == BillingCycle.MONTHLY.value:
                        next_billing = subscription.next_billing_date + timedelta(days=30)
                    elif plan.billing_cycle == BillingCycle.QUARTERLY.value:
                        next_billing = subscription.next_billing_date + timedelta(days=90)
                    elif plan.billing_cycle == BillingCycle.YEARLY.value:
                        next_billing = subscription.next_billing_date + timedelta(days=365)
                    else:  # LIFETIME
                        next_billing = None
                    
                    subscription.current_period_start = subscription.next_billing_date
                    subscription.current_period_end = next_billing
                    subscription.next_billing_date = next_billing
                    subscription.last_payment_date = now
                    
                    self.update(subscription)
                    
                    renewal_results.append({
                        'subscription_id': subscription.id,
                        'user_id': subscription.user_id,
                        'status': 'success',
                        'amount': plan.price,
                        'next_billing_date': next_billing
                    })
                    
                except Exception as e:
                    self.logger.error(f"Failed to renew subscription {subscription.id}: {e}")
                    renewal_results.append({
                        'subscription_id': subscription.id,
                        'user_id': subscription.user_id,
                        'status': 'failed',
                        'error': str(e)
                    })
            
            self.logger.info(f"Processed {len(renewal_results)} subscription renewals")
            return renewal_results
            
        except Exception as e:
            self.logger.error(f"Failed to process subscription renewals: {e}")
            return []
    
    def expire_trials(self) -> int:
        """
        Expire trial subscriptions that have ended.
        
        Returns:
            Number of trials expired
        """
        try:
            now = datetime.utcnow()
            
            query = f"""
                UPDATE {self.table_name}
                SET status = %(expired_status)s,
                    ends_at = %(now)s
                WHERE status = %(trial_status)s 
                AND trial_end <= %(now)s
            """
            
            params = {
                'expired_status': SubscriptionStatus.EXPIRED.value,
                'trial_status': SubscriptionStatus.TRIAL.value,
                'now': now
            }
            
            self.db.execute_query(query, params)
            expired_count = self.db.get_affected_rows()
            
            if expired_count > 0:
                self.logger.info(f"Expired {expired_count} trial subscriptions")
            
            return expired_count
            
        except Exception as e:
            self.logger.error(f"Failed to expire trials: {e}")
            return 0
    
    def get_subscriptions_by_status(self, status: str, limit: Optional[int] = None) -> List[Subscription]:
        """Get subscriptions by status."""
        options = QueryOptions(
            filters={'status': status},
            limit=limit,
            order_by=['-created_at']
        )
        result = self.list_all(options)
        return result.data
    
    def get_expiring_subscriptions(self, days: int = 7) -> List[Subscription]:
        """Get subscriptions expiring in the next N days."""
        try:
            cutoff_date = datetime.utcnow() + timedelta(days=days)
            
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE status IN (%(active)s, %(trial)s)
                AND (
                    (trial_end IS NOT NULL AND trial_end <= %(cutoff)s) OR
                    (next_billing_date IS NOT NULL AND next_billing_date <= %(cutoff)s)
                )
                ORDER BY COALESCE(trial_end, next_billing_date)
            """
            
            params = {
                'active': SubscriptionStatus.ACTIVE.value,
                'trial': SubscriptionStatus.TRIAL.value,
                'cutoff': cutoff_date
            }
            
            result = self.db.execute_query(query, params)
            return [self._to_entity(row) for row in result] if result else []
            
        except Exception as e:
            self.logger.error(f"Failed to get expiring subscriptions: {e}")
            return []


class PaymentRepository(BaseRepository[Payment, int]):
    """Repository for payment management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "payments", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> Payment:
        """Convert database row to Payment entity."""
        return Payment(
            id=row.get('id'),
            subscription_id=row.get('subscription_id', 0),
            user_id=row.get('user_id', 0),
            amount=Decimal(str(row.get('amount', '0.00'))),
            currency=row.get('currency', 'USD'),
            status=row.get('status', PaymentStatus.PENDING.value),
            payment_method=row.get('payment_method'),
            transaction_id=row.get('transaction_id'),
            invoice_id=row.get('invoice_id'),
            payment_date=row.get('payment_date'),
            processed_at=row.get('processed_at'),
            failure_reason=row.get('failure_reason'),
            failure_code=row.get('failure_code'),
            refunded_amount=Decimal(str(row.get('refunded_amount', '0.00'))) if row.get('refunded_amount') else None,
            refunded_at=row.get('refunded_at'),
            refund_reason=row.get('refund_reason'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at'),
            metadata=row.get('metadata')
        )
    
    def _to_dict(self, entity: Payment) -> Dict[str, Any]:
        """Convert Payment entity to dictionary."""
        return {
            'id': entity.id,
            'subscription_id': entity.subscription_id,
            'user_id': entity.user_id,
            'amount': float(entity.amount),
            'currency': entity.currency,
            'status': entity.status,
            'payment_method': entity.payment_method,
            'transaction_id': entity.transaction_id,
            'invoice_id': entity.invoice_id,
            'payment_date': entity.payment_date,
            'processed_at': entity.processed_at,
            'failure_reason': entity.failure_reason,
            'failure_code': entity.failure_code,
            'refunded_amount': float(entity.refunded_amount) if entity.refunded_amount else None,
            'refunded_at': entity.refunded_at,
            'refund_reason': entity.refund_reason,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
            'metadata': entity.metadata
        }
    
    def _validate_entity(self, entity: Payment, is_update: bool = False) -> None:
        """Validate Payment entity."""
        if not entity.subscription_id:
            raise ValidationError("Subscription ID is required")
        
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if entity.amount <= 0:
            raise ValidationError("Payment amount must be positive")
        
        if entity.status not in [status.value for status in PaymentStatus]:
            raise ValidationError(f"Invalid payment status: {entity.status}")
    
    def create_payment(self, subscription_id: int, user_id: int, amount: Decimal,
                      payment_method: str, transaction_id: Optional[str] = None) -> Payment:
        """Create a new payment record."""
        payment = Payment(
            subscription_id=subscription_id,
            user_id=user_id,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            payment_date=datetime.utcnow()
        )
        
        return self.create(payment)
    
    def mark_payment_completed(self, payment_id: int, transaction_id: Optional[str] = None) -> Payment:
        """Mark payment as completed."""
        payment = self.get_by_id_or_raise(payment_id)
        payment.status = PaymentStatus.COMPLETED.value
        payment.processed_at = datetime.utcnow()
        if transaction_id:
            payment.transaction_id = transaction_id
        
        return self.update(payment)
    
    def mark_payment_failed(self, payment_id: int, failure_reason: str, 
                          failure_code: Optional[str] = None) -> Payment:
        """Mark payment as failed."""
        payment = self.get_by_id_or_raise(payment_id)
        payment.status = PaymentStatus.FAILED.value
        payment.failure_reason = failure_reason
        payment.failure_code = failure_code
        payment.processed_at = datetime.utcnow()
        
        return self.update(payment)
    
    def get_user_payments(self, user_id: int, limit: Optional[int] = None) -> List[Payment]:
        """Get payments for a user."""
        options = QueryOptions(
            filters={'user_id': user_id},
            limit=limit,
            order_by=['-created_at']
        )
        result = self.list_all(options)
        return result.data
    
    def get_subscription_payments(self, subscription_id: int) -> List[Payment]:
        """Get payments for a subscription."""
        options = QueryOptions(
            filters={'subscription_id': subscription_id},
            order_by=['-created_at']
        )
        result = self.list_all(options)
        return result.data


# Export all classes for easy importing
__all__ = [
    'SubscriptionStatus', 'BillingCycle', 'PaymentStatus',
    'SubscriptionPlan', 'Subscription', 'Payment', 'UsageRecord', 'SubscriptionAnalytics',
    'SubscriptionPlanRepository', 'SubscriptionRepository', 'PaymentRepository'
]
