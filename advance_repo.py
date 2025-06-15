"""
Step-3: \ucf00\ubc84\ub9ac\uc9c0(Codecov) \b7 Sphinx \ubb38\uc11c \b7 PR/Issue \ud15c\ud50c\ub9bf \b7
Docker Compose(Postgres+Supabase Stub) \uc790\ub3d9 \uc0dd\uc131 \uc2a4\ud06c\ub9bd\ud2b8.
\uc2e4\ud589:  python advance_repo.py
"""

from pathlib import Path
import textwrap, datetime

ROOT = Path(".")
TODAY = datetime.date.today().isoformat()

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print("📝", path)

# 1) .coveragerc
write(ROOT / ".coveragerc", """
[run]
branch = True
source = .
omit =
    tests/*
""")

# 2) GitHub workflow: coverage + Codecov
write(ROOT / ".github/workflows/coverage.yml", """
name: Coverage

on:
  push:
  pull_request:

jobs:
  cov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt coverage[toml] codecov
      - run: pytest --cov=./ --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
""")

# 3) Sphinx quick-start docs
docs_conf = """
project = 'v-Infinity'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
html_theme = 'furo'
"""
write(ROOT / "docs/conf.py", docs_conf)
write(ROOT / "docs/index.rst", """
v-Infinity Documentation
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
""")

# 4) GitHub Pages build workflow
write(ROOT / ".github/workflows/docs.yml", """
name: Docs

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt sphinx furo
      - run: sphinx-build -b html docs docs/_build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/_build
""")

# 5) Pull Request \ud15c\ud50c\ub9bf
write(ROOT / ".github/PULL_REQUEST_TEMPLATE.md", """
## \ubcc0\uacbd \uc0ac\ud56d
- 

## \ud14c\uc2a4\ud2b8
- [ ] \ub85c\uceec pytest \ud1b5\uacfc
- [ ] CI \ub17c\uc0b0 \ud655\uc778

## \uad00\ub828 \uc774\uc288
- closes #
""")

# 6) Issue \ud15c\ud50c\ub9bf
issue_tpl = """
name: Bug Report
description: \ubc84\uadf8\ub97c \uc2dc\uace0\ud574\uc8fc\uc138\uc694
title: "[Bug] "
labels: ["bug"]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: \ubb38\uc81c \uc124\uba85
      description: \ubc1c\uc0dd\ud55c \ubc84\uadf8\ub97c \uc790\uc138\ud788 \uc801\uc5b4\uc8fc\uc138\uc694
      placeholder: |
        1. ...
        2. ...
    validations:
      required: true
"""
write(ROOT / ".github/ISSUE_TEMPLATE/bug.yml", issue_tpl)

# 7) Docker Compose (Postgres + pgAdmin stub)
compose = """
version: "3.9"
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: supabase
    ports: ["5432:5432"]

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports: ["5050:80"]
"""
write(ROOT / "docker-compose.yml", compose)

print("\u2705 Step-3 \ud30c\uc77c \uc0dd\uc131 \uc644\ub8cc \u2014 git add/commit \ud6c4 push \ud558\uba74\n\u2022 Codecov \ucf00\ubc84\ub9ac\uc9c0 \uc5c5\ub85c\ub4dc\n\u2022 Sphinx \u2192 GitHub Pages \ube4c\ub4dc\n\u2022 PR/Issue \ud15c\ud50c\ub9bf \ud65c\uc131\ud654\n\u2022 docker-compose \ub85c \ub85c\uceec DB \uad6c\ubd84\uc774 \uac00\ub2a5\ud569\ub2c8\ub2e4.")
