from typing import Annotated, Union
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.numbers.sinch_events.v1.events.active_number_sinch_event import (
    ActiveNumberSinchEvent,
)
from sinch.domains.numbers.sinch_events.v1.events.number_order_sinch_event import (
    NumberOrderSinchEvent,
)
from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event import (
    NumberSinchEvent,
)

NumberSinchEventPayload = Annotated[
    Union[
        ActiveNumberSinchEvent,
        NumberOrderSinchEvent,
        NumberSinchEvent,
    ],
    ResolveUnion(discriminator="resource_type", fallback=NumberSinchEvent),
]

NumberSinchEventAdapter: TypeAdapter = TypeAdapter(NumberSinchEventPayload)
