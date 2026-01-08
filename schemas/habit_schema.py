from pydantic import BaseModel
import datetime
from typing import Optional


# -----------------------------
# Create Habit
# -----------------------------
class HabitCreate(BaseModel):
    name: str


# -----------------------------
# Update OR Complete Habit
# -----------------------------
class HabitUpdateRequest(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime.date] = None

    class Config:
        extra = "forbid"


# -----------------------------
# Habit Response
# Used for: Create, Update, Toggle
# -----------------------------
class HabitResponse(BaseModel):
    id: int                     # Database PK
    user_habit_number: int      # User-facing habit number
    name: str
    created_at: datetime.datetime

    # Only present when toggling
    completed: Optional[bool] = None
    date: Optional[str] = None

    class Config:
        from_attributes = True


# -----------------------------
# Streak Response
# -----------------------------
class StreakResponse(BaseModel):
    habit_id: int               # Database PK
    user_habit_number: int      # Custom habit number
    name: str
    streak_count: int
    last_completed_date: Optional[datetime.date] = None

    class Config:
        from_attributes = True


# -----------------------------
# Today Habit Response
# -----------------------------
class TodayHabitResponse(BaseModel):
    habit_id: int               # Database PK
    user_habit_number: int
    name: str
    completed: bool


# -----------------------------
# Delete Habit Response
# -----------------------------
class DeleteHabitResponse(BaseModel):
    habit_id: int
    user_habit_number: int
    message: str = "Habit deleted successfully"

    class Config:
        from_attributes = True
