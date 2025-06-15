"""Minimal webhook receiver for triggering pipeline components."""

import logging
import os
import subprocess

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # pylint: disable=no-name-in-module

app = FastAPI(title="v-Infinity Webhook Receiver")

# 기본 간단 인증 (Webhooks 보호용)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")


# 수신 요청 모델
class HookRequest(BaseModel):
    """Schema for webhook requests."""

    secret: str
    command: str  # 실행할 모듈명 ex: orchestrator, ab_variant_manager
    table: str = "content"
    limit: int = 5
    days: int = 7
    params: dict = {}


@app.post("/webhook/")
async def webhook(req: HookRequest):
    """Execute a pipeline command if the secret matches."""
    if req.secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 명령어 매핑
    command_map = {
        "orchestrator": "python orchestrator.py",
        "ab_variants": (
            "python ab_variant_manager.py --table"
            f" {req.table} --limit {req.limit} --title-variants 3 --thumb-variants 2"
        ),
        "rewriter": (
            f"python auto_rewriter.py --table {req.table} --threshold 0.3"
        ),
        "uploader": (
            f"python hook_uploader.py --table {req.table} --limit {req.limit}"
        ),
        "osmu": (
            f"python osmu_analytics.py --table {req.table} "
            f"--days {req.days} --limit {req.limit}"
        ),
        "graphic": (
            f"python graphic_generator.py --table {req.table} --limit {req.limit}"
        ),
        "podcast": (
            f"python podcast_creator.py --table {req.table} --limit {req.limit}"
        ),
        "insight": (
            f"python auto_insight.py --table {req.table} "
            f"--days {req.days} --notion-db $NOTION_DB_ID"
        ),
    }

    if req.command not in command_map:
        raise HTTPException(status_code=400, detail="Invalid command")

    command = command_map[req.command]
    logging.info("Webhook Triggered: %s", command)

    try:
        subprocess.Popen(command, shell=True)
        return {"status": "accepted", "executed": command}
    except Exception as e:  # noqa: W0718
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/")
async def health():
    """Simple health check."""
    return {"status": "alive"}


if __name__ == "__main__":
    uvicorn.run("webhook_receiver:app", host="0.0.0.0", port=9000)
