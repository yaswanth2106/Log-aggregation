from .schemas import LogCreate,LogStats
from . import crud
from sqlalchemy.orm import Session
from .database import get_db
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import Optional
from . import models
from app.cache import get_cache, set_cache
from app.worker import process_log
from app.auth import verify_api_key
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.main import active_connections
import json
from app.sampling import should_store_log


limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/logs")


@router.post("/logs")
@limiter.limit("100/minute")
async def create_log(
    request: Request,
    log: LogCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    new_log = crud.create_log(db, log)

    log_data = {
        "level": log.level,
        "message": log.message,
        "service": log.service_name
    }

    for connection in active_connections:
        await connection.send_text(json.dumps(log_data))

    return new_log


async def broadcast_log(log):

    for connection in active_connections:
        await connection.send_text(json.dumps(log))



@router.get("/logs")
def fetch_logs(
    service: str | None = Query(None),
    level: str | None = Query(None),
    start: datetime | None = Query(None),
    end: datetime | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    logs = crud.get_logs(
        db,
        service=service,
        level=level,
        start=start,
        end=end,
        page=page,
        limit=limit,
    )

    return {
        "page": page,
        "limit": limit,
        "count": len(logs),
        "data": logs,
    }

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    cache_key = "log_stats"

    cached = get_cache(cache_key)
    if cached:
        return cached

    stats = crud.get_log_stats(db)

    set_cache(cache_key, stats, ttl=60)

    return stats

@router.get("/logs/{log_id}")
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log



@router.get("/search")
def search_logs(q: str, db: Session = Depends(get_db)):

    logs = db.query(models.Log).filter(
        models.Log.message.contains(q)
    ).all()

    return logs