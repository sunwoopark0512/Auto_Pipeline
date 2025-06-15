# -------------------- filename: pipeline_api.py ------------------------

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# 기존 모듈 import (앞서 만든 모듈 활용)
import content_formatter
import snippet_generator
import ab_variant_manager
import auto_insight
import podcast_creator
import graphic_generator
import osmu_analytics

app = FastAPI(title="v-Infinity Pipeline API", version="1.0")


# 기본 요청 모델
class JobRequest(BaseModel):
    table: str
    limit: Optional[int] = 5
    days: Optional[int] = 7


# --- Content Formatter ---
@app.post("/format/")
def format_content(req: JobRequest):
    try:
        # 실제에선 Supabase에서 가져오지만, 샘플 호출
        sample_row = {
            "title": "Sample Title",
            "content": (
                "This is a long content example that will be formatted "
                "for multiple channels."
            ),
        }
        result = {}
        for channel in ["youtube", "medium", "x", "tistory"]:
            formatted = content_formatter.format_for_channel(
                sample_row,
                channel,
            )
            result[channel] = formatted
        return {"formatted": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Snippet Generator ---
@app.post("/snippet/")
def snippet_gen(req: JobRequest):
    try:
        sample_row = {
            "title": "Sample Snippet",
            "content": (
                "This content will be used to generate snippets."
            ),
        }
        result = {}
        for channel in ["youtube", "medium", "x", "tistory"]:
            snippet = snippet_generator.generate_snippet(
                sample_row,
                channel,
            )
            result[channel] = snippet
        return {"snippets": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- A/B Variant Generator ---
@app.post("/variants/")
def variants_gen(req: JobRequest):
    try:
        ab_variant_manager.process_batch(
            req.table,
            req.limit,
            title_n=3,
            thumb_n=2,
        )
        return {"status": "A/B variants generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Insight Generator ---
@app.post("/insight/")
def insight_gen(req: JobRequest):
    try:
        auto_insight.generate_insight(
            req.table,
            req.days,
            os.getenv("NOTION_DB"),
        )
        return {"status": "Insight generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Podcast Generator ---
@app.post("/podcast/")
def podcast_gen(req: JobRequest):
    try:
        podcast_creator.process_batch(req.table, req.limit)
        return {"status": "Podcast batch processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Graphic Generator ---
@app.post("/graphic/")
def graphic_gen(req: JobRequest):
    try:
        graphic_generator.process_batch(req.table, req.limit)
        return {"status": "Graphic batch processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- OSMU Analytics ---
@app.post("/osmu/")
def osmu_calc(req: JobRequest):
    try:
        osmu_analytics.process(req.table, req.days, req.limit)
        return {"status": "OSMU analytics completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
