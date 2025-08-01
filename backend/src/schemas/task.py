from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta

class TaskSchema(BaseModel):
  id: int
  user_id: str
  name: str
  type: str
  estimated_duration: Optional[timedelta]
  deadline: Optional[date]
  recurrence_rule: Optional[str]
  group_id: Optional[int]

  class Config:
    orm_mode=True