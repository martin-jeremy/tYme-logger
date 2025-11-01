from pydantic import BaseModel
from datetime import datetime

class Log(BaseModel):
    task_id: int
    week_number: int
    log_date: datetime
    logged_time: float
    notes: str