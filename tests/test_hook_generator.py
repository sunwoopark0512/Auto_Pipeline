from hook_generator import generate_hook_prompt


def test_generate_hook_prompt_contains_fields():
    prompt = generate_hook_prompt('키워드', 'topic', 'Google', 80, 1.4, 100)
    assert '키워드' in prompt
    assert 'Google' in prompt
    assert '80' in prompt
    assert '1.4' in prompt
    assert '100' in prompt
