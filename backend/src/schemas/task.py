from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta

class TaskCreateSchema(BaseModel):
  name: str
  type: str
  estimated_duration: Optional[timedelta]
  deadline: Optional[date]
  recurrence_rule: Optional[str]
  group_id: Optional[int]

class TaskSchema(TaskCreateSchema):
  id: int
  user_id: str

  class Config:
    orm_mode=True