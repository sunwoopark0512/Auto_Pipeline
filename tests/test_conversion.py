import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from content_converter import convert_content

class TestConversion(unittest.TestCase):
    def setUp(self):
        self.text = "테스트 글 제목\n본문 내용이 이어집니다."

    def test_facebook_template(self):
        result = convert_content(self.text, "facebook")
        self.assertIn("자세히 보기:", result)

    def test_linkedin_template(self):
        result = convert_content(self.text, "linkedin")
        self.assertIn("전문 읽기:", result)

if __name__ == '__main__':
    unittest.main()
