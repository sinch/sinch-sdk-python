from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated, TypedDict

from sinch.domains.voice.models.v2.services.types.event_destination_configuration_dict import (
    EventDestinationConfigurationDict,
)
from sinch.domains.voice.models.v2.svaml.types.svaml_input_dict import (
    SvamlInputDict,
)


class NoneCallBehaviorDict(TypedDict):
    type: Literal["NONE"]


class EventDestinationCallBehaviorDict(TypedDict):
    type: Literal["EVENT_DESTINATION"]
    event_destination: EventDestinationConfigurationDict


class StaticCallBehaviorDict(TypedDict):
    type: Literal["STATIC"]
    static: SvamlInputDict


CallBehaviorDict = Annotated[
    Union[
        NoneCallBehaviorDict,
        EventDestinationCallBehaviorDict,
        StaticCallBehaviorDict,
    ],
    Field(discriminator="type"),
]
