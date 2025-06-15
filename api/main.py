from fastapi import FastAPI, Depends, HTTPException, Header
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from typing import Annotated, List
import os
import json
import pathlib

Bearer = Annotated[str, Header(alias="X-API-Key")]

API_KEY = os.getenv("API_KEY", "changeme")
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

DATA_PATH = pathlib.Path(__file__).parent / "../data/generated_hooks.json"
if DATA_PATH.exists():
    DATA: List[str] = json.loads(DATA_PATH.read_text())
else:
    DATA = []


def _auth(api_key: Bearer) -> str:
    if api_key != API_KEY:
        raise HTTPException(401, "Invalid API key")
    return api_key


@app.get("/v1/keywords")
@limiter.limit("5/second")
async def keywords(q: str, _: str = Depends(_auth)) -> List[str]:
    return [kw for kw in DATA if q.lower() in kw.lower()][:20]


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}
