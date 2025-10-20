from typing import Optional
from datetime import datetime
from pydantic import Field, StrictInt, StrictStr
from sinch.domains.sms.models.v1.types import (
    DeliveryReceiptStatusCodeType,
    DeliveryStatusType,
    EncodingType,
    RecipientDeliveryReportType,
)
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class RecipientDeliveryReport(BaseModelConfigurationResponse):
    applied_originator: Optional[StrictStr] = Field(
        default=None,
        description="The default originator used for the recipient this delivery report belongs to, if default originator pool configured and no originator set when submitting batch.",
    )
    at: datetime = Field(
        default=...,
        description="A timestamp of when the Delivery Report was created in the Sinch service. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    batch_id: StrictStr = Field(
        default=...,
        description="The ID of the batch this delivery report belongs to",
    )
    client_reference: Optional[StrictStr] = Field(
        default=None,
        description="The client identifier of the batch this delivery report belongs to, if set when submitting batch.",
    )
    code: DeliveryReceiptStatusCodeType = Field(
        default=...,
        description="The detailed [status code](https://developers.sinch.com/docs/sms/api-reference/sms/tag/Delivery-reports/#tag/Delivery-reports/section/Delivery-report-error-codes).",
    )
    encoding: Optional[EncodingType] = Field(
        default=None,
        description="Applied encoding for message. Present only if smart encoding is enabled.",
    )
    number_of_message_parts: Optional[StrictInt] = Field(
        default=None,
        description="The number of parts the message was split into. Present only if `max_number_of_message_parts` parameter was set.",
    )
    operator: Optional[StrictStr] = Field(
        default=None,
        description="The operator that was used for delivering the message to this recipient, if enabled on the account by Sinch.",
    )
    operator_status_at: Optional[datetime] = Field(
        default=None,
        description="A timestamp extracted from the Delivery Receipt from the originating SMSC. Formatted as [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601): `YYYY-MM-DDThh:mm:ss.SSSZ`.",
    )
    recipient: StrictStr = Field(
        default=..., description="Phone number that was queried."
    )
    status: DeliveryStatusType = Field(
        default=..., description="The delivery status."
    )
    type: RecipientDeliveryReportType = Field(
        default=..., description="The recipient delivery report type."
    )
