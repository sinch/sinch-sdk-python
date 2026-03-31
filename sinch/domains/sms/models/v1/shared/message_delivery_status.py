from typing import Optional
from pydantic import Field, StrictInt, StrictStr, conlist
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.sms.models.v1.types import (
    DeliveryReceiptStatusCodeType,
    DeliveryStatusType,
)


class MessageDeliveryStatus(BaseModelConfigurationResponse):
    code: DeliveryReceiptStatusCodeType = Field(
        default=...,
        description="The detailed [status code](/docs/sms/api-reference/sms/tag/Delivery-reports/#tag/Delivery-reports/section/Delivery-report-error-codes).",
    )
    count: StrictInt = Field(
        default=...,
        description="The number of messages that currently has this code.",
    )
    recipients: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="Only for `full` report. A list of the phone number recipients which messages has this status code.",
    )
    status: DeliveryStatusType = Field(..., description="The delivery status.")
