from datetime import datetime, timedelta


def get_next_datetime(
    target_day: int,
    target_hour: int,
    target_minute: int,
    timezone: str = "America/New_York",
) -> int:
    """
    Finds the next timestamp in the future in milliseconds that will have the given day of the week, hour,  and minute.

    Args:
        target_day (int): an int [0-6] mapping to Monday=0 through Sunday=6
        target_hour (int): an int giving the hour of a day [0-23]
        target_minute (int): an int giving the minute of an hour [0-59]
        timezone (str): a string representing the timezone to look for the next datetime in

    Returns:
        int: An integer representing the timestamp of the target datetime in milliseconds
    """
    # Get the current datetime
    now = datetime.now(tz=timezone)

    # Calculate the current week day, hour, and minute
    current_day = now.weekday()

    # Calculate the difference in days between now and the target day
    days_until_target = (target_day - current_day + 7) % 7

    # Create the target datetime for this week
    target_datetime = datetime(
        now.year, now.month, now.day, target_hour, target_minute, tzinfo=timezone
    ) + timedelta(days=days_until_target)

    # If the target datetime is in the past (earlier today or earlier this week), add 7 days to move it to next week
    if target_datetime <= now:
        target_datetime += timedelta(days=7)

    # return milliseconds
    return target_datetime.timestamp() * 1000
