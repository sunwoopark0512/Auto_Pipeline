import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import run_pipeline as rp


def test_run_script_missing(monkeypatch):
    monkeypatch.setattr(rp.os.path, 'exists', lambda p: False)
    assert rp.run_script('x.py') is False


def test_run_script_process_fail(monkeypatch):
    monkeypatch.setattr(rp.os.path, 'exists', lambda p: True)
    cp = rp.subprocess.CompletedProcess('cmd', 1, stdout='out', stderr='err')
    monkeypatch.setattr(rp.subprocess, 'run', lambda *a, **k: cp)
    assert rp.run_script('x.py') is False


def test_run_script_success(monkeypatch):
    monkeypatch.setattr(rp.os.path, 'exists', lambda p: True)
    cp = rp.subprocess.CompletedProcess('cmd', 0, stdout='done', stderr='')
    monkeypatch.setattr(rp.subprocess, 'run', lambda *a, **k: cp)
    assert rp.run_script('y.py') is True


def test_run_pipeline(monkeypatch):
    seq = []

    def fake_run(script):
        seq.append(script)
        return script != 'fail.py'

    monkeypatch.setattr(rp, 'PIPELINE_SEQUENCE', ['a.py', 'fail.py', 'b.py'])
    monkeypatch.setattr(rp, 'run_script', fake_run)
    rp.run_pipeline()
    assert seq == ['a.py', 'fail.py', 'b.py']
