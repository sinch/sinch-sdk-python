from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class EventDestinationConfiguration(BaseModelConfiguration):
    url: StrictStr = Field(default=...)
    fallback_url: Optional[StrictStr] = Field(
        default=None, alias="fallbackUrl"
    )
