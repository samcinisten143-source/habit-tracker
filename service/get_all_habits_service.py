from sqlalchemy.orm import Session
from model.habit import Habit


def get_all_habits(db: Session, user_id: int):
    habits = (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .order_by(Habit.user_habit_number.asc())
        .all()
    )

    return habits
