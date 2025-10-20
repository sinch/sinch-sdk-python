from typing import Optional
from datetime import datetime
from pydantic import conlist, conint, constr
from sinch.domains.sms.models.v1.types import DeliveryReceiptStatusCodeType
from sinch.domains.sms.models.v1.types import DeliveryStatusType
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class ListDeliveryReportsRequest(BaseModelConfigurationRequest):
    page: Optional[conint(strict=True, ge=0)] = 0
    page_size: Optional[conint(strict=True, le=100, ge=1)] = 30
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[conlist(DeliveryStatusType)] = None
    code: Optional[conlist(DeliveryReceiptStatusCodeType)] = None
    client_reference: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = None
