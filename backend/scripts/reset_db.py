import os
import psycopg2
from sqlalchemy import create_engine
from src.database.models import Base
from src.config import DATABASE_URL, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def drop_and_create_db():
  print("Resetting the database...")

  # Temporal conection to the default database
  conn = psycopg2.connect(
      dbname="postgres",
      user=DB_USER,
      password=DB_PASSWORD,
      host=DB_HOST,
      port=DB_PORT
  )
  conn.autocommit = True
  cursor = conn.cursor()

  # End active connections to the target database
  cursor.execute(f"""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '{DB_NAME}' AND pid <> pg_backend_pid();
  """)

  # Delete and create the database
  cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
  cursor.execute(f"CREATE DATABASE {DB_NAME}")
  cursor.close()
  conn.close()
  print("Database reset complete.")

def create_tables():
  print("Creating tables...")
  engine = create_engine(DATABASE_URL)
  Base.metadata.create_all(bind=engine)
  print("Tables created successfully.")

if __name__ == "__main__":
  drop_and_create_db()
  create_tables()
