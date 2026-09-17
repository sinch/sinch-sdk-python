from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    _SDK_TYPE_VALUE as _SDK_CALL_BEHAVIOR_TYPE_VALUE,
)
from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    _WIRE_TYPE_VALUE as _WIRE_CALL_BEHAVIOR_TYPE_VALUE,
)

_WIRE_EVENT_PREFIX = "call.webhook."
_SDK_EVENT_PREFIX = "call.customEvent."


def rename_wire_event_prefix(data):
    if isinstance(data, dict) and isinstance(data.get("event"), str):
        event = data["event"]
        if event.startswith(_WIRE_EVENT_PREFIX):
            data = {
                **data,
                "event": _SDK_EVENT_PREFIX + event[len(_WIRE_EVENT_PREFIX) :],
            }
    return data


def rename_wire_call_behavior_type(data, *, field):
    if not isinstance(data, dict):
        return data
    behavior = data.get(field)
    if (
        isinstance(behavior, dict)
        and behavior.get("type") == _WIRE_CALL_BEHAVIOR_TYPE_VALUE
    ):
        data = {
            **data,
            field: {**behavior, "type": _SDK_CALL_BEHAVIOR_TYPE_VALUE},
        }
    return data
