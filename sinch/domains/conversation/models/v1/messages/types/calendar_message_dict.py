from typing import TypedDict
from typing_extensions import NotRequired


class CalendarMessageDict(TypedDict):
    title: str
    event_start: str
    event_end: str
    event_title: str
    fallback_url: str
    event_description: NotRequired[str]
