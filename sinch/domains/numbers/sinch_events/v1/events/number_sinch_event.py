from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import Field, StrictStr

from sinch.domains.numbers.sinch_events.v1.internal import SinchEvent


class NumberSinchEvent(SinchEvent):
    event_id: Optional[StrictStr] = Field(
        default=None, alias="eventId", description="The ID of the event."
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="The date and time when the callback was created and added to the callbacks queue.",
    )
    project_id: Optional[StrictStr] = Field(
        default=None,
        alias="projectId",
        description="The ID of the project to which the event belongs.",
    )
    resource_id: Optional[StrictStr] = Field(
        default=None,
        alias="resourceId",
        description="The unique identifier of the resource, depending on the resource type. For example, a phone number, a hosting order ID, or a brand ID.",
    )
    resource_type: Optional[Union[Literal["ACTIVE_NUMBER"], StrictStr]] = (
        Field(default=None, alias="resourceType")
    )
    event_type: Optional[
        Union[
            Literal[
                "PROVISIONING_TO_SMS_PLATFORM",
                "DEPROVISIONING_FROM_SMS_PLATFORM",
                "PROVISIONING_TO_CAMPAIGN",
                "DEPROVISIONING_FROM_CAMPAIGN",
                "PROVISIONING_TO_VOICE_PLATFORM",
                "DEPROVISIONING_FROM_VOICE_PLATFORM",
                "NUMBER_ORDER_PROCESSING",
            ],
            StrictStr,
        ]
    ] = Field(
        default=None, alias="eventType", description="The type of the event."
    )
    status: Optional[
        Union[
            Literal[
                "SUCCEEDED",
                "FAILED",
                "IN_REVIEW",
                "BLOCKED",
                "COMPLETED",
                "REJECTED",
                "EXPIRED",
            ],
            StrictStr,
        ]
    ] = Field(
        default=None,
        description="The status of the event or the state transition it represents.",
    )
    failure_code: Optional[
        Union[
            Literal[
                "CAMPAIGN_EXPIRED",
                "CAMPAIGN_MNO_REJECTED",
                "CAMPAIGN_MNO_REVIEW",
                "CAMPAIGN_MNO_SUSPENDED",
                "CAMPAIGN_NOT_AVAILABLE",
                "CAMPAIGN_PENDING_ACCEPTANCE",
                "CAMPAIGN_PROVISIONING_FAILED",
                "EXCEEDED_10DLC_LIMIT",
                "INSUFFICIENT_BALANCE",
                "INVALID_NNID",
                "MNO_SHARING_ERROR",
                "MOCK_CAMPAIGN_NOT_ALLOWED",
                "NUMBER_PROVISIONING_FAILED",
                "PARTNER_SERVICE_UNAVAILABLE",
                "TFN_NOT_ALLOWED",
            ],
            StrictStr,
        ]
    ] = Field(
        default=None,
        alias="failureCode",
        description="If the status is FAILED, a failure code will be provided. For numbers provisioning to SMS platform, there won't be any extra `failureCode`, as the result is binary. For campaign provisioning-related failures, refer to the list for the possible values.",
    )
    internal_failure_code: Optional[StrictStr] = Field(
        default=None,
        alias="internalFailureCode",
        description="If the status is FAILED, certain processes (eg. number to campaign provisioning) will have an internalFailureCode in the payload. The details of these codes can be found in our dedicated [Provisioning errors](https://developers.sinch.com/docs/numbers/api-reference/error-codes/provisioning-errors) documentation.",
    )