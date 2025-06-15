import random
from phoenix.trace import set_trace_config

def sample_trace(trace):
    return random.random() < 0.01   # 1% 샘플

set_trace_config(should_trace=sample_trace)
