from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from datetime import datetime
from .database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    level = Column(String, index=True)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

Index("idx_service_time", Log.service_name, Log.timestamp)