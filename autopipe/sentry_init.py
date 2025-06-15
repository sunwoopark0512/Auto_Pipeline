import os
import sentry_sdk
from sentry_sdk import SamplingContext

ENV = os.getenv("APP_ENV", "prod")   # dev / qa / staging / prod


def _default_rate(env: str) -> float:
    return {"prod": 0.05, "staging": 0.20}.get(env, 1.0)


def _traces_sampler(ctx: SamplingContext) -> float:
    # root 트랜잭션만 평가
    if ctx.parent_sampling_decision is not None:
        return ctx.parent_sampling_decision
    name = ctx.transaction_context.get("name", "")
    if ENV == "prod" and name.startswith(("retry_", "dashboard_notifier")):
        return 0.005   # 0.5 %
    return _default_rate(ENV)


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sampler=_traces_sampler,
    profiles_sample_rate=0.02,
    environment=ENV,
    release=os.getenv("DD_VERSION", "0.4.2"),
)
