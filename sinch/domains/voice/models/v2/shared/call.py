from datetime import datetime
from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.shared.call_destination import (
    CallDestination,
)
from sinch.domains.voice.models.v2.shared.call_origin import CallOrigin
from sinch.domains.voice.models.v2.shared.money import Money
from sinch.domains.voice.models.v2.types.call_direction import CallDirection
from sinch.domains.voice.models.v2.types.call_reason import CallReason
from sinch.domains.voice.models.v2.types.call_result import CallResult
from sinch.domains.voice.models.v2.types.call_type import CallType
from sinch.domains.voice.models.v2.types.origination_type import (
    OriginationType,
)


class Call(BaseModelConfiguration):
    call_id: StrictStr = Field(
        default=..., alias="callId", description="The `Id` of the call."
    )
    project_id: StrictStr = Field(
        default=...,
        alias="projectId",
        description="The `Id` of the project associated with the call.",
    )
    service_id: StrictStr = Field(
        default=...,
        alias="serviceId",
        description="The ID of the service used.",
    )
    session_id: StrictStr = Field(
        default=..., alias="sessionId", description="The ID of the session."
    )
    bridge_name: Optional[StrictStr] = Field(
        default=None,
        alias="bridgeName",
        description="The name of the bridge the call belongs to. Omitted for calls not assigned to any bridge.",
    )
    batch_id: Optional[StrictStr] = Field(
        default=None, alias="batchId", description="The ID of the batch."
    )
    from_: Optional[CallOrigin] = Field(default=None, alias="from")
    to: Optional[CallDestination] = Field(default=None)
    start_time: datetime = Field(
        default=...,
        alias="startTime",
        description="Timestamp (RFC 3339) indicating when the call was created and call setup was initiated (start of the call attempt).",
    )
    update_time: Optional[datetime] = Field(
        default=None,
        alias="updateTime",
        description="Timestamp (RFC 3339) indicating when the call was last updated.\n\nOmitted if no updates were performed on this call.",
    )
    call_type: CallType = Field(default=..., alias="callType")
    direction: CallDirection = Field(default=...)
    answer_time: Optional[datetime] = Field(
        default=None,
        alias="answerTime",
        description="Timestamp (RFC 3339) indicating when the call was answered.\n\nOmitted if the call was not answered.",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        alias="endTime",
        description="Timestamp (RFC 3339) indicating when the call ended.\n\nOmitted for ongoing calls.",
    )
    call_duration_seconds: Optional[StrictInt] = Field(
        default=None,
        alias="callDurationSeconds",
        description="Duration of the call in seconds",
    )
    call_result: CallResult = Field(default=..., alias="callResult")
    call_reason: Optional[CallReason] = Field(default=None, alias="callReason")
    origination_type: OriginationType = Field(
        default=..., alias="originationType"
    )
    call_rate: Money = Field(
        default=...,
        alias="callRate",
        description="The rate charged for this call, expressed as a monetary amount per minute in the specified currency.",
    )
    call_resource_url: StrictStr = Field(
        default=...,
        alias="callResourceUrl",
        description="Absolute URI to this call resource. Use this URL to retrieve the call details",
    )
