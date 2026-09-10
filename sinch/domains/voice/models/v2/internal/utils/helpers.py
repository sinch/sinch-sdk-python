_WIRE_EVENT_PREFIX = "call.webhook."
_SDK_EVENT_PREFIX = "call.customEvent."


def rename_wire_event_prefix(data):
    if isinstance(data, dict) and isinstance(data.get("event"), str):
        event = data["event"]
        if event.startswith(_WIRE_EVENT_PREFIX):
            data = {
                **data,
                "event": _SDK_EVENT_PREFIX + event[len(_WIRE_EVENT_PREFIX):],
            }
    return data
