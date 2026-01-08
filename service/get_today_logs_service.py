from sqlalchemy.orm import Session
from model.habit_log import HabitLog


def get_today_logs_service(db: Session, habit_id: int, user_id: int):
    rows = (
        db.query(HabitLog.date)
        .filter(HabitLog.habit_id == habit_id, HabitLog.user_id == user_id, HabitLog.completed == True)
        .order_by(HabitLog.date)
        .all()
    )
    return rows
