__all__ = [
    "CarouselMessage",
    "CarouselMessageField",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "CarouselMessage":
        from sinch.domains.conversation.models.v1.messages.categories.carousel.carousel_message import (
            CarouselMessage,
        )

        return CarouselMessage
    if name == "CarouselMessageField":
        from sinch.domains.conversation.models.v1.messages.categories.carousel.carousel_message_field import (
            CarouselMessageField,
        )

        return CarouselMessageField
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
