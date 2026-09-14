from typing import TypedDict

from typing_extensions import NotRequired

from sinch.domains.voice.models.v2.svaml.types.recording_destination_type import (
    RecordingDestinationType,
)
from sinch.domains.voice.models.v2.svaml.types.recording_format_type import (
    RecordingFormatType,
)
from sinch.domains.voice.models.v2.svaml.types.recording_type import (
    RecordingType,
)
from sinch.domains.voice.models.v2.svaml.types.transcription_options_dict import (
    TranscriptionOptionsDict,
)


class RecordingOptionsDict(TypedDict):
    destination: RecordingDestinationType
    destination_url: str
    credentials: str
    format: NotRequired[RecordingFormatType]
    recording_type: NotRequired[RecordingType]
    transcription_options: NotRequired[TranscriptionOptionsDict]
