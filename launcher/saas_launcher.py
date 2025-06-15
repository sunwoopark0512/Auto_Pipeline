"""Utility to create new SaaS instances from a template."""

import subprocess
import pathlib
import yaml

def launch_saas(template_file: str, saas_name: str) -> None:
    """Create a new SaaS instance from the given template."""
    with open(template_file, encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    repo_dir = pathlib.Path("./instances") / saas_name
    subprocess.run(["cp", "-r", "base_saas/", repo_dir], check=True)
    (repo_dir / "spec.yaml").write_text(yaml.dump(spec, allow_unicode=True))
    subprocess.run(["git", "-C", str(repo_dir), "init"], check=True)
    subprocess.run([
        "gh",
        "repo",
        "create",
        saas_name,
        "--public",
        "--source",
        str(repo_dir),
    ], check=True)
    print(f"✅ SaaS {saas_name} 생성 완료")

if __name__ == "__main__":
    launch_saas("templates/newsletter.yaml", "newsletter-ai-001")
