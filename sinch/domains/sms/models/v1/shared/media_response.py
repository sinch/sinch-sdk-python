from typing import Dict, Optional
from datetime import datetime
from pydantic import Field, StrictBool, StrictStr, conlist, constr
from sinch.domains.sms.models.v1.types.delivery_report_type import (
    DeliveryReportType,
)
from sinch.domains.sms.models.v1.shared.media_body import MediaBody
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class MediaResponse(BaseModelConfigurationResponse):
    id: Optional[StrictStr] = Field(
        default=None, description="Unique identifier for batch"
    )
    to: Optional[conlist(StrictStr, min_length=1, max_length=1000)] = Field(
        default=None,
        description="List of Phone numbers and group IDs that will receive the batch. [More info](https://community.sinch.com/t5/Glossary/MSISDN/ta-p/7628)",
    )
    from_: Optional[StrictStr] = Field(
        default=None,
        alias="from",
        description="Sender number.    Required if Automatic Default Originator not configured.",
    )
    canceled: Optional[StrictBool] = Field(
        default=False,
        description="Indicates if the batch has been canceled or not.",
    )
    body: Optional[MediaBody] = None
    parameters: Optional[
        Dict[str, Dict[str, constr(strict=True, max_length=1600)]]
    ] = Field(
        default=None,
        description="Contains the parameters that will be used for customizing the message for each recipient.   [Click here to learn more about parameterization](/docs/sms/resources/message-info/message-parameterization).",
    )
    type: StrictStr = Field(default=..., description="Media message")
    created_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp for when batch was created.     YYYY-MM-DDThh:mm:ss.SSSZ format",
    )
    modified_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp for when batch was last updated.     YYYY-MM-DDThh:mm:ss.SSSZ format",
    )
    delivery_report: Optional[DeliveryReportType] = None
    send_at: Optional[datetime] = Field(
        default=None,
        description="If set in the future the message will be delayed until send_at occurs.     Must be before `expire_at`.     If set in the past messages will be sent immediately.     YYYY-MM-DDThh:mm:ss.SSSZ format",
    )
    expire_at: Optional[datetime] = Field(
        default=None,
        description="If set the system will stop trying to deliver the message at this point.     Must be after `send_at`. Default and max is 3 days after send_at.     YYYY-MM-DDThh:mm:ss.SSSZ format",
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
        description="If set to true then [feedback](/docs/sms/api-reference/sms/tag/Batches/#tag/Batches/operation/deliveryFeedback) is expected after successful delivery.",
    )
    strict_validation: Optional[StrictBool] = Field(
        default=None,
        description="Whether or not you want the media included in your message to be checked against [Sinch MMS channel best practices](/docs/mms/bestpractices/). If set to true, your message will be rejected if it doesn't conform to the listed recommendations, otherwise no validation will be performed. ",
    )
