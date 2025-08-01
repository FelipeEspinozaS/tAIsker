from fastapi import APIRouter, Depends, Request
from typing import List
from sqlalchemy.orm import Session
from src.utils.auth import authenticate_and_get_user_details
from src.database.db import get_db
from src.database.models import Task
from src.schemas.task import TaskSchema

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# POST /tasks - Create a new task for the authenticated user
@router.post("/", response_model=TaskSchema)
def create_task(
  request: Request,
  task: TaskSchema,
  db: Session = Depends(get_db)):

  user = authenticate_and_get_user_details(request)

  db_task = Task(
    user_id = user["clerk_id"],
    name = task.name,
    type = task.type,
    estimated_duration = task.estimated_duration,
    deadline = task.deadline,
    recurrence_rule = task.recurrence_rule,
    group_id = task.group_id
  )
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return db_task

# GET /tasks - Get all tasks for the authenticated user
@router.get("/", response_model=List[TaskSchema])
def get_tasks(request: Request, db: Session = Depends(get_db)):
  user = authenticate_and_get_user_details(request)

  tasks = (db.query(Task)
           .filter(Task.user_id == user["clerk_id"])
           .all())
  
  return tasks