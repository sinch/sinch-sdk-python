__all__ = [
    "LocationMessage",
    "LocationMessageField",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "LocationMessage":
        from sinch.domains.conversation.models.v1.messages.categories.location.location_message import (
            LocationMessage,
        )

        return LocationMessage
    if name == "LocationMessageField":
        from sinch.domains.conversation.models.v1.messages.categories.location.location_message_field import (
            LocationMessageField,
        )

        return LocationMessageField
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
