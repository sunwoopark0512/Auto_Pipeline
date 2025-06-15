from content_writer import generate_article


def test_generate_article():
    article = generate_article("keyword")
    assert "keyword" in article
