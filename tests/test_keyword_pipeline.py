import sys
import types

sys.modules.setdefault("pytrends", types.ModuleType("pytrends"))
sys.modules.setdefault(
    "pytrends.request", types.ModuleType("pytrends.request")
)
setattr(sys.modules["pytrends.request"], "TrendReq", object)

sys.modules.setdefault("snscrape", types.ModuleType("snscrape"))
sys.modules.setdefault(
    "snscrape.modules", types.ModuleType("snscrape.modules")
)
sys.modules.setdefault(
    "snscrape.modules.twitter", types.ModuleType("snscrape.modules.twitter")
)
setattr(
    sys.modules["snscrape.modules.twitter"],
    "TwitterSearchScraper",
    object,
)

from keyword_auto_pipeline import (  # noqa: E402
    filter_keywords,
    GOOGLE_TRENDS_MIN_SCORE,
    GOOGLE_TRENDS_MIN_GROWTH,
    TWITTER_MIN_MENTIONS,
    TWITTER_MIN_TOP_RETWEET,
    MIN_CPC,
)


def test_google_trends_threshold_pass():
    entry = {
        "keyword": "test",
        "source": "GoogleTrends",
        "score": GOOGLE_TRENDS_MIN_SCORE,
        "growth": GOOGLE_TRENDS_MIN_GROWTH,
        "cpc": MIN_CPC,
    }
    assert filter_keywords([entry]) == [entry]


def test_google_trends_threshold_fail_score():
    entry = {
        "keyword": "test",
        "source": "GoogleTrends",
        "score": GOOGLE_TRENDS_MIN_SCORE - 1,
        "growth": GOOGLE_TRENDS_MIN_GROWTH,
        "cpc": MIN_CPC,
    }
    assert filter_keywords([entry]) == []


def test_google_trends_threshold_fail_growth():
    entry = {
        "keyword": "test",
        "source": "GoogleTrends",
        "score": GOOGLE_TRENDS_MIN_SCORE,
        "growth": round(GOOGLE_TRENDS_MIN_GROWTH - 0.01, 2),
        "cpc": MIN_CPC,
    }
    assert filter_keywords([entry]) == []


def test_google_trends_fail_low_cpc():
    entry = {
        "keyword": "test",
        "source": "GoogleTrends",
        "score": GOOGLE_TRENDS_MIN_SCORE,
        "growth": GOOGLE_TRENDS_MIN_GROWTH,
        "cpc": MIN_CPC - 1,
    }
    assert filter_keywords([entry]) == []


def test_twitter_threshold_pass():
    entry = {
        "keyword": "test",
        "source": "Twitter",
        "mentions": TWITTER_MIN_MENTIONS,
        "top_retweet": TWITTER_MIN_TOP_RETWEET,
        "cpc": MIN_CPC,
    }
    assert filter_keywords([entry]) == [entry]


def test_twitter_fail_mentions():
    entry = {
        "keyword": "test",
        "source": "Twitter",
        "mentions": TWITTER_MIN_MENTIONS - 1,
        "top_retweet": TWITTER_MIN_TOP_RETWEET,
        "cpc": MIN_CPC,
    }
    assert filter_keywords([entry]) == []


def test_twitter_fail_top_retweet():
    entry = {
        "keyword": "test",
        "source": "Twitter",
        "mentions": TWITTER_MIN_MENTIONS,
        "top_retweet": TWITTER_MIN_TOP_RETWEET - 1,
        "cpc": MIN_CPC,
    }
    assert filter_keywords([entry]) == []


def test_twitter_fail_low_cpc():
    entry = {
        "keyword": "test",
        "source": "Twitter",
        "mentions": TWITTER_MIN_MENTIONS,
        "top_retweet": TWITTER_MIN_TOP_RETWEET,
        "cpc": MIN_CPC - 1,
    }
    assert filter_keywords([entry]) == []


def test_mixed_entries():
    google_entry_pass = {
        "keyword": "gpass",
        "source": "GoogleTrends",
        "score": GOOGLE_TRENDS_MIN_SCORE + 10,
        "growth": GOOGLE_TRENDS_MIN_GROWTH + 0.5,
        "cpc": MIN_CPC,
    }
    twitter_entry_fail = {
        "keyword": "tfail",
        "source": "Twitter",
        "mentions": TWITTER_MIN_MENTIONS - 5,
        "top_retweet": TWITTER_MIN_TOP_RETWEET,
        "cpc": MIN_CPC,
    }
    result = filter_keywords([google_entry_pass, twitter_entry_fail])
    assert result == [google_entry_pass]
