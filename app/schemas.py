from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Dict


class LogCreate(BaseModel):
    service_name: str
    level: str
    message: str
    timestamp: datetime


class LogResponse(LogCreate):
    id: int

    class Config:
        from_attributes = True
        model_config = ConfigDict(from_attributes=True)



class LogStats(BaseModel):
    total_logs: int
    levels: Dict[str, int]
    services: Dict[str, int]