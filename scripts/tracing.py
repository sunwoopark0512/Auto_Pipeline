import os
from contextlib import contextmanager
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource.create({SERVICE_NAME: "v-infinity"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

@contextmanager
def start_span(name: str):
    with tracer.start_as_current_span(name) as span:
        if os.getenv("DRY_RUN"):
            span.set_attribute("dry", True)
        yield span
