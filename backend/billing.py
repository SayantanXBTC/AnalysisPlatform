import stripe
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import models
import config

stripe.api_key = config.STRIPE_SECRET_KEY

def create_checkout_session(user_email: str, price_id: str, success_url: str, cancel_url: str):
    """Create Stripe checkout session"""
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=user_email,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'user_email': user_email
            }
        )
        return checkout_session
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None

def handle_checkout_completed(session, db: Session):
    """Handle successful checkout"""
    try:
        user_email = session.get('customer_email') or session.get('metadata', {}).get('user_email')
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')
        
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if user:
            user.subscription_tier = "PRO"
            user.subscription_status = "active"
            user.stripe_customer_id = customer_id
            user.stripe_subscription_id = subscription_id
            user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
            user.updated_at = datetime.utcnow()
            db.commit()
            return True
    except Exception as e:
        print(f"Error handling checkout: {e}")
        db.rollback()
    return False

def handle_subscription_updated(subscription, db: Session):
    """Handle subscription updates"""
    try:
        customer_id = subscription.get('customer')
        status = subscription.get('status')
        
        user = db.query(models.User).filter(
            models.User.stripe_customer_id == customer_id
        ).first()
        
        if user:
            if status == 'active':
                user.subscription_status = "active"
                user.subscription_tier = "PRO"
            elif status in ['canceled', 'unpaid', 'past_due']:
                user.subscription_status = "inactive"
                user.subscription_tier = "FREE"
            
            user.updated_at = datetime.utcnow()
            db.commit()
            return True
    except Exception as e:
        print(f"Error handling subscription update: {e}")
        db.rollback()
    return False

def handle_subscription_deleted(subscription, db: Session):
    """Handle subscription cancellation"""
    try:
        customer_id = subscription.get('customer')
        
        user = db.query(models.User).filter(
            models.User.stripe_customer_id == customer_id
        ).first()
        
        if user:
            user.subscription_status = "inactive"
            user.subscription_tier = "FREE"
            user.updated_at = datetime.utcnow()
            db.commit()
            return True
    except Exception as e:
        print(f"Error handling subscription deletion: {e}")
        db.rollback()
    return False

def check_usage_limit(user: models.User) -> bool:
    """Check if user has exceeded usage limit"""
    # Reset monthly counter if needed
    now = datetime.utcnow()
    if user.last_reset_date.month != now.month or user.last_reset_date.year != now.year:
        user.analyses_this_month = 0
        user.last_reset_date = now
    
    # Check limits
    if user.subscription_tier == "PRO":
        return True  # Unlimited
    else:
        return user.analyses_this_month < config.FREE_TIER_LIMIT

def increment_usage(user: models.User, db: Session):
    """Increment user's usage counter"""
    user.analyses_this_month += 1
    user.updated_at = datetime.utcnow()
    db.commit()

def can_generate_pdf(user: models.User) -> bool:
    """Check if user can generate PDF"""
    return user.subscription_tier == "PRO"

def can_use_rag(user: models.User) -> bool:
    """Check if user can use RAG features"""
    return user.subscription_tier == "PRO"
