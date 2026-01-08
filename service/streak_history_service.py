from datetime import timedelta, date

def get_streak_history(completed_dates: list[date]):
    """
    Build streak segments from a list of completed habit dates.
    
    Returns a list of objects:
    [
        { "start": "2025-01-05", "end": "2025-01-10", "days": 6 },
        ...
    ]
    """

    if not completed_dates:
        return []

    # Remove duplicates + sort
    completed_dates = sorted(set(completed_dates))

    history = []
    streak_start = completed_dates[0]
    streak_end = completed_dates[0]
    streak_count = 1

    for i in range(1, len(completed_dates)):
        prev = completed_dates[i - 1]
        current = completed_dates[i]

        # If dates are consecutive → continue streak
        if current == prev + timedelta(days=1):
            streak_end = current
            streak_count += 1
        else:
            # Close previous streak
            history.append({
                "start": streak_start.isoformat(),
                "end": streak_end.isoformat(),
                "days": streak_count
            })

            # Start new streak
            streak_start = current
            streak_end = current
            streak_count = 1

    # Add the final streak block
    history.append({
        "start": streak_start.isoformat(),
        "end": streak_end.isoformat(),
        "days": streak_count
    })

    return history
