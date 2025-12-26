from typing import Union
from pydantic import Field, StrictFloat, StrictInt
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class Coordinates(BaseModelConfigurationResponse):
    latitude: Union[StrictFloat, StrictInt] = Field(
        default=..., description="The latitude."
    )
    longitude: Union[StrictFloat, StrictInt] = Field(
        default=..., description="The longitude."
    )
