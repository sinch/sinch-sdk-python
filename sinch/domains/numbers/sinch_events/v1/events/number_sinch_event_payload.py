from typing import Annotated, Union

from pydantic import Discriminator, Tag, TypeAdapter

from sinch.domains.numbers.sinch_events.v1.events.active_number_sinch_event import (
    ActiveNumberSinchEvent,
)
from sinch.domains.numbers.sinch_events.v1.events.number_order_sinch_event import (
    NumberOrderSinchEvent,
)
from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event import (
    NumberSinchEvent,
)

_FALLBACK_TAG = "__other__"


def _resource_type_discriminator(value: object) -> str:
    if isinstance(value, dict):
        resource_type = value.get("resourceType", value.get("resource_type"))
    else:
        resource_type = getattr(value, "resource_type", None)

    if resource_type in ["ACTIVE_NUMBER", "NUMBER_ORDER"]:
        return resource_type
    else:
        return _FALLBACK_TAG


NumberSinchEventPayload = Annotated[
    Union[
        Annotated[ActiveNumberSinchEvent, Tag("ACTIVE_NUMBER")],
        Annotated[NumberOrderSinchEvent, Tag("NUMBER_ORDER")],
        Annotated[NumberSinchEvent, Tag(_FALLBACK_TAG)],
    ],
    Discriminator(_resource_type_discriminator),
]

NumberSinchEventAdapter: TypeAdapter = TypeAdapter(NumberSinchEventPayload)
