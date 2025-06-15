from datetime import datetime

from podcast.feed import Episode, Feed


def test_add_and_get_latest_episode():
    feed = Feed(title="My Podcast", description="Test")
    ep1 = Episode("E1", "e1.mp3", datetime(2023, 1, 1))
    ep2 = Episode("E2", "e2.mp3", datetime(2023, 1, 2))
    feed.add_episode(ep1)
    feed.add_episode(ep2)

    assert feed.get_latest_episode() == ep2
