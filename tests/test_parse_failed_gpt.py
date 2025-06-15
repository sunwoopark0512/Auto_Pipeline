import json
import os
import sys
import types

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Provide a dummy notion_client to satisfy imports
dummy_client = types.SimpleNamespace()
dummy_client.Client = lambda *args, **kwargs: object()
sys.modules.setdefault('notion_client', dummy_client)
os.makedirs('logs', exist_ok=True)

from notion_hook_uploader import parse_generated_text


def test_parse_failed_gpt(tmp_path, monkeypatch):
    failed = tmp_path / "failed_hooks.json"
    reparsed = tmp_path / "reparsed.json"

    text = "후킹 문장1: a\n후킹 문장2: b\n블로그 초안: x\ny\nz\n영상 제목: t1\n- t2"
    data = [{"keyword": "kw1", "generated_text": text}, {"keyword": "kw2"}]
    failed.write_text(json.dumps(data, ensure_ascii=False))

    monkeypatch.setenv("FAILED_HOOK_PATH", str(failed))
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(reparsed))
    from scripts import parse_failed_gpt  # import after env setup
    parse_failed_gpt.parse_failed_gpt()

    output = json.loads(reparsed.read_text())
    assert len(output) == 1
    assert output[0]["keyword"] == "kw1"
    assert output[0]["parsed"] == parse_generated_text(text)
