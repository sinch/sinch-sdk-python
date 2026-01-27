from datetime import datetime
from typing import TypedDict
from typing_extensions import NotRequired


class CalendarMessageDict(TypedDict):
    title: str
    event_start: datetime
    event_end: datetime
    event_title: str
    fallback_url: str
    event_description: NotRequired[str]
