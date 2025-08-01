from fastapi import APIRouter, Depends, Request
from typing import List
from sqlalchemy.orm import Session
from src.utils.auth import authenticate_and_get_user_details
from src.database.db import get_db
from src.database.models import TaskGroup
from src.schemas.task_group import TaskGroupSchema

router = APIRouter(prefix="/task_groups", tags=["TaskGroups"])

# GET /task_groups - Get all task groups
@router.get("/", response_model=List[TaskGroupSchema])
def get_task_groups(request: Request, db: Session = Depends(get_db)):
    return db.query(TaskGroup).all()

# POST /task_groups - Create a new task group
@router.post("/", response_model=TaskGroupSchema)
def create_task_group(
    request: Request,
    task_group: TaskGroupSchema,
    db: Session = Depends(get_db)
):    
    new_group = TaskGroup(
        name=task_group.name,
        description=task_group.description
    )
    
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group