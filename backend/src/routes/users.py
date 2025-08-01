from fastapi import APIRouter, Depends, Request, Body, HTTPException
from sqlalchemy import Session
from src.utils.auth import authenticate_and_get_user_details
from src.database.models import User
from src.database.db import get_db
from src.schemas.user import UserSchema
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/users", tags=["users"])

# GET /users/me - Get the authenticated user's details
@router.get("/me", response_model=UserSchema)
def get_me(request: Request, db: Session = Depends(get_db)):
  user = authenticate_and_get_user_details(request)
  db_user = db.query(User).filter(User.id == user["clerk_id"]).first()
  
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")

  return db_user

# GET /users/ensure - Ensure the user exists in the database and create if not
@router.get("/ensure", response_model=UserSchema)
def ensure_user(request: Request, db: Session = Depends(get_db)):
  user = authenticate_and_get_user_details(request)

  db_user = db.query(User).filter(User.id == user["clerk_id"]).first()
  if not db_user:
    db_user = User(id=user["clerk_id"])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
  
  return db_user

# PATCH /users/me - Update the authenticated user's settings
@router.patch("/me", response_model=UserSchema)
def update_user_week_start(
  request: Request,
  week_starts_on_sunday: bool = Body(...),
  db: Session = Depends(get_db)
):
  user = authenticate_and_get_user_details(request)
  db_user = db.query(User).filter(User.id == user["clerk_id"]).first()

  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  
  db_user.week_starts_on_sunday = week_starts_on_sunday
  db.commit()
  db.refresh(db_user)
  return db_user

# GET /users/week_start_date
@router.get("/week_start_date")
def get_week_start_date(
  request: Request,
  db: Session = Depends(get_db)
):
  user = authenticate_and_get_user_details(request)
  db_user = db.query(User).filter(User.id == user["clerk_id"]).first()

  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")

  today = datetime.now(timezone.utc).date()
  weekday = today.weekday()  # Monday is 0, Sunday is 6
  if db_user.week_starts_on_sunday:
    # Sunday is 6 (so we need to handle Sunday as 0)
    days_to_subtract = (today.weekday() + 1) % 7
  else:
    days_to_subtract = weekday

  week_start = today - timedelta(days=days_to_subtract)
  return {"start_date": week_start}