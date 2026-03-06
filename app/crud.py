from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import and_
from datetime import datetime
from sqlalchemy import func
from app.circuit import db_breaker



@db_breaker
def create_log(db: Session, log: schemas.LogCreate):
    db_log = models.Log(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(
    db: Session,
    service: str | None = None,
    level: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    page: int = 1,
    limit: int = 10,
):
    query = db.query(models.Log)

    if service:
        query = query.filter(models.Log.service_name == service)

    if level:
        query = query.filter(models.Log.level == level)

    if start:
        query = query.filter(models.Log.timestamp >= start)

    if end:
        query = query.filter(models.Log.timestamp <= end)

    offset = (page - 1) * limit

    logs = query.offset(offset).limit(limit).all()

    return logs



def get_log_stats(db, start=None, end=None):

    query = db.query(models.Log)

    if start:
        query = query.filter(models.Log.timestamp >= start)

    if end:
        query = query.filter(models.Log.timestamp <= end)

    total_logs = query.count()

    level_counts = (
        query.with_entities(
            models.Log.level,
            func.count(models.Log.id)
        )
        .group_by(models.Log.level)
        .all()
    )

    service_counts = (
        query.with_entities(
            models.Log.service_name,
            func.count(models.Log.id)
        )
        .group_by(models.Log.service_name)
        .all()
    )

    return {
        "total_logs": total_logs,
        "levels": dict(level_counts),
        "services": dict(service_counts),
    }