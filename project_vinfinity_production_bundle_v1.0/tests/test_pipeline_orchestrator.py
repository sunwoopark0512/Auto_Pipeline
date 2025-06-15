from pipeline_orchestrator import run_pipeline


def test_run_pipeline(capsys):
    run_pipeline("topic", "token")
    captured = capsys.readouterr()
    assert "Uploaded" in captured.out or "Rejected" in captured.out
