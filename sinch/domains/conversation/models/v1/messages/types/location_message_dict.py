from typing import TypedDict
from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.coordinates_dict import (
    CoordinatesDict,
)


class LocationMessageDict(TypedDict):
    coordinates: CoordinatesDict
    title: str
    label: NotRequired[str]
