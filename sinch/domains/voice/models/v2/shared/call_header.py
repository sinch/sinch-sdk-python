from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class CallHeader(BaseModelConfiguration):
    key: StrictStr = Field(
        default=...,
        description="Name of the header. Must be 1-255 characters, using printable ASCII characters or tabs. Regex pattern: `[\\x20-\\x7e\\t]+$`.",
    )
    value: Optional[StrictStr] = Field(
        default=None,
        description="Value of the header. Must be at most 255 characters, using printable ASCII characters or tabs. Regex pattern: `[\\x20-\\x7e\\t]*$`.",
    )
