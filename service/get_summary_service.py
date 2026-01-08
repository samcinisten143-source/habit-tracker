
from sqlalchemy.orm import Session

from service.get_all_habits_service import get_all_habits
from service.get_completed_today_service import get_completed_today_service
from service.get_pending_today_service import get_pending_today
from service.calculate_streak_service import calculate_streak_service


def get_habit_summary_service(db: Session, user_id: int):

    # 1. Fetch all habits
    habits = get_all_habits(db, user_id)
    total_habits = len(habits)

    # 2. Completed today — ensure integer
    completed_today = get_completed_today_service(db, user_id)
    completed_today = int(completed_today) if completed_today else 0

    # 3. Pending today
    pending_today = get_pending_today(total_habits, completed_today)

    # 4. Streaks for each habit
    streaks = [
        {
            "id": habit.user_habit_number,
            "name": habit.name,
            "streak": calculate_streak_service(db, habit.id, user_id)
        }
        for habit in habits
    ]

    return {
        "summary": {
            "total_habits": total_habits,
            "completed_today": completed_today,
            "pending_today": pending_today,
        },
        "streaks": streaks,
    }
