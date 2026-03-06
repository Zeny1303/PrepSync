from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateSlot(BaseModel):
    startTime: datetime
    duration: int
    skills: List[str]