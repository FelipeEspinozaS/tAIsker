from pydantic import BaseModel, root_validator
from database import time, date

class AvailableSlotCreateSchema(BaseModel):
  date: date
  start_time: time
  end_time: time

  @root_validator
  def validate_times_renge(cls, values):
    start = values.get("start_time")
    end = values.get("end_time")
    if start and end and start >= end:
      raise ValueError("Start time must be before end time")
    
    return values

class AvailableSlotSchema(AvailableSlotCreateSchema):
  id: int

  class Config:
    orm_mode = True