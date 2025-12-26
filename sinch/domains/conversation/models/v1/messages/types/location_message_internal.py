from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.coordinates import (
    Coordinates,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class LocationMessageInternal(BaseModelConfigurationResponse):
    coordinates: Coordinates = Field(...)
    label: Optional[StrictStr] = Field(
        default=None, description="Label or name for the position."
    )
    title: StrictStr = Field(
        default=...,
        description="The title is shown close to the button or link that leads to a map showing the location. The title can be clickable in some cases.",
    )
