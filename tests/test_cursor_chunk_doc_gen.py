import ast
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cursor_chunk_doc_gen import add_docstrings


def test_add_docstrings_inserts_function_docstring():
    source = """\
def foo(a, b):
    return a + b
"""
    updated = add_docstrings(source)
    tree = ast.parse(updated)
    func = tree.body[0]
    assert ast.get_docstring(func) is not None


def test_add_docstrings_inserts_class_docstring():
    source = """\
class Bar:
    def method(self):
        pass
"""
    updated = add_docstrings(source)
    tree = ast.parse(updated)
    cls = tree.body[0]
    assert ast.get_docstring(cls) is not None
