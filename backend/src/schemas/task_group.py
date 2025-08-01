from pydantic import BaseModel
from typing import Optional

class TaskGroupSchema(BaseModel):
  id: int
  name: str
  description: Optional[str] = None

  class Config:
    orm_mode = True