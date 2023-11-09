from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SensorData(BaseModel):
    sensor_id: int
    reading_type: str
    reading_value: float
    timestamp: datetime


class StatisticResponse(BaseModel):
    sensor_id: int
    reading_type: str
    min: float = None
    max: float = None
    avg: float = None
