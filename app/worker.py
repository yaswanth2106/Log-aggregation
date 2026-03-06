from celery_worker import celery
from app.database import SessionLocal
from app import models

@celery.task
def process_log(log_data):

    db = SessionLocal()

    log = models.Log(**log_data)

    db.add(log)
    db.commit()
    db.close()