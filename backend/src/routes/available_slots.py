from fastapi import APIRouter, Depends, Request, Query
from typing import List
from sqlalchemy import Session
from src.utils.auth import authenticate_and_get_user_details
from src.database.db import get_db
from src.database.models import Week, AvailableSlot
from src.schemas.available_slot import AvailableSlotSchema
from datetime import date

router = APIRouter(prefix="/available_slots", tags=["AvailableSlots"])

# POST /available_slots - Create available slots for the current week
@router.post("/", response_model=List[AvailableSlotSchema])
def create_slots(
  request: Request,
  slots: List[AvailableSlotSchema],
  db: Session = Depends(get_db)):

  user = authenticate_and_get_user_details(request)

  created_slots = []

  for slot in slots:
    # Ensure the week exists or create it if it doesn't
    week = (db.query(Week)
            .filter(Week.id == slot.week_id, Week.user_id == user["clerk_id"])
            .first())
    
    if not week:
      week = Week(
        user_id = user["clerk_id"],
        start_date = slot.start_date)
      db.add(week)
      db.commit()
      db.refresh(week)
    
    db_slot = AvailableSlot(
      week_id=week.id,
      weekday=slot.weekday,
      start_time=slot.start_time,
      end_time=slot.end_time
    )
    db.add(db_slot)
    created_slots.append(db_slot)

  db.commit()
  return created_slots

# GET /available_slots - Get all available slots for the current week
@router.get("/", response_model=List[AvailableSlotSchema])
def get_slots(
  request: Request,
  start_date: date = Query(...),
  db: Session = Depends(get_db)):  
              
  user = authenticate_and_get_user_details(request)

  week = (db.query(Week)
          .filter(Week.user_id == user["clerk_id"], Week.start_date == start_date)
          .first())
  
  if not week:
    return []

  slots = (db.query(AvailableSlot)
           .filter(AvailableSlot.week_id == week.id)
           .all())
  
  return slots