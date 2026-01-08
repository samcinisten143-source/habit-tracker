from datetime import date
from sqlalchemy.orm import Session
from model.habit import Habit
from model.habit_log import HabitLog


def get_all_habits_service(db: Session, user_id: int):
    """Return all habits for the user with today's completion status."""

    today = date.today()

    # Fetch all habits ordered by the user's habit numbering
    habits = (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .order_by(Habit.user_habit_number.asc())
        .all()
    )

    result = []

    for habit in habits:
        # Check today's completion status
        log = (
            db.query(HabitLog)
            .filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == user_id,
                HabitLog.date == today
            )
            .first()
        )

        result.append({
            "habit_id": habit.id,                         # REAL DB ID
            "user_habit_number": habit.user_habit_number, # UI numbering
            "name": habit.name,
            "created_at": habit.created_at,
            "completed_today": log.completed if log else False
        })

    return result
