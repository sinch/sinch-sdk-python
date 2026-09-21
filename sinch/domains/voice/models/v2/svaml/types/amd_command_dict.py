from typing import Literal, TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.svaml.types.amd_events_dict import (
    AmdEventsDict,
)


class AmdCommandDict(TypedDict):
    command: Literal["amd"]
    events: NotRequired[AmdEventsDict]
