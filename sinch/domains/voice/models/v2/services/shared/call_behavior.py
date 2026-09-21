from typing import Literal, Union

from pydantic import Field, field_serializer
from typing_extensions import Annotated

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.services.shared.event_destination_configuration import (
    EventDestinationConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_input import SvamlInput


class NoneCallBehavior(BaseModelConfiguration):
    type: Literal["NONE"] = Field(default="NONE")


_WIRE_TYPE_VALUE = "WEBHOOK"
_SDK_TYPE_VALUE = "EVENT_DESTINATION"


class EventDestinationCallBehavior(BaseModelConfiguration):
    type: Literal[_SDK_TYPE_VALUE] = Field(default=_SDK_TYPE_VALUE)
    event_destination: EventDestinationConfiguration = Field(
        default=..., alias="webhook"
    )

    @field_serializer("type")
    def _serialize_type(self, _value: str) -> str:
        return _WIRE_TYPE_VALUE


class StaticCallBehavior(BaseModelConfiguration):
    type: Literal["STATIC"] = Field(default="STATIC")
    static: SvamlInput = Field(default=...)


CallBehavior = Annotated[
    Union[NoneCallBehavior, EventDestinationCallBehavior, StaticCallBehavior],
    Field(discriminator="type"),
]
