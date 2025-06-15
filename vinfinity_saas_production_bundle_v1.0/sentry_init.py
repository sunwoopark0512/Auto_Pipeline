import sentry_sdk, os
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=0.25,
    release=os.getenv("GIT_SHA","dev")
)
