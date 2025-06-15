import unittest
from scripts.parse_failed_gpt import parse_generated_text, parse_entry


class ParseFailedGptTests(unittest.TestCase):
    def test_parse_generated_text(self):
        text = (
            "후킹 문장1: 첫번째 후킹\n"
            "후킹 문장2: 두번째 후킹\n"
            "블로그 초안:\n문단1\n문단2\n문단3\n"
            "영상 제목:\n제목1\n제목2"
        )
        parsed = parse_generated_text(text)
        self.assertEqual(parsed["hook_lines"], ["첫번째 후킹", "두번째 후킹"])
        self.assertEqual(parsed["blog_paragraphs"], ["문단1", "문단2", "문단3"])
        self.assertEqual(parsed["video_titles"], ["제목1", "제목2"])

    def test_parse_entry_without_generated_text(self):
        entry = {
            "keyword": "테스트 키워드",
            "hook_lines": ["a", "b"],
            "blog_paragraphs": ["c", "d", "e"],
            "video_titles": ["f", "g"],
        }
        parsed = parse_entry(entry)
        self.assertEqual(parsed["hook_lines"], ["a", "b"])
        self.assertEqual(parsed["blog_paragraphs"], ["c", "d", "e"])
        self.assertEqual(parsed["video_titles"], ["f", "g"])


if __name__ == "__main__":
    unittest.main()
