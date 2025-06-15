from fastapi import Request, HTTPException
from models.tenant import Tenant
from sqlalchemy.orm import Session


async def verify_api_key(request: Request, call_next):
    db: Session = request.state.db
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        raise HTTPException(status_code=403, detail="Missing API key")

    tenant = db.query(Tenant).filter_by(api_key=api_key, active=True).first()
    if not tenant:
        raise HTTPException(status_code=403, detail="Invalid API key")

    response = await call_next(request)
    return response
