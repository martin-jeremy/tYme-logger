from pydantic import BaseModel

class Task(BaseModel):
    tfs_number: str
    sprint_id: int
    project_id: int
    activity_id: int
    status: str
    assigned_to: str
    estimated_time: float
    resting_time: float
    done_time: float