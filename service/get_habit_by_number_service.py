from sqlalchemy.orm import Session
from model.habit import Habit


def get_habit_by_number_service(db: Session, user_id: int, user_habit_number: int):
    """Fetch a habit using the user's habit number mapping."""

    habit = (
        db.query(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.user_habit_number == user_habit_number
        )
        .first()
    )

    return habit
