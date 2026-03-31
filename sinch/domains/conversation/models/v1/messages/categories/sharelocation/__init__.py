__all__ = [
    "ShareLocationMessage",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "ShareLocationMessage":
        from sinch.domains.conversation.models.v1.messages.categories.sharelocation.share_location_message import (
            ShareLocationMessage,
        )

        return ShareLocationMessage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
