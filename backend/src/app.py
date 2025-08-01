from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import users

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(users.router)

@app.get("/")
def root():
  return {"message": "Welcome to the tAIsker API!"}