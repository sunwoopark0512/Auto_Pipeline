from __future__ import annotations

import os
from batch_log import auto_deployment_log
from slack_alert import send_slack_alert


def run_deployment_pipeline(module: str, env: str, version: str) -> None:
    """Run deployment steps and record results."""
    print(f"✅ {module} {env} 배포 시작 - 버전: {version}")

    auto_deployment_log(module, env, version)
    send_slack_alert(f"🚀 {module} {env} 배포 완료 - v{version}")


# Example invocation
if __name__ == "__main__":
    MODULE = os.getenv("DEPLOY_MODULE", "Backend API")
    ENV = os.getenv("DEPLOY_ENV", "Production")
    VERSION = os.getenv("DEPLOY_VERSION", "v1.0.0")
    run_deployment_pipeline(MODULE, ENV, VERSION)
