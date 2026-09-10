from typing import List, TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)


class IncomingCallEventsDict(TypedDict):
    on_hangup: NotRequired[List[SvamlCommandDict]]
