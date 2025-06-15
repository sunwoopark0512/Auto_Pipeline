import textwrap
from cursor_chunk_doc_gen import generate_docstrings


_SAMPLE = textwrap.dedent(
    '''
    def add(x, y):
        return x + y
    '''
)


def test_docstring_injection(monkeypatch):
    """Docstring가 삽입되는지 확인."""
    monkeypatch.setattr(
        "cursor_chunk_doc_gen._ask_chatgpt",
        lambda prompt: '"""Add two numbers.\n\nArgs:\n    x: int\n    y: int\n\nReturns:\n    int\n"""',
    )
    result = generate_docstrings(_SAMPLE)
    assert 'Add two numbers.' in result

