from pydantic import BaseModel
from datetime import date, time

class ScheduledTaskSchema(BaseModel):
  id: int
  task_id: int
  user_id: str
  date: date
  start_time: time
  end_time: time
  manually_modified: bool = False

  class Config:
    orm_mode = True