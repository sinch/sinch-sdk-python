from typing import Optional

from pydantic import Field, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class MessageEvents(BaseModelConfiguration):
    on_finish: Optional[conlist("SvamlCommand")] = Field(
        default=None,
        alias="onFinish",
        description="Commands to execute when all messages in the sequence have finished playing.",
    )
