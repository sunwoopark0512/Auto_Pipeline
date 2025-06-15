import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autopipe.opsgenie import _map_priority, TEAM_MAP, TEAM_DEFAULT


def test_gpt_priority():
    prio, team = _map_priority("gpt.api", "500")
    assert prio == "P1"
    assert team == TEAM_MAP["gpt"]


def test_notion_priority():
    prio, team = _map_priority("notion.api", "404")
    assert prio == "P2"
    assert team == TEAM_MAP["notion"]


def test_default_priority():
    prio, team = _map_priority("other", "error")
    assert prio == "P4"
    assert team == TEAM_DEFAULT
