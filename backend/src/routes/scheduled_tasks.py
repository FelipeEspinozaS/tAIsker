from fastapi import APIRouter, Depends, Request, Query
from typing import List
from sqlalchemy import Session
from datetime import date
from src.utils.auth import authenticate_and_get_user_details
from src.database.db import get_db
from src.database.models import ScheduledTask
from src.schemas.scheduled_task import ScheduledTaskSchema

router = APIRouter(prefix="/scheduled_tasks", tags=["ScheduledTasks"])

# GET /scheduled_tasks?date=YYYY-MM-DD - Get all scheduled tasks for that date
def get_scheduled_tasks(
    request: Request,
    date: date = Query(...),
    db: Session = Depends(get_db)):
  
  user = authenticate_and_get_user_details(request)

  tasks = db.query(ScheduledTask).filter(
    ScheduledTask.user_id == user["clerk_id"],
    ScheduledTask.date == date
  ).all()
  
  return tasks

# POST /scheduled_tasks - Create a new scheduled task

# PATCH /scheduled_tasks/{task_id} - Update a scheduled task