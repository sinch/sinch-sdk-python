from typing import Dict, Optional
from datetime import datetime
from pydantic import Field, StrictBool, StrictStr, conlist, constr, conint
from sinch.domains.sms.models.v1.types import DeliveryReportType
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class UpdateTextRequest(BaseModelConfigurationRequest):
    from_: Optional[StrictStr] = Field(
        default=None,
        alias="from",
        description="Sender number. Must be valid phone number, short code or alphanumeric.",
    )
    type: Optional[StrictStr] = Field(
        default="mt_text", description="Regular SMS"
    )
    to_add: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of phone numbers and group IDs to add to the batch.",
    )
    to_remove: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of phone numbers and group IDs to remove from the batch.",
    )
    delivery_report: Optional[DeliveryReportType] = None
    send_at: Optional[datetime] = Field(
        default=None,
        description="If set, in the future the message will be delayed until `send_at` occurs. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`.  Constraints: Must be before expire_at. If set in the past, messages will be sent immediately. ",
    )
    expire_at: Optional[datetime] = Field(
        default=None,
        description="If set, the system will stop trying to deliver the message at this point.  Constraints: Must be after `send_at`  Default: 3 days after `send_at` ",
    )
    callback_url: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = Field(
        default=None,
        description="Override the default callback URL for this batch.  Constraints: Must be valid URL. ",
    )
    client_reference: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = Field(
        default=None,
        description="The client identifier of a batch message. If set, the identifier will be added in the delivery report/callback of this batch",
    )
    feedback_enabled: Optional[StrictBool] = Field(
        default=False,
        description="If set to `true`, then [feedback](/docs/sms/api-reference/sms/tag/Batches/#tag/Batches/operation/deliveryFeedback) is expected after successful delivery.",
    )
    parameters: Optional[
        Dict[str, Dict[str, constr(strict=True, max_length=1600)]]
    ] = Field(
        default=None,
        description="Contains the parameters that will be used for customizing the message for each recipient.   [Click here to learn more about parameterization](/docs/sms/resources/message-info/message-parameterization).",
    )
    body: Optional[constr(strict=True, max_length=2000, min_length=0)] = Field(
        default=None, description="The message content"
    )
    from_ton: Optional[conint(strict=True, le=6, ge=0)] = Field(
        default=None,
        description="The type of number for the sender number. Use to override the automatic detection.",
    )
    from_npi: Optional[conint(strict=True, le=18, ge=0)] = Field(
        default=None,
        description="Number Plan Indicator for the sender number. Use to override the automatic detection.",
    )
    max_number_of_message_parts: Optional[conint(strict=True, ge=1)] = Field(
        default=None,
        description="Message will be dispatched only if it is not split to more parts than Max Number of Message Parts",
    )
    truncate_concat: Optional[StrictBool] = Field(
        default=None,
        description="If set to true the message will be shortened when exceeding one part.",
    )
    flash_message: Optional[StrictBool] = Field(
        default=False,
        description="Shows message on screen without user interaction while not saving the message to the inbox.",
    )
