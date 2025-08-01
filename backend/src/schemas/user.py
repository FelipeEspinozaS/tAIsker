from pydantic import BaseModel

class UserSchema(BaseModel):
  id: str
  week_starts_on_sunday: bool = False

  class Config:
    orm_mode = True