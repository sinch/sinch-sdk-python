from typing import Literal, TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.types.call_destination_dict import (
    CallDestinationDict,
)
from sinch.domains.voice.models.v2.svaml.types.call_events_dict import (
    CallEventsDict,
)
from sinch.domains.voice.models.v2.types.call_origin_dict import CallOriginDict


class DialCommandDict(TypedDict):
    command: Literal["dial"]
    call_name: NotRequired[str]
    from_: NotRequired[CallOriginDict]
    to: CallDestinationDict
    dial_timeout_duration_seconds: NotRequired[int]
    max_call_duration_seconds: NotRequired[int]
    events: NotRequired[CallEventsDict]
