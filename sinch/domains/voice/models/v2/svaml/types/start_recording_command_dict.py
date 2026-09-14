from typing import Literal, TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.svaml.types.recording_events_dict import (
    RecordingEventsDict,
)
from sinch.domains.voice.models.v2.svaml.types.recording_options_dict import (
    RecordingOptionsDict,
)


class StartRecordingCommandDict(TypedDict):
    command: Literal["startRecording"]
    recording_name: NotRequired[str]
    recording_options: RecordingOptionsDict
    events: NotRequired[RecordingEventsDict]
