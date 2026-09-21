from typing import Any, Optional


def discriminate_channel_credentials(value: Any) -> Optional[str]:
    """Resolve the Union tag from a channel-credentials payload or instance."""
    if isinstance(value, dict):
        return value.get("channel")
    return getattr(value, "channel", None)
