"""OpenTelemetry 초기화 & 스팬 헬퍼."""

import os
from contextlib import asynccontextmanager, contextmanager

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "https://api.datadoghq.com")
_SERVICE = os.getenv("DD_SERVICE", "autopipeline")
_ENV = os.getenv("DD_ENV", "prod")
_VERSION = os.getenv("DD_VERSION", "0.4.1")

resource = Resource.create(
    {
        SERVICE_NAME: _SERVICE,
        "deployment.environment": _ENV,
        "service.version": _VERSION,
    }
)
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint=_OTLP_ENDPOINT + "/api/v2/otlp",
        headers={"DD-API-KEY": os.getenv("DD_API_KEY", "")},
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


@contextmanager
def span(name: str, **attrs):
    """동기 코드에서 사용."""
    with tracer.start_as_current_span(name, attributes=attrs):
        yield


@asynccontextmanager
async def aspan(name: str, **attrs):
    """비동기 코드에서 사용."""
    with tracer.start_as_current_span(name, attributes=attrs):
        yield
