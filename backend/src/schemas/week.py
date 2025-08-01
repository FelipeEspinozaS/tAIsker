from pydantic import BaseModel
from database import date

class WeekSchema(BaseModel):
  id: int
  user_id: str
  start_date: date

  class Config:
    orm_mode = True