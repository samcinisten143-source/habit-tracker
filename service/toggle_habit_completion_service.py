from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date
from model.habit_log import HabitLog
from model.habit import Habit

def toggle_habit_completion_service(
    db: Session,
    user_id: int,
    user_habit_number: int,
    date: date
):
    """
    Toggle (or create) the HabitLog for the habit identified by
    (user_id, user_habit_number) on the given date.
    Returns the unified response which includes user_habit_number.
    """

    # 1) Find the habit by user_habit_number (this is the frontend ID)
    habit = (
        db.query(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.user_habit_number == user_habit_number
        )
        .first()
    )

    if not habit:
        # raise HTTPException so router can return a proper 404
        raise HTTPException(status_code=404, detail="Habit not found")

    # 2) Find existing log for that day
    log = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit.id,
            HabitLog.user_id == user_id,
            HabitLog.date == date
        )
        .first()
    )

    # 3) Toggle or create
    if log:
        log.completed = not log.completed
    else:
        log = HabitLog(
            habit_id=habit.id,
            user_id=user_id,
            date=date,
            completed=True
        )
        db.add(log)

    # 4) Commit + refresh
    db.commit()
    db.refresh(log)

    # 5) Return unified payload (includes user_habit_number for frontend)
    return {
        "id": habit.id,                          # internal DB id
        "user_habit_number": habit.user_habit_number,  # frontend id
        "name": habit.name,
        "created_at": habit.created_at,
        "completed": log.completed,
        "date": str(date)
    }
