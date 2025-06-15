import os
import sentry_sdk

RATE = float(os.getenv("TRACE_RATE", "0.05"))

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=RATE,
    profiles_sample_rate=min(RATE * 0.4, 0.1),
)
