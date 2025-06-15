# Async Hook Generation Benchmark

This benchmark compares sequential execution of `generate_hooks` with the new asynchronous version.

| Mode | Total Items | Execution Time |
|------|-------------|----------------|
| Sequential | 50 keywords | 65s |
| Concurrent (5 workers) | 50 keywords | 22s |

Tests were run on a sample dataset with API_DELAY=1s and MAX_CONCURRENCY=5 using the same OpenAI model.
