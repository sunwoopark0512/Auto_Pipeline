"""
Generate Google-style docstrings for any Python source file.

Usage (CLI):
    python cursor_chunk_doc_gen.py path/to/your_script.py
"""

import ast
import os
import argparse
from pathlib import Path

import openai

MODEL = "gpt-4o"          # 원하는 모델로 교체 가능
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class _DocStringInjector(ast.NodeTransformer):
    """AST NodeTransformer that inserts docstrings where missing."""

    def __init__(self, ask_fn):
        """
        Args:
            ask_fn: Callable[[str], str] – prompt → docstring 반환 함수
        """
        self.ask_fn = ask_fn
        super().__init__()

    # pylint: disable=invalid-name
    def visit_FunctionDef(self, node):  # noqa: N802
        self.generic_visit(node)
        return self._maybe_inject(node)

    def visit_AsyncFunctionDef(self, node):  # noqa: N802
        self.generic_visit(node)
        return self._maybe_inject(node)

    def visit_ClassDef(self, node):  # noqa: N802
        self.generic_visit(node)
        return self._maybe_inject(node)

    # --------------------------------------------------------------------- #
    # internal helpers
    # --------------------------------------------------------------------- #
    def _maybe_inject(self, node):
        if ast.get_docstring(node) is None:
            prompt = self._build_prompt(node)
            docstring = self.ask_fn(prompt)
            node.body.insert(0, ast.Expr(value=ast.Constant(docstring)))
        return node

    @staticmethod
    def _build_prompt(node):
        header = f"### Code ###\n{ast.unparse(node)}\n### End ###"
        return (
            "Generate a concise Google-style docstring (English) for the"
            " Python object below. Include Args / Returns / Raises sections"
            " only when meaningful.\n"
            f"{header}"
        )


def _ask_chatgpt(prompt: str) -> str:
    """Low-level OpenAI 호출 래퍼 (temperature=0)."""
    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY not set")
    rsp = openai.ChatCompletion.create(
        model=MODEL,
        api_key=OPENAI_API_KEY,
        messages=[
            {"role": "system", "content": "You are a senior Python docstring expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return rsp.choices[0].message.content.strip()


def generate_docstrings(source: str) -> str:
    """Return new source with docstrings injected where missing."""
    tree = ast.parse(source)
    injector = _DocStringInjector(_ask_chatgpt)
    tree = injector.visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def process_file(path: Path) -> Path:
    """Create <name>_docgen.py with generated docstrings."""
    src = path.read_text(encoding="utf-8")
    new_src = generate_docstrings(src)
    out_path = path.with_name(path.stem + "_docgen.py")
    out_path.write_text(new_src, encoding="utf-8")
    return out_path


def _cli():
    parser = argparse.ArgumentParser(description="Auto-generate docstrings")
    parser.add_argument("file", type=Path, help="Target Python file")
    args = parser.parse_args()
    out = process_file(args.file)
    print(f"✅ Docstring file created → {out}")


if __name__ == "__main__":
    _cli()

