from __future__ import annotations
import json
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends, Query
from starlette.requests import Request
from aiolimiter import AsyncLimiter

LIMITER = AsyncLimiter(10, 1)  # 10 rps
API_KEYS = set(os.getenv("API_KEYS", "").split(","))
DATA = Path("data/generated_hooks.json")


def verify_key(req: Request):
    key = req.headers.get("X-API-KEY")
    if not key or key not in API_KEYS:
        raise HTTPException(status_code=401, detail="invalid api key")


app = FastAPI(title="Auto Pipeline API", version="0.4.1")


@app.get("/v1/keywords", dependencies=[Depends(verify_key)])
async def read_keywords(limit: int = Query(20, le=100)):
    async with LIMITER:
        if not DATA.exists():
            raise HTTPException(503, detail="data unavailable")
        rows = json.loads(DATA.read_text(encoding="utf-8"))[:limit]
        return {"count": len(rows), "items": rows}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
