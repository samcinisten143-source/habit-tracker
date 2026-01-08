from sqlalchemy.orm import Session
from model.habit_log import HabitLog
from datetime import date, timedelta


def calculate_streak_service(db: Session, habit_id: int, user_id: int):
    """
    Calculate the current streak for a specific habit.
    Streak counts only consecutive completed days up to the most recent day.
    """

    logs = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == user_id,
            HabitLog.completed == True
        )
        .order_by(HabitLog.date.desc())
        .all()
    )

    if not logs:
        return 0

    # Remove duplicates (safety) and sort descending
    unique_dates = sorted({log.date for log in logs}, reverse=True)

    streak = 1
    prev_date = unique_dates[0]

    for current in unique_dates[1:]:
        # Check if consecutive
        if current == prev_date - timedelta(days=1):
            streak += 1
            prev_date = current
        else:
            break

    return streak
