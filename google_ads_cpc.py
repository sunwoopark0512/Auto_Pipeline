import os
import logging
from functools import lru_cache
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def _get_client() -> GoogleAdsClient:
    """Create Google Ads client using environment variables."""
    config = {
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
        "use_proto_plus": True,
    }
    missing = [k for k, v in config.items() if k != "login_customer_id" and not v]
    if missing:
        raise ValueError(f"Missing Google Ads credentials: {', '.join(missing)}")
    return GoogleAdsClient.load_from_dict(config)


@lru_cache(maxsize=128)
def fetch_cpc(keyword: str, customer_id: str | None = None) -> float:
    """Fetch average CPC for a keyword from Google Ads.

    Args:
        keyword: Keyword text to query.
        customer_id: Google Ads customer ID. If None, uses GOOGLE_ADS_CUSTOMER_ID.

    Returns:
        Average CPC in the account's currency as a float, or 0 if not found.
    """
    client = _get_client()
    ga_service = client.get_service("GoogleAdsService")
    customer_id = customer_id or os.getenv("GOOGLE_ADS_CUSTOMER_ID")
    if not customer_id:
        raise ValueError("GOOGLE_ADS_CUSTOMER_ID is not set")

    query = (
        "SELECT metrics.average_cpc FROM keyword_view "
        f"WHERE segments.keyword.text = '{keyword}' LIMIT 1"
    )
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            micros = row.metrics.average_cpc.micros
            return micros / 1_000_000
    except GoogleAdsException as exc:
        logging.error("Google Ads API error for %s: %s", keyword, exc)
    return 0.0
