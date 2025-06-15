"""v-Infinity 최소 실행·품질 확보용 파일 세트 자동 생성 스크립트."""
import os, textwrap, pathlib, json

ROOT = pathlib.Path(".")
scripts_dir = ROOT / "scripts"
tests_dir = ROOT / "tests"
gh_dir = ROOT / ".github/workflows"

files: dict[str, str] = {
    "requirements.txt": """\
openai>=1.25.0
notion-client>=2.2.0
python-dotenv>=1.0.1
requests>=2.32.3
schedule>=1.2.1
pandas>=2.2.2
pytest>=8.2.0
pytest-mock>=3.14.0
ruff>=0.4.4
""",
    "scripts/parse_failed_gpt.py": """\
\"\"\"GPT 실패 로그(JSON)에서 status=='failed' 항목만 추출.\"\"\"
import json, pathlib, sys

def parse_fail_log(path: str):
    data = json.loads(pathlib.Path(path).read_text())
    return [item for item in data if item.get('status') == 'failed']

if __name__ == '__main__':
    print(json.dumps(parse_fail_log(sys.argv[1]), indent=2, ensure_ascii=False))
""",
    "scripts/notify_retry_result.py": """\
\"\"\"재시도 결과 summary(JSON)를 Slack Webhook으로 알림.\"\"\"
import os, json, requests, sys

HOOK = os.getenv('SLACK_WEBHOOK', '')

def notify(summary: dict):
    if not HOOK:
        print('⚠️  SLACK_WEBHOOK 미설정 – 알림 생략')
        return
    requests.post(HOOK, json={'text': f"✅ GPT 재시도 결과\n```{json.dumps(summary, indent=2, ensure_ascii=False)}```"})

if __name__ == '__main__':
    notify(json.loads(sys.stdin.read()))
""",
    "tests/test_pipeline_smoke.py": """\
import importlib, pytest

MODULES = ['keyword_generator', 'content_writer', 'editor_seo_optimizer', 'qa_filter', 'run_pipeline']

@pytest.mark.parametrize('mod', MODULES)
def test_imports(mod):
    importlib.import_module(mod)
""",
    ".ruff.toml": "line-length = 100\ntarget-version = 'py311'\nselect = ['E','F','I']\n",
    ".pre-commit-config.yaml": """\
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
""",
    ".github/workflows/ci-tests.yml": """\
name: CI Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -q
      - run: ruff .
""",
    ".github/workflows/codex-cleanup.yml": """\
name: Codex Branch Cleanup
on:
  schedule:
    - cron: '30 0 * * *'
  workflow_dispatch:
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Delete stale codex branches
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          set -euo pipefail
          api() { curl -s -H 'Authorization: Bearer $GITHUB_TOKEN' -H 'Accept: application/vnd.github+json' "$@"; }
          OWNER=${{ github.repository_owner }}
          REPO=${{ github.event.repository.name }}
          mapfile -t branches < <(api https://api.github.com/repos/$OWNER/$REPO/branches?per_page=100 | jq -r '.[].name' | grep '-codex/')
          for br in "${branches[@]}"; do
            pr_state=$(api https://api.github.com/repos/$OWNER/$REPO/pulls?state=all&head=$OWNER:$br | jq -r '.[0].state // empty')
            last_date=$(api https://api.github.com/repos/$OWNER/$REPO/commits/$br | jq -r '.commit.author.date')
            [[ "$pr_state" == 'closed' || "$(date -d "$last_date" +%s)" -lt $(date -d '7 days ago' +%s) ]] && api -X DELETE https://api.github.com/repos/$OWNER/$REPO/git/refs/heads/$br
          done
""",
    ".github/workflows/daily-pipeline.yml": """\
name: Daily Pipeline
on:
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *'
jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python run_pipeline.py --topic 'daily-keyword' --token $WORDPRESS_API_TOKEN
""",
}

# --- 파일 생성 ---
for path_str, content in files.items():
    path = ROOT / path_str
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content))

print("✅ 필요한 파일 9개를 생성했습니다. git add → commit 하면 CI가 바로 동작합니다.")
