from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# DB
from database.db_session import get_db

# Schemas
from schemas.habit_schema import (
    HabitCreate,
    HabitUpdateRequest,
    HabitResponse,
    DeleteHabitResponse,
)

# Services
from service.create_habit_service import create_habit
from service.update_habit_name_service import update_habit_name_service
from service.toggle_habit_completion_service import toggle_habit_completion_service
from service.delete_habit_service import delete_habit_service
from service.get_summary_service import get_habit_summary_service
from service.calculate_streak_service import calculate_streak_service
from service.streak_history_service import get_streak_history
from service.habit_history_service import get_habit_history_service
from service.get_today_logs_service import get_today_logs_service
from service.get_all_habits_service import get_all_habits

# Models
from model.habit import Habit

# Auth
from service.auth_dependency import get_current_user


router = APIRouter(prefix="/habits", tags=["Habits"])


# ---------------------------------------------------------
# CREATE HABIT
# ---------------------------------------------------------
@router.post("/", response_model=HabitResponse)
def add_habit(
    habit: HabitCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_habit(db, habit, user_id=user["id"])


# ---------------------------------------------------------
# UPDATE NAME OR TOGGLE COMPLETION (using user_habit_number)
# ---------------------------------------------------------
@router.put("/{user_habit_number}", response_model=HabitResponse)
def update_or_complete_habit(
    user_habit_number: int,
    payload: HabitUpdateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    # Case 1 → Update name
    if payload.name:
        result = update_habit_name_service(
            db=db,
            user_id=user["id"],
            user_habit_number=user_habit_number,
            new_name=payload.name
        )

        if not result:
            raise HTTPException(status_code=404, detail="Habit not found")

        return result

    # Case 2 → Toggle completion by date
    if payload.date:
        result = toggle_habit_completion_service(
            db=db,
            user_id=user["id"],
            user_habit_number=user_habit_number,
            date=payload.date,
        )

        if "error" in result:
            raise HTTPException(status_code=404, detail="Habit not found")

        return result

    raise HTTPException(status_code=400, detail="Invalid request data provided")


# ---------------------------------------------------------
# DELETE HABIT (fixed + consistent)
# ---------------------------------------------------------
@router.delete("/{user_habit_number}", response_model=DeleteHabitResponse)
def delete_habit(
    user_habit_number: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    deleted = delete_habit_service(
        db=db,
        user_habit_number=user_habit_number,
        user_id=user["id"]
    )

    if deleted is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    return DeleteHabitResponse(
        habit_id=deleted["habit_id"],
        user_habit_number=deleted["user_habit_number"],
        message="Habit deleted successfully"
    )


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
@router.get("/summary")
def get_habits_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_habit_summary_service(db, user["id"])


# ---------------------------------------------------------
# STREAK SUMMARY (clean + consistent)
# ---------------------------------------------------------
@router.get("/streak-summary")
def get_streak_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    habits = get_all_habits(db, user["id"])
    summary = []

    for habit in habits:
        current_streak = calculate_streak_service(
            db=db,
            habit_id=habit.id,
            user_id=user["id"]
        )

        rows = get_today_logs_service(db, habit.id, user["id"])
        completed_dates = [r[0] for r in rows]

        streak_history = get_streak_history(completed_dates)

        summary.append({
            "user_habit_number": habit.user_habit_number,
            "habit_name": habit.name,
            "current_streak": current_streak,
            "streak_history": streak_history,
            "last_completed": completed_dates[-1] if completed_dates else None,
            "total_streaks": len(streak_history)
        })

    return summary


# ---------------------------------------------------------
# FULL HABIT HISTORY
# ---------------------------------------------------------
@router.get("/{user_habit_number}/history")
def get_habit_history(
    user_habit_number: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    history = get_habit_history_service(
        db=db,
        user_habit_number=user_habit_number,
        user_id=user["id"]
    )

    if history is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    return history
