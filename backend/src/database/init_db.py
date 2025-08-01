from src.database.db import engine
from src.database.models import Base

print("Creating tables (no reset)...")
Base.metadata.create_all(bind=engine)
print("Tables created.")