from typing import Optional, List
from pydantic import StrictStr, Field
from sinch.domains.sms.models.v1.types import (
    DeliveryReceiptStatusCodeType,
    DeliveryReportType,
    DeliveryStatusType,
)
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class GetBatchDeliveryReportRequest(BaseModelConfigurationRequest):
    batch_id: StrictStr
    type: Optional[DeliveryReportType] = Field(
        default=None,
        description="The type of delivery report.",
    )
    status: Optional[List[DeliveryStatusType]] = Field(
        default=None,
        description="Comma separated list of delivery_report_statuses to include",
    )
    code: Optional[List[DeliveryReceiptStatusCodeType]] = Field(
        default=None,
        description="Comma separated list of delivery receipt error codes to include",
    )
    client_reference: Optional[StrictStr] = Field(
        default=None,
        description="The client identifier of the batch this delivery report belongs to, if set when submitting batch.",
    )
