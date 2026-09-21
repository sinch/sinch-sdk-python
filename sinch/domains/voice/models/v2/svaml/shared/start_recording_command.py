from typing import Literal, Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.recording_events import (
    RecordingEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.recording_options import (
    RecordingOptions,
)


class StartRecordingCommand(BaseModelConfiguration):
    command: Literal["startRecording"] = Field(
        default="startRecording",
        description="Command to start recording on the channel",
    )
    recording_name: Optional[StrictStr] = Field(
        default=None,
        alias="recordingName",
        description="Identifier for this recording within the session. Must be unique across active recordings in the session.\n\nOther commands (e.g., `stopRecording`) reference this name to target a specific recording.\n\nSetting the recording name is useful for stopping the recording using the `stopRecording` command. If name is not set, recording can only be stopped when the call is disconnected.",
    )
    recording_options: RecordingOptions = Field(
        default=..., alias="recordingOptions"
    )
    events: Optional[RecordingEvents] = Field(default=None)
