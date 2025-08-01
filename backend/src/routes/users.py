from fastapi import APIRouter, Depends, Request
from src.utils.auth import authenticate_and_get_user_details
from src.schemas.user import UserSchema

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserSchema)
def get_me(request: Request):
  user = authenticate_and_get_user_details(request)
  return {
    "id": user["clerk_id"],
    "fullname": user["fullname"],
    "email": user["email"]
  }