import os

os.environ['DRYRUN'] = 'true'

from Codex_Master_Automation_Module_v2_0.publishers.youtube_adapter import YouTubeAdapter
from Codex_Master_Automation_Module_v2_0.publishers.wordpress_adapter import WordPressAdapter
from Codex_Master_Automation_Module_v2_0.publishers.medium_adapter import MediumAdapter


def test_youtube_adapter_dryrun():
    adapter = YouTubeAdapter()
    url = adapter.publish({'title': 't', 'description': 'd', 'file_path': 'f.mp4'})
    assert url.startswith('dryrun://')


def test_wordpress_adapter_dryrun():
    adapter = WordPressAdapter()
    url = adapter.publish({'title': 't', 'body': 'b'})
    assert url.startswith('dryrun://')


def test_medium_adapter_dryrun():
    adapter = MediumAdapter()
    url = adapter.publish({'title': 't', 'body': 'b'})
    assert url.startswith('dryrun://')
