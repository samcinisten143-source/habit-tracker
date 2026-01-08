from sqlalchemy.orm import Session
from model.habit import Habit
from schemas.habit_schema import HabitCreate
from datetime import datetime


def create_habit(db: Session, habit: HabitCreate, user_id: int):

    # Get the highest user_habit_number for this user
    last_number = (
        db.query(Habit.user_habit_number)
        .filter(Habit.user_id == user_id)
        .order_by(Habit.user_habit_number.desc())
        .first()
    )

    # Assign next sequential number
    next_number = (last_number[0] + 1) if last_number else 1

    new_habit = Habit(
        name=habit.name,
        user_id=user_id,
        user_habit_number=next_number,
        created_at=datetime.utcnow()
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit
