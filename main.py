import sys
import os



# Allow import of service/, model/, routers/ without __init__.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from fastapi import FastAPI
from database.db_session import Base, engine
from routers import habit_router, auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Daily Habit Tracker")

app.include_router(auth_router.router)
app.include_router(habit_router.router)

@app.get("/")
def home():
    return {"message": "Welcome to Daily Habit Tracker!"}

