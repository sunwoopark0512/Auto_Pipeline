from qa_filter import content_safety_check


def test_content_safety_check():
    assert content_safety_check("text")
