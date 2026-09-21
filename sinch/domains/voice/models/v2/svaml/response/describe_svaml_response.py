from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class DescribeSvamlResponse(BaseModelConfiguration):
    description: Optional[StrictStr] = Field(
        default=None,
        description="Human-readable description of the call flow.",
    )
