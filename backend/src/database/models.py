from sqlalchemy import Column, Integer, String, Boolean, Date, Time, Interval, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class User(Base):
  __tablename__ = "users"
  id = Column(String, primary_key=True, index=True) # Clerk ID
  week_starts_on_sunday = Column(Boolean, default=False)

  weeks = relationship("Week", back_populates="user")
  tasks = relationship("Task", back_populates="user")

class Week(Base):
  __tablename__ = "weeks"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(String, ForeignKey("users.id"))
  start_date = Column(Date, nullable=False)

  user = relationship("User", back_populates="weeks")
  available_slots = relationship("AvailableSlot", back_populates="week")
  scheduled_tasks = relationship("ScheduledTask", back_populates="week")

class AvailableSlot(Base):
  __tablename__ = "available_slots"

  id = Column(Integer, primary_key=True, index=True)
  week_id = Column(Integer, ForeignKey("weeks.id"))
  weekday = Column(Integer) # 0: Monday, 6: Sunday
  start_time = Column(Time, nullable=False)
  end_time = Column(Time, nullable=False)

  week = relationship("Week", back_populates="available_slots")

class TaskGroup(Base):
  __tablename__ = "task_groups"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  description = Column(String, nullable=True)

  tasks = relationship("Task", back_populates="group")

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
  scheduled_tasks = relationship("ScheduledTask", back_populates="task")

class ScheduledTask(Base):
  __tablename__ = "scheduled_tasks"

  id = Column(Integer, primary_key=True, index=True)
  task_id = Column(Integer, ForeignKey("tasks.id"))
  week_id = Column(Integer, ForeignKey("weeks.id"))
  date = Column(Date, nullable=False)
  start_time = Column(Time, nullable=False)
  end_time = Column(Time, nullable=False)
  manually_modified = Column(Boolean, default=False)

  task = relationship("Task", back_populates="scheduled_tasks")
  week = relationship("Week", back_populates="scheduled_tasks")
