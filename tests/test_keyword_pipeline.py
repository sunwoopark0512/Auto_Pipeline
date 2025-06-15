import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import keyword_auto_pipeline as kap


def test_filter_keywords_google_trends():
    entries = [
        {
            "keyword": "kw1",
            "source": "GoogleTrends",
            "score": kap.GOOGLE_TRENDS_MIN_SCORE,
            "growth": kap.GOOGLE_TRENDS_MIN_GROWTH,
            "cpc": kap.MIN_CPC,
        },
        {
            "keyword": "kw2",
            "source": "GoogleTrends",
            "score": kap.GOOGLE_TRENDS_MIN_SCORE - 1,
            "growth": kap.GOOGLE_TRENDS_MIN_GROWTH,
            "cpc": kap.MIN_CPC,
        },
    ]

    result = kap.filter_keywords(entries)
    assert len(result) == 1
    assert result[0]["keyword"] == "kw1"


def test_filter_keywords_twitter():
    entries = [
        {
            "keyword": "kw1",
            "source": "Twitter",
            "mentions": kap.TWITTER_MIN_MENTIONS,
            "top_retweet": kap.TWITTER_MIN_TOP_RETWEET,
            "cpc": kap.MIN_CPC,
        },
        {
            "keyword": "kw2",
            "source": "Twitter",
            "mentions": kap.TWITTER_MIN_MENTIONS - 1,
            "top_retweet": kap.TWITTER_MIN_TOP_RETWEET,
            "cpc": kap.MIN_CPC,
        },
    ]

    result = kap.filter_keywords(entries)
    assert len(result) == 1
    assert result[0]["keyword"] == "kw1"


def test_run_pipeline_writes_output(tmp_path):
    out_file = tmp_path / "output.json"

    mock_gtrend = {
        "keyword": "topic sub",
        "source": "GoogleTrends",
        "score": kap.GOOGLE_TRENDS_MIN_SCORE + 10,
        "growth": kap.GOOGLE_TRENDS_MIN_GROWTH + 1,
        "cpc": kap.MIN_CPC,
    }

    mock_twitter = {
        "keyword": "topic sub",
        "source": "Twitter",
        "mentions": kap.TWITTER_MIN_MENTIONS + 10,
        "top_retweet": kap.TWITTER_MIN_TOP_RETWEET + 10,
        "cpc": kap.MIN_CPC,
    }

    with patch.object(kap, "TOPIC_DETAILS", {"topic": ["sub"]}), \
        patch.object(kap, "OUTPUT_PATH", str(out_file)), \
        patch.object(kap, "fetch_google_trends", return_value=mock_gtrend), \
        patch.object(kap, "fetch_twitter_metrics", return_value=mock_twitter):
        kap.run_pipeline()

    data = json.loads(out_file.read_text())
    assert data["filtered_keywords"] == [mock_gtrend, mock_twitter]
