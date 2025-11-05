from typing import Optional
from datetime import datetime
from pydantic import Field, StrictBool, StrictStr, conlist, constr, conint
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class BinaryResponse(BaseModelConfigurationResponse):
    id: Optional[StrictStr] = Field(
        default=None, description="Unique identifier for batch."
    )
    to: Optional[conlist(StrictStr, min_length=1, max_length=1000)] = Field(
        default=None,
        description="A list of phone numbers and group IDs that have received the batch. [More info](https://community.sinch.com/t5/Glossary/MSISDN/ta-p/7628).",
    )
    from_: Optional[StrictStr] = Field(
        default=None,
        alias="from",
        description="The sender number provided.  Required if the Automatic Default Originator is not configured.",
    )
    canceled: Optional[StrictBool] = Field(
        default=False,
        description="Indicates whether or not the batch has been canceled.",
    )
    body: Optional[StrictStr] = Field(
        default=None,
        description="The message content provided. Base64 encoded. ",
    )
    udh: Optional[StrictStr] = Field(
        default=None,
        description="The [UDH](https://community.sinch.com/t5/Glossary/UDH-User-Data-Header/ta-p/7776) header of a binary message HEX encoded. Max 140 bytes including the `body`.",
    )
    type: StrictStr = Field(
        default=...,
        description="SMS in [binary](https://community.sinch.com/t5/Glossary/Binary-SMS/ta-p/7470) format.",
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp for when batch was created.   Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    modified_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp for when batch was last updated.   Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    delivery_report: Optional[StrictStr] = Field(
        default=None,
        description="The delivery report callback option selected. Will be either `none`, `summary`, `full`, `per_recipient`, or `per_recipient_final`.",
    )
    send_at: Optional[datetime] = Field(
        default=None,
        description="If set, the date and time the message should be delivered. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    expire_at: Optional[datetime] = Field(
        default=None,
        description="If set, the date and time the message will expire. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601). For example: `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    callback_url: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = Field(
        default=None, description="The callback URL provided in the request."
    )
    client_reference: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = Field(
        default=None,
        description="The string input to identify this batch message. If set, the identifier will be added in the delivery report/callback of this batch.",
    )
    feedback_enabled: Optional[StrictBool] = Field(
        default=False,
        description="If set to true, then [feedback](/docs/sms/api-reference/sms/tag/Batches/#tag/Batches/operation/deliveryFeedback) is expected after successful delivery.",
    )
    from_ton: Optional[conint(strict=True, le=6, ge=0)] = Field(
        default=None, description="The type of number for the sender number."
    )
    from_npi: Optional[conint(strict=True, le=18, ge=0)] = Field(
        default=None,
        description="Number Plan Indicator for the sender number.",
    )
