from pydantic import BaseModel
from database import time

class AvailableSlotSchema(BaseModel):
  id: int
  week_id: int
  weekday: int # 0 = monday, 6 = Sunday
  start_time: time
  end_time: time

  class Config:
    orm_mode = True