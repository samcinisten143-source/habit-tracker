from datetime import date
from sqlalchemy.orm import Session
from model.habit_log import HabitLog
from model.habit import Habit


def get_completed_today_service(db: Session, user_id: int):
    today = date.today()

    logs = (
        db.query(HabitLog, Habit)
        .join(Habit, HabitLog.habit_id == Habit.id)
        .filter(
            HabitLog.user_id == user_id,
            HabitLog.date == today,
            HabitLog.completed.is_(True)
        )
        .all()
    )

    result = []
    for log, habit in logs:
        result.append({
            "habit_id": habit.id,
            "user_habit_number": habit.user_habit_number,
            "name": habit.name,
            "completed": True,
            "date": str(today)
        })

    return len(result)   # Return only count (int)
