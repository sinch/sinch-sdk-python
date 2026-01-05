__all__ = [
    "ListMessage",
    "ListMessageField",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "ListMessage":
        from sinch.domains.conversation.models.v1.messages.categories.list.list_message import (
            ListMessage,
        )

        return ListMessage
    if name == "ListMessageField":
        from sinch.domains.conversation.models.v1.messages.categories.list.list_message_field import (
            ListMessageField,
        )

        return ListMessageField
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
