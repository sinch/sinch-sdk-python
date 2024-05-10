from datetime import datetime


def timestamp_to_datetime_in_utc_deserializer(timestamp: str):
    """
    Older Python versions (like 3.9) do not support "Z" as a TZ information.
    One needs to use '+00:00' to represent UTC tz.
    """
    if timestamp.endswith("Z"):
        timestamp = timestamp[:-1]

    return datetime.fromisoformat(timestamp + "+00:00")
