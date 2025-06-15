from __future__ import annotations
__doc__ = "OpenTelemetry tracing utilities with latency based export filter."

import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Span

_OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "https://api.datadoghq.com")
provider = TracerProvider()

TH_MS = int(os.getenv("LATENCY_THRESHOLD_MS", "2000"))  # 2 s default


class LatencyFilterSpanProcessor(BatchSpanProcessor):
    """Filter out spans shorter than threshold."""

    def on_end(self, span: Span) -> None:  # type: ignore[override]
        dur = (span.end_time - span.start_time) / 1e6  # ns -> ms
        if dur < TH_MS and span.attributes.get("force_export") is None:
            return
        super().on_end(span)


_exporter = OTLPSpanExporter(
    endpoint=_OTLP_ENDPOINT + "/api/v2/otlp",
    headers={"DD-API-KEY": os.getenv("DD_API_KEY", "")},
)

provider.add_span_processor(LatencyFilterSpanProcessor(_exporter))
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=_OTLP_ENDPOINT + "/api/v2/otlp",
            headers={"DD-API-KEY": os.getenv("DD_API_KEY", "")},
        )
    )
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
