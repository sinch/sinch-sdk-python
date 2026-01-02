__all__ = [
    "CalendarMessage",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "CalendarMessage":
        from sinch.domains.conversation.models.v1.messages.categories.calendar.calendar_message import (
            CalendarMessage,
        )

        return CalendarMessage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
