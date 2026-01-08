from datetime import date, timedelta
from sqlalchemy.orm import Session
from model.habit import Habit
from model.habit_log import HabitLog


def get_habit_history_service(db: Session, user_habit_number: int, user_id: int):

    today = date.today()

    #Fetch the habit using user_habit_number (NOT habit.id)
    habit = (
        db.query(Habit)
        .filter(
            Habit.user_habit_number == user_habit_number,
            Habit.user_id == user_id
        )
        .first()
    )

    if not habit:
        return {
            "message": "Habit not found",
            "history": []
        }

    #Fetch completed logs for this habit using habit.id
    log_rows = (
        db.query(HabitLog.date)
        .filter(
            HabitLog.habit_id == habit.id,       # logs use REAL id
            HabitLog.user_id == user_id,
            HabitLog.completed == True
        )
        .order_by(HabitLog.date.asc())
        .all()
    )

    completed_dates = {row[0] for row in log_rows}

    # Build timeline
    start_date = habit.created_at.date()
    end_date = today

    history = []
    current = start_date

    while current <= end_date:
        history.append({
            "date": current,
            "completed": current in completed_dates
        })
        current += timedelta(days=1)

    return {
        "habit_id": user_habit_number,      # send user_habit_number back
        "habit_name": habit.name,
        "start_date": start_date,
        "end_date": end_date,
        "total_days": len(history),
        "completed_days": len(completed_dates),
        "completion_percentage": (
            (len(completed_dates) / len(history)) * 100 if history else 0
        ),
        "history": history
    }
