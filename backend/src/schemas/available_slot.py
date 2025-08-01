from pydantic import BaseModel
from database import time, date

class AvailableSlotCreateSchema(BaseModel):
  start_date: date
  weekday: int  # 0 = Monday, 6 = Sunday
  start_time: time
  end_time: time

class AvailableSlotSchema(BaseModel):
  id: int
  week_id: int
  weekday: int # 0 = monday, 6 = Sunday
  start_time: time
  end_time: time

  class Config:
    orm_mode = True