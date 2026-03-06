from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.task_routes = {
    "app.worker.process_log": {"queue": "logs"}
}