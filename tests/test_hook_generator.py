import sys
import types

# Stub external dependencies before importing the module
sys.modules['dotenv'] = types.ModuleType('dotenv')
sys.modules['dotenv'].load_dotenv = lambda: None
sys.modules['openai'] = types.ModuleType('openai')

sys.path.insert(0, '.')
sys.path.insert(0, 'Auto_Pipeline')

import hook_generator


def test_generate_hook_prompt():
    prompt = hook_generator.generate_hook_prompt(
        keyword='테스트 키워드',
        topic='테스트',
        source='GoogleTrends',
        score=80,
        growth=2.0,
        mentions=100,
    )
    assert '테스트 키워드' in prompt
    assert 'GoogleTrends' in prompt
