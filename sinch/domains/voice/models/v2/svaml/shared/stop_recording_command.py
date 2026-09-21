from typing import Literal

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class StopRecordingCommand(BaseModelConfiguration):
    command: Literal["stopRecording"] = Field(
        default="stopRecording",
        description="Command to stop recording on the channel",
    )
    recording_name: StrictStr = Field(
        default=...,
        alias="recordingName",
        description="Name of the recording to stop, as set by `recordingName` in the `startRecording` command.",
    )
