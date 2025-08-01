from sqlalchemy import Column, Integer, String, Boolean, Date, Time, Interval, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class User(Base):
  __tablename__ = "users"
  id = Column(String, primary_key=True, index=True) # Clerk ID
  week_starts_on_sunday = Column(Boolean, default=False)

  available_slots = relationship("AvailableSlot", back_populates="user", cascade="all, delete-orphan")
  tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

class AvailableSlot(Base):
  __tablename__ = "available_slots"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(String, ForeignKey("users.id"))
  date = Column(Date, nullable=False)
  start_time = Column(Time, nullable=False)
  end_time = Column(Time, nullable=False)

  user = relationship("User", back_populates="available_slots")

class TaskGroup(Base):
  __tablename__ = "task_groups"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  description = Column(String, nullable=True)

  tasks = relationship("Task", back_populates="group", cascade="all, delete-orphan")

class Task(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(String, ForeignKey("users.id"))
  name = Column(String, nullable=False)
  type = Column(String, nullable=False)  # daily | general | periodic | groupable
  estimated_duration = Column(Interval, nullable=True)
  deadline = Column(Date, nullable=True)
  recurrence_rule = Column(String, nullable=True)
  group_id= Column(Integer, ForeignKey("task_groups.id"), nullable=True)

  user = relationship("User", back_populates="tasks")
  group = relationship("TaskGroup", back_populates="tasks")
  scheduled_tasks = relationship("ScheduledTask", back_populates="task", cascade="all, delete-orphan")

class ScheduledTask(Base):
  __tablename__ = "scheduled_tasks"

  id = Column(Integer, primary_key=True, index=True)
  task_id = Column(Integer, ForeignKey("tasks.id"))
  user_id = Column(String, ForeignKey("users.id"))
  date = Column(Date, nullable=False)
  start_time = Column(Time, nullable=False)
  end_time = Column(Time, nullable=False)
  manually_modified = Column(Boolean, default=False)

  task = relationship("Task", back_populates="scheduled_tasks")
  week = relationship("User")
