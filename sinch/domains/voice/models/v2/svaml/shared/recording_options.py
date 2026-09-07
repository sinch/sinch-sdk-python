from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.transcription_options import (
    TranscriptionOptions,
)
from sinch.domains.voice.models.v2.svaml.types.recording_destination_type import (
    RecordingDestinationType,
)
from sinch.domains.voice.models.v2.svaml.types.recording_format_type import (
    RecordingFormatType,
)
from sinch.domains.voice.models.v2.svaml.types.recording_type import (
    RecordingType,
)


class RecordingOptions(BaseModelConfiguration):
    format: Optional[RecordingFormatType] = Field(default=None)
    recording_type: Optional[RecordingType] = Field(
        default=None, alias="recordingType"
    )
    destination: RecordingDestinationType = Field(default=...)
    destination_url: StrictStr = Field(
        default=...,
        alias="destinationUrl",
        description="Destination URL for the recording.",
    )
    credentials: StrictStr = Field(
        default=..., description="Credentials to third party storage."
    )
    transcription_options: Optional[TranscriptionOptions] = Field(
        default=None, alias="transcriptionOptions"
    )
