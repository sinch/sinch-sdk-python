from typing import Any


def default_voice_configuration_type(value: Any) -> Any:
    """A missing ``type`` defaults to RTC."""
    if isinstance(value, dict) and not value.get("type"):
        return {**value, "type": "RTC"}
    return value
