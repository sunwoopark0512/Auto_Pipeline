import ast
import os
import openai

# SETUP: API 키는 환경변수로 관리
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"

class DocStringGenerator(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.parsed = ast.parse(source_code)

    def generate_docstrings(self):
        for node in ast.walk(self.parsed):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                docstring = self._create_docstring(node)
                if not ast.get_docstring(node):
                    node.body.insert(0, ast.Expr(value=ast.Str(docstring)))
        return ast.unparse(self.parsed)

    def _create_docstring(self, node):
        prompt = self._build_prompt(node)
        response = self._ask_gpt(prompt)
        return response.strip()

    def _build_prompt(self, node):
        signature = ast.unparse(node)
        return f"Generate a Google-style docstring for the following Python code:\n\n{signature}"

    def _ask_gpt(self, prompt):
        response = openai.ChatCompletion.create(
            model=MODEL,
            api_key=OPENAI_API_KEY,
            messages=[
                {"role": "system", "content": "You are a senior Python documentation expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    generator = DocStringGenerator(code)
    new_code = generator.generate_docstrings()
    output_path = file_path.replace(".py", "_docgen.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_code)
    print(f"Docstring generated: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate docstrings for a Python file")
    parser.add_argument("file_path", help="Path to the Python file")
    args = parser.parse_args()
    process_file(args.file_path)
