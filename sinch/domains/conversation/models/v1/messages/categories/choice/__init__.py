__all__ = [
    "ChoiceMessage",
    "ChoiceMessageField",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "ChoiceMessage":
        from sinch.domains.conversation.models.v1.messages.categories.choice.choice_message import (
            ChoiceMessage,
        )

        return ChoiceMessage
    if name == "ChoiceMessageField":
        from sinch.domains.conversation.models.v1.messages.categories.choice.choice_message_field import (
            ChoiceMessageField,
        )

        return ChoiceMessageField
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
