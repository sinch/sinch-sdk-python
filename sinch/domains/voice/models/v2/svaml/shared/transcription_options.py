from typing import Optional

from pydantic import Field, StrictBool, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class TranscriptionOptions(BaseModelConfiguration):
    is_enabled: StrictBool = Field(
        default=...,
        alias="isEnabled",
        description="If true, the recording will be transcribed to text.",
    )
    locale: Optional[StrictStr] = Field(
        default=None, description="Language code in BCP-47 format."
    )
