from datetime import datetime


def timestamp_to_datetime_in_utc_deserializer(timestamp: str):
    return datetime.fromisoformat(timestamp + 'Z')
