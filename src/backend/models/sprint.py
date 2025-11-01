from datetime import date
from pydantic import BaseModel

class Sprint(BaseModel):
    id: int
    tfs_number: str
    code: str
    starting_date: date
    ending_date: date
    