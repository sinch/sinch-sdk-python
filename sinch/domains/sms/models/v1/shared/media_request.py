from typing import Dict, Optional
from datetime import datetime
from pydantic import Field, StrictBool, StrictStr, conlist, constr
from sinch.domains.sms.models.v1.types import (
    DeliveryReportType,
)
from sinch.domains.sms.models.v1.shared import MediaBody
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class MediaRequest(BaseModelConfigurationRequest):
    to: conlist(StrictStr) = Field(
        default=...,
        description="List of Phone numbers and group IDs that will receive the batch. [More info](https://community.sinch.com/t5/Glossary/MSISDN/ta-p/7628)",
    )
    var_from: Optional[StrictStr] = Field(
        default=None,
        alias="from",
        description="Sender number. Must be valid phone number, short code or alphanumeric. Required if Automatic Default Originator not configured.",
    )
    body: MediaBody = Field(...)
    parameters: Optional[
        Dict[str, Dict[str, constr(strict=True, max_length=1600)]]
    ] = Field(
        default=None,
        description="Contains the parameters that will be used for customizing the message for each recipient.   [Click here to learn more about parameterization](/docs/sms/resources/message-info/message-parameterization).",
    )
    type: Optional[StrictStr] = Field(default=None, description="MMS")
    delivery_report: Optional[DeliveryReportType] = None
    send_at: Optional[datetime] = Field(
        default=None,
        description="If set in the future, the message will be delayed until `send_at` occurs. Must be before `expire_at`. If set in the past, messages will be sent immediately. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`. ",
    )
    expire_at: Optional[datetime] = Field(
        default=None,
        description="If set, the system will stop trying to deliver the message at this point. Must be after `send_at`. Default and max is 3 days after `send_at`. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`. ",
    )
    callback_url: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = Field(
        default=None,
        description="Override the default callback URL for this batch. Must be valid URL.",
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
    strict_validation: Optional[StrictBool] = Field(
        default=False,
        description="Whether or not you want the media included in your message to be checked against [Sinch MMS channel best practices](/docs/mms/bestpractices/). If set to true, your message will be rejected if it doesn't conform to the listed recommendations, otherwise no validation will be performed. ",
    )
