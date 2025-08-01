from pydantic import BaseModel

class UserSchema(BaseModel):
  id: str
  fullname: str
  email: str