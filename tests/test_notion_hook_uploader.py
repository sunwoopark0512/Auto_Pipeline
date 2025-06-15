import os
os.makedirs('logs', exist_ok=True)
import notion_hook_uploader as nhu


def test_parse_generated_text():
    sample = (
        "후킹 문장1: 첫번째 문장\n"
        "후킹 문장2: 두번째 문장\n"
        "블로그 초안: 서론\n"
        "첫 문단 내용\n"
        "둘째 문단 내용\n"
        "셋째 문단 내용\n"
        "영상 제목:\n"
        "- 비디오제목1\n"
        "- 비디오제목2\n"
    )
    parsed = nhu.parse_generated_text(sample)
    assert parsed["hook_lines"] == ["첫번째 문장", "두번째 문장"]
    assert parsed["blog_paragraphs"] == ["서론"]
    assert parsed["video_titles"] == ["비디오제목2"]
