from pydantic import BaseModel
from database import time, date

class AvailableSlotCreateSchema(BaseModel):
  date: date
  start_time: time
  end_time: time

class AvailableSlotSchema(AvailableSlotCreateSchema):
  id: int

  class Config:
    orm_mode = True