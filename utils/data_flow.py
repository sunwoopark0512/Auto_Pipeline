"""Data flow utilities for buffered IO and batch processing."""
from __future__ import annotations

from typing import Generator, Iterable, Tuple, TypeVar


def read_in_chunks(file_path: str, chunk_size: int = 1024) -> Generator[str, None, None]:
    """Yield file contents in blocks to save memory."""
    with open(file_path, "r", buffering=chunk_size) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


T = TypeVar("T")


def batched(iterable: Iterable[T], batch_size: int) -> Generator[Tuple[T, ...], None, None]:
    """Batch data from an iterable returning tuples."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield tuple(batch)
            batch = []
    if batch:
        yield tuple(batch)


def process_in_batches(data: Iterable[T], batch_size: int, processor) -> None:
    """Process data in batches with error handling."""
    for batch in batched(data, batch_size):
        try:
            processor(batch)
        except Exception as exc:  # pragma: no cover - processor is user-supplied
            log_batch_error(batch, exc)


def log_batch_error(batch: Tuple[T, ...], error: Exception) -> None:
    """Default error logger for batch processing."""
    print(f"Batch {batch} failed: {error}")

