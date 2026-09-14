from typing import Optional

from pydantic import Field, StrictBool, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.message import Message


class MenuPrompt(BaseModelConfiguration):
    allow_barge_in: Optional[StrictBool] = Field(
        default=None,
        alias="allowBargeIn",
        description="Controls whether input can interrupt prompt playback.\n\nWhen enabled, playback stops as soon as input is detected and the input is evaluated immediately if matching conditions are met.\n\nWhen disabled, input is still collected during playback and evaluated after playback finishes.",
    )
    messages: conlist(Message) = Field(
        default=..., description="Ordered list of messages to play."
    )
