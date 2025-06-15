import utils
from unittest.mock import MagicMock


def test_create_hook_page_builds_properties():
    notion = MagicMock()
    item = {
        "keyword": "test keyword",
        "parsed": {
            "hook_lines": ["h1", "h2"],
            "blog_paragraphs": ["p1", "p2", "p3"],
            "video_titles": ["v1", "v2"],
        },
    }
    utils.create_hook_page(notion, "dbid", item)
    notion.pages.create.assert_called_once()
    kwargs = notion.pages.create.call_args.kwargs
    assert kwargs["parent"]["database_id"] == "dbid"
    props = kwargs["properties"]
    assert props["키워드"]["title"][0]["text"]["content"] == "test keyword"
    assert "등록일" in props

