from pathlib import Path
import json

from ai_self_heal.failure_replay import save_failure


def test_save_failure(tmp_path: Path) -> None:
    path = tmp_path / "buffer.jsonl"
    sample = {"prompt": "p", "completion": None, "error": "err"}
    save_failure(sample, path=path)

    data = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert data[0] == sample
