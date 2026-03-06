import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("log_service")
logger.setLevel(logging.INFO)

logHandler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s %(service)s %(trace_id)s"
)

logHandler.setFormatter(formatter)

logger.addHandler(logHandler)