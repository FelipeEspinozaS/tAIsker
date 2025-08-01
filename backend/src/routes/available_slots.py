from fastapi import APIRouter, Depends, Request, Body, Query
from typing import List, Union
from sqlalchemy import Session
from src.utils.auth import authenticate_and_get_user_details
from src.database.db import get_db
from src.database.models import AvailableSlot
from src.schemas.available_slot import AvailableSlotSchema, AvailableSlotCreateSchema
from datetime import date

router = APIRouter(prefix="/available_slots", tags=["AvailableSlots"])

# POST /available_slots - Create one or multiple available slots
@router.post("/", response_model=Union[AvailableSlotSchema, List[AvailableSlotSchema]])
def create_available_slots(
  request: Request,
  slots: Union[AvailableSlotSchema, List[AvailableSlotCreateSchema]] = Body(...),
  db: Session = Depends(get_db)):

  user = authenticate_and_get_user_details(request)

  slot_list = slots if isinstance(slots, list) else [slots]
  created = []

  for slot in slot_list:
    db_slot = AvailableSlot(
      user_id=user["clerk_id"],
      date=slot.date,
      start_time=slot.start_time,
      end_time=slot.end_time
    )
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    created.append(db_slot)

  return created if isinstance(slots, list) else created[0]

# GET /available_slots?date=YYYY-MM-DD - Get all available slots for that date
@router.get("/", response_model=List[AvailableSlotSchema])
def get_available_slots(
  request: Request,
  date: date = Query(...),
  db: Session = Depends(get_db)):  
              
  user = authenticate_and_get_user_details(request)

  slots = (db.query(AvailableSlot).filter(
    AvailableSlot.user_id == user["clerk_id"],
    AvailableSlot.date == date
  ).all())
  
  return slots