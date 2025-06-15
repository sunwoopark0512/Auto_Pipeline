import os
from batch_log import auto_deployment_log
from slack_alert import send_slack_alert

def run_deployment_pipeline(module, env, version):
    print(f"✅ {module} {env} 배포 시작 - 버전: {version}")

    auto_deployment_log(module, env, version)

    send_slack_alert(f"🚀 {module} {env} 배포 완료 - v{version}")
