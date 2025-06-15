from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider, BatchSpanProcessor

def setup_otel(service: str):
    provider = TracerProvider(resource=Resource.create({"service.name": service}))
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318"))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
