from pydantic import Field, StrictStr
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class GetDeliveryReportByPhoneNumberRequest(BaseModelConfigurationRequest):
    batch_id: StrictStr = Field(
        default=...,
        description="The batch ID you received from sending a message.",
    )
    recipient_msisdn: StrictStr = Field(
        default=..., description="The recipient phone number in E.164 format."
    )
