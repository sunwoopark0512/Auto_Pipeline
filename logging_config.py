import logging
from ddtrace import patch

patch(logging=True)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s %(message)s'
    )
