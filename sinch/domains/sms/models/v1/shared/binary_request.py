from typing import Optional
from datetime import datetime
from pydantic import Field, StrictBool, StrictStr, conlist, constr, conint
from sinch.domains.sms.models.v1.types import (
    DeliveryReportType,
)
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class BinaryRequest(BaseModelConfigurationRequest):
    to: conlist(StrictStr) = Field(
        default=...,
        description="A list of phone numbers and group IDs that will receive the batch. [More info](https://community.sinch.com/t5/Glossary/MSISDN/ta-p/7628).",
    )
    from_: Optional[StrictStr] = Field(
        default=None,
        alias="from",
        description="Sender number. Must be valid phone number, short code or alphanumeric. Required if Automatic Default Originator not configured.",
    )
    body: StrictStr = Field(
        default=...,
        description="The message content Base64 encoded.   Max 140 bytes including `udh`.",
    )
    udh: StrictStr = Field(
        default=...,
        description="The UDH header of a binary message HEX encoded. Max 140 bytes including the `body`.",
    )
    type: Optional[StrictStr] = Field(
        default="mt_binary",
        description="SMS in [binary](https://community.sinch.com/t5/Glossary/Binary-SMS/ta-p/7470) format.",
    )
    delivery_report: Optional[DeliveryReportType] = None
    send_at: Optional[datetime] = Field(
        default=None,
        description="If set in the future the message will be delayed until `send_at` occurs.   Must be before `expire_at`.   If set in the past, messages will be sent immediately.   Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    expire_at: Optional[datetime] = Field(
        default=None,
        description="If set, the system will stop trying to deliver the message at this point. Must be after `send_at`. Default and max is 3 days after `send_at`.   Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    callback_url: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = Field(
        default=None,
        description="Override the *default* callback URL for this batch. Must be a valid URL. Learn how to set a default callback URL [here](https://community.sinch.com/t5/SMS/How-do-I-assign-a-callback-URL-to-an-SMS-service-plan/ta-p/8414).",
    )
    client_reference: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = Field(
        default=None,
        description="The client identifier of a batch message. If set, the identifier will be added in the delivery report/callback of this batch.",
    )
    feedback_enabled: Optional[StrictBool] = Field(
        default=False,
        description="If set to true then [feedback](/docs/sms/api-reference/sms/tag/Batches/#tag/Batches/operation/deliveryFeedback) is expected after successful delivery.",
    )
    from_ton: Optional[conint(strict=True, le=6, ge=0)] = Field(
        default=None,
        description="The type of number for the sender number. Use to override the automatic detection.",
    )
    from_npi: Optional[conint(strict=True, le=18, ge=0)] = Field(
        default=None,
        description="Number Plan Indicator for the sender number. Use to override the automatic detection.",
    )
