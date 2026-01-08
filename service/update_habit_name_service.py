from sqlalchemy.orm import Session
from fastapi import HTTPException
from model.habit import Habit


def update_habit_name_service(db: Session, habit_id: int, user_id: int, new_name: str):

    habit = (
        db.query(Habit)
        .filter(Habit.id == habit_id, Habit.user_id == user_id)
        .first()
    )

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Update the name
    habit.name = new_name
    db.commit()
    db.refresh(habit)

    # Unified return structure
    return {
        "id": habit.id,
        "user_habit_number": habit.user_habit_number,
        "name": habit.name,
        "created_at": habit.created_at,
        "completed": None,
        "date": None
    }
