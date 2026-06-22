from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event import (
    NumberSinchEvent,
)


class NumberOrderSinchEvent(NumberSinchEvent):
    resource_type: Literal["NUMBER_ORDER"] = Field(..., alias="resourceType")
    event_type: Optional[
        Union[
            Literal[
                "NUMBER_ORDER_PROCESSING",
            ],
            StrictStr,
        ]
    ] = Field(default=None, alias="eventType", description="The type of the event.")
    status: Optional[
        Union[
            Literal[
                "IN_REVIEW",
                "BLOCKED",
                "COMPLETED",
                "REJECTED",
                "EXPIRED",
            ],
            StrictStr,
        ]
    ] = Field(default=None, description="The status of the event or the state transition it represents.")
