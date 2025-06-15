import os
import re
from contextlib import asynccontextmanager, contextmanager
from functools import lru_cache
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Span
from opentelemetry.sdk.trace.sampling import SamplingResult, Decision

# Environment variable for sampling environment
ENV = os.getenv("APP_ENV", "prod")

# ---------- Regex & Attr based decision ----------
_REGEX_LIST = [re.compile(r"^retry_"), re.compile(r"^dashboard_")]
_SPECIAL_ATTRS = {"retry", "backoff"}

# ---------- LRU Cache ----------
@lru_cache(maxsize=5000)
def _memo(trace_id: int, name: str, attrs_frozenset: frozenset, base_rate: float) -> float:
    """Memoize decision: reuse if TraceID+context same."""
    # Regex priority
    if any(r.match(name) for r in _REGEX_LIST):
        return 0.005
    # attribute in ..
    if _SPECIAL_ATTRS & attrs_frozenset:
        return 0.20
    return base_rate


def _default_rate(env: str) -> float:
    return {"prod": 0.05, "staging": 0.20}.get(env, 1.0)


def _traces_sampler(ctx):
    txn = ctx.transaction_context
    name = txn.get("name", "")
    attrs = txn.get("attributes", {})
    # reuse if parent exists
    if ctx.parent_sampling_decision is not None:
        return ctx.parent_sampling_decision
    trace_id = ctx.trace_id
    attrs_fset = frozenset(attrs.values())
    return _memo(trace_id, name, attrs_fset, _default_rate(ENV))
