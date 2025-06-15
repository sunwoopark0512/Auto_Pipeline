import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from hook_generator import generate_hook_prompt  # noqa: E402


def test_generate_hook_prompt_basic():
    keyword = '테스트 키워드'
    prompt = generate_hook_prompt(keyword, '주제', '출처', 5, 1.2, 100)
    assert keyword in prompt
    assert '주제:' in prompt

