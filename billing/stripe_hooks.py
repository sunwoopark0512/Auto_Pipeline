import stripe

stripe.api_key = "sk_live_xxx"


def create_customer(email: str) -> str:
    """Create a Stripe customer and return the customer id."""
    customer = stripe.Customer.create(email=email)
    return customer.id


def create_subscription(customer_id: str, price_id: str):
    """Create a subscription for the given customer."""
    return stripe.Subscription.create(customer=customer_id, items=[{"price": price_id}])
