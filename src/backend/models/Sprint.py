from datetime import datetime
from pydantic import BaseModel

class Sprint(BaseModel):
    tfs_number: str
    name: str
    starting_date: datetime
    ending_date: datetime
    