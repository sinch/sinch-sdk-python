from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.numbers.sinch_events.v1.events.number_sinch_event import (
    NumberSinchEvent,
)


class ActiveNumberSinchEvent(NumberSinchEvent):
    resource_type: Literal["ACTIVE_NUMBER"] = Field(..., alias="resourceType")
    event_type: Optional[
        Union[
            Literal[
                "PROVISIONING_TO_SMS_PLATFORM",
                "DEPROVISIONING_FROM_SMS_PLATFORM",
                "PROVISIONING_TO_CAMPAIGN",
                "DEPROVISIONING_FROM_CAMPAIGN",
                "PROVISIONING_TO_VOICE_PLATFORM",
                "DEPROVISIONING_FROM_VOICE_PLATFORM",
            ],
            StrictStr,
        ]
    ] = Field(default=None, alias="eventType", description="The type of the event.")
    status: Optional[
        Union[
            Literal[
                "SUCCEEDED",
                "FAILED",
            ],
            StrictStr,
        ]
    ] = Field(default=None, description="The status of the event or the state transition it represents.")
    internal_failure_code: Optional[StrictStr] = Field(default=None, alias="internalFailureCode", description="If the status is FAILED, certain processes (eg. number to campaign provisioning) will have an internalFailureCode in the payload. The details of these codes can be found in our dedicated [Provisioning errors](https://developers.sinch.com/docs/numbers/api-reference/error-codes/provisioning-errors) documentation.")
