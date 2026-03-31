__all__ = [
    "UrlMessage",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "UrlMessage":
        from sinch.domains.conversation.models.v1.messages.categories.url.url_message import (
            UrlMessage,
        )

        return UrlMessage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
