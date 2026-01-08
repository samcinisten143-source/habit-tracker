def count_today_status_service(habits, today_logs):
    logs_map = {log.habit_id: log for log in today_logs}

    completed_today = sum(
        1 for habit in habits
        if logs_map.get(habit.id) and logs_map[habit.id].completed
    )

    pending_today = len(habits) - completed_today

    return completed_today, pending_today, logs_map
