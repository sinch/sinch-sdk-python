from typing import List

from typing_extensions import NotRequired, TypedDict

from sinch.domains.voice.models.v2.svaml.types.incoming_call_response_events_dict import (
    IncomingCallResponseEventsDict,
)
from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)


class SvamlInputDict(TypedDict):
    commands: List[SvamlCommandDict]
    call_name: NotRequired[str]
    events: NotRequired[IncomingCallResponseEventsDict]
