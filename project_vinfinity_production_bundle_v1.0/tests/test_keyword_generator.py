from keyword_generator import generate_keywords


def test_generate_keywords():
    keywords = generate_keywords("test")
    assert keywords == ["test example1", "test example2"]
