from sqlalchemy.orm import Session
from model.habit import Habit


def delete_habit_service(db: Session, user_habit_number: int, user_id: int):
    """
    Delete habit using user_habit_number (not id).
    """

    habit = (
        db.query(Habit)
        .filter(
            Habit.user_habit_number == user_habit_number,
            Habit.user_id == user_id
        )
        .first()
    )

    if habit is None:
        return None

    deleted_data = {
        "habit_id": habit.id,
        "user_habit_number": habit.user_habit_number,
        "name": habit.name,
        "created_at": habit.created_at
    }

    db.delete(habit)
    db.commit()

    return deleted_data
