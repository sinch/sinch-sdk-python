__all__ = [
    "CallMessage",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "CallMessage":
        from sinch.domains.conversation.models.v1.messages.categories.call.call_message import (
            CallMessage,
        )

        return CallMessage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
