from importlib import reload
from types import SimpleNamespace


def test_parse_generated_text_full():
    import notion_hook_uploader
    reload(notion_hook_uploader)
    text = (
        "후킹 문장1: 훅1\n"
        "후킹 문장2: 훅2\n"
        "블로그 초안: 문단1\n문단2\n문단3\n"
        "영상 제목:\n- 제목1\n- 제목2\n"
    )
    result = notion_hook_uploader.parse_generated_text(text)
    assert result["hook_lines"] == ["훅1", "훅2"]
    assert result["blog_paragraphs"] == ["문단1"]
    assert result["video_titles"] == ["제목2"]


def test_parse_generated_text_missing_sections():
    import notion_hook_uploader
    reload(notion_hook_uploader)
    text = "후킹 문장1: A\n후킹 문장2: B"
    result = notion_hook_uploader.parse_generated_text(text)
    assert result["hook_lines"] == ["A", "B"]
    assert result["blog_paragraphs"] == ["", "", ""]
    assert result["video_titles"] == ["", ""]


def test_page_exists(monkeypatch):
    import notion_hook_uploader
    reload(notion_hook_uploader)
    class DummyDB:
        def __init__(self, ret, raise_err=False):
            self.ret = ret
            self.raise_err = raise_err
        def query(self, **kwargs):
            if self.raise_err:
                raise ValueError("fail")
            return self.ret
    notion_hook_uploader.notion = SimpleNamespace(databases=DummyDB({"results": [{}]}))
    assert notion_hook_uploader.page_exists("kw") is True
    notion_hook_uploader.notion = SimpleNamespace(databases=DummyDB({"results": []}))
    assert notion_hook_uploader.page_exists("kw") is False
    notion_hook_uploader.notion = SimpleNamespace(databases=DummyDB({}, raise_err=True))
    assert notion_hook_uploader.page_exists("kw") is False


def test_filter_keywords():
    import keyword_auto_pipeline
    reload(keyword_auto_pipeline)
    entries = [
        {"keyword": "a", "source": "GoogleTrends", "score": 60, "growth": 1.3, "cpc": 1000},
        {"keyword": "b", "source": "GoogleTrends", "score": 50, "growth": 1.5, "cpc": 1000},
        {"keyword": "c", "source": "Twitter", "mentions": 30, "top_retweet": 50, "cpc": 1000},
        {"keyword": "d", "source": "Twitter", "mentions": 20, "top_retweet": 50, "cpc": 1000},
    ]
    result = keyword_auto_pipeline.filter_keywords(entries)
    assert {e["keyword"] for e in result} == {"a", "c"}

