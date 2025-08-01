from fastapi import APIRouter, Depends, Request, Body
from typing import List, Union
from sqlalchemy.orm import Session
from src.utils.auth import authenticate_and_get_user_details
from src.database.db import get_db
from src.database.models import Task
from src.schemas.task import TaskSchema, TaskCreateSchema

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# POST /tasks - Create one or multiple tasks
@router.post("/", response_model=Union[TaskSchema, List[TaskSchema]])
def create_tasks(
  request: Request,
  tasks: Union[TaskCreateSchema, List[TaskCreateSchema]] = Body(...),
  db: Session = Depends(get_db)):

  user = authenticate_and_get_user_details(request)
  created_tasks = []

  task_list = tasks if isinstance(tasks, list) else [tasks]

  for task in task_list:
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
    created_tasks.append(db_task)

  return created_tasks if isinstance(tasks, list) else created_tasks[0]

# GET /tasks - Get all tasks for the authenticated user
@router.get("/", response_model=List[TaskSchema])
def get_tasks(request: Request, db: Session = Depends(get_db)):
  user = authenticate_and_get_user_details(request)

  tasks = (db.query(Task).filter(Task.user_id == user["clerk_id"]).all())
  return tasks