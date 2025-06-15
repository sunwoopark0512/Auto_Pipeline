"""
v-Infinity 레포 Step-2: README / .env.sample / Dockerfile / 개선된 CI / CodeQL /
Dependabot / Docker-release 워크플로 등을 한 번에 생성합니다.
실행:  python enhance_repo.py
"""
from pathlib import Path
import textwrap
import datetime

ROOT = Path(".")
TODAY = datetime.date.today().isoformat()


def write(path: Path, content: str, mode="w"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print("📝", path)

# 1) README.md (Quick Start 블록 추가 — 이미 있으면 덧붙임)
readme_path = ROOT / "README.md"
quick_start = f"""
## 🚀 Quick Start ({TODAY})

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env  # 환경 변수 채우기
python run_pipeline.py --topic "테스트 키워드" --token $WORDPRESS_API_TOKEN
```
"""
if readme_path.exists():
    if "Quick Start" not in readme_path.read_text():
        with readme_path.open("a") as f:
            f.write(textwrap.dedent(quick_start))
        print("📝 README.md 에 Quick Start 블록을 추가했습니다.")
else:
    write(readme_path, f"# v-Infinity 프로젝트\n{quick_start}")

# 2) .env.sample
write(ROOT / ".env.sample", """
OPENAI_API_KEY=
WORDPRESS_API_TOKEN=
SLACK_WEBHOOK=
SUPABASE_URL=
SUPABASE_KEY=
""")

# 3) Dockerfile
write(ROOT / "Dockerfile", """
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
CMD ["python", "run_pipeline.py", "--topic", "hello-docker"]
""")

# 4) 개선된 CI (기존 ci-tests.yml 덮어쓰기)
write(ROOT / ".github/workflows/ci-tests.yml", """
name: CI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest]
        python-version: ["3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "${{ matrix.python-version }}"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('requirements.txt') }}
      - run: pip install -r requirements.txt
      - run: pytest -q
      - run: ruff .
""")

# 5) Docker 이미지 빌드 & 푸시(태그 릴리스 트리거)
write(ROOT / ".github/workflows/docker-release.yml", """
name: Docker Release

on:
  push:
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
""")

# 6) CodeQL 분석
write(ROOT / ".github/workflows/codeql-analysis.yml", """
name: CodeQL

on:
  push:
  pull_request:
  schedule:
    - cron: "0 3 * * 3"

jobs:
  analyze:
    uses: github/codeql-action/analyze@v3
    with:
      languages: python
""")

# 7) Dependabot
write(ROOT / ".github/dependabot.yml", """
version: 2
updates:

  package-ecosystem: "pip"
  directory: "/"
  schedule: { interval: "weekly" }
""")

print("✅ Step-2 파일 생성 완료. git add → commit → push 하면 CI·린트·Docker·CodeQL이 활성화됩니다.")
