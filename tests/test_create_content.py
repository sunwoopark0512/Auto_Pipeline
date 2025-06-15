import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.create_content import create_content

def test_create_content_output(capsys):
    create_content()
    captured = capsys.readouterr()
    assert "Creating content" in captured.out
    assert "Content created successfully" in captured.out
