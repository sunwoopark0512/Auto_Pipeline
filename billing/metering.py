import datetime
from .stripe_hooks import create_subscription
from models.tenant import Tenant

# Placeholder for database session
from sqlalchemy.orm import Session

quota_limit = 0  # Example global limit


def record_usage(db: Session, api_key: str, tokens: int) -> None:
    """Record token usage for a tenant and trigger plan upgrade if exceeded."""
    tenant = db.query(Tenant).filter_by(api_key=api_key).first()
    if not tenant:
        return
    tenant.used += tokens
    tenant.updated_at = datetime.datetime.utcnow()
    db.commit()

    if tenant.used > tenant.quota and tenant.plan == "free":
        # Example upgrade logic
        create_subscription(tenant.stripe_customer_id, "pro_plan_price_id")
        tenant.plan = "pro"
        db.commit()
