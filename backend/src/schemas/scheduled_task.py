from pydantic import BaseModel
from datetime import date, time

class ScheduledTaskSchema(BaseModel):
  id: int
  task_id: int
  week_id: int
  date: date
  start_time: time
  end_time: time
  manually_modified: bool = False

  class Config:
    orm_mode = True