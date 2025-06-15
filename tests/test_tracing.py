import sys
from pathlib import Path
import time
from opentelemetry.trace import SpanContext, TraceFlags

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autopipe.tracing import LatencyFilterSpanProcessor, TH_MS


class DummySpan:
    def __init__(self, duration_ms: int):
        self.end_time = int(time.time() * 1e9)
        self.start_time = self.end_time - duration_ms * 1_000_000
        self.context = SpanContext(0x1, 0x1, False, TraceFlags(TraceFlags.SAMPLED))
        self.attributes = {}


class DummyExporter:
    def __init__(self):
        self.exported = []

    def export(self, spans):
        self.exported.extend(spans)
        return None


class DummyProcessor(LatencyFilterSpanProcessor):
    def __init__(self):
        self.exporter = DummyExporter()
        super().__init__(self.exporter)


def test_latency_filter_short_span():
    proc = DummyProcessor()
    span = DummySpan(duration_ms=TH_MS - 500)
    proc.on_end(span)
    assert proc.exporter.exported == []


