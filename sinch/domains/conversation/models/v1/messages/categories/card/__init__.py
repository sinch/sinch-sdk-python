__all__ = [
    "CardMessage",
    "CardMessageField",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "CardMessage":
        from sinch.domains.conversation.models.v1.messages.categories.card.card_message import (
            CardMessage,
        )

        return CardMessage
    if name == "CardMessageField":
        from sinch.domains.conversation.models.v1.messages.categories.card.card_message_field import (
            CardMessageField,
        )

        return CardMessageField
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
