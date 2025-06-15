from pathlib import Path

def test_project_structure():
    '프로젝트 구조를 검증합니다.'
    required_dirs = ['src', 'tests', 'docs', 'scripts']
    for directory in required_dirs:
        assert Path(directory).exists(), f"{directory} 디렉토리가 없습니다"

def test_type_hints():
    'Type hints 지원을 검증합니다.'
    assert Path('src/py.typed').exists(), 'Type hints 지원 파일이 없습니다'
