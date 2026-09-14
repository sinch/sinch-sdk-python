from typing import Optional

from pydantic import Field, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class RecordingEvents(BaseModelConfiguration):
    on_finish: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onFinish",
        description="Commands to execute when the recording is successfully stopped. Note that this does not mean that the file is delivered to the configured destination yet.",
    )
    on_failure: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onFailure",
        description="Commands to execute if the recording fails to start. If omitted, failures are silently ignored and the call flow continues.",
    )
