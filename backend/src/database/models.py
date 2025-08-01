from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from src.database.db import Base

class User(Base):
  __tablename__ = 'users'
  id = Column(String, primary_key=True, index=True) # Clerk ID
