"""Utility helpers for OpenTelemetry tracing."""

import os
from contextlib import contextmanager

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


def start_span(name: str):
    """Start and return a span with optional dry-run attribute."""
    span = tracer.start_span(name)
    # DRY_RUN attribute makes it easy to filter traces in Datadog
    if os.getenv("DRY_RUN"):
        span.set_attribute("dry", True)
    return span


@contextmanager
def traced(name: str):
    """Context manager that automatically ends the span."""
    span = start_span(name)
    try:
        yield span
    finally:
        span.end()
