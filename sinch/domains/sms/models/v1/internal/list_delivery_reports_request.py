from typing import Optional
from datetime import datetime
from pydantic import conlist, StrictInt, StrictStr
from sinch.domains.sms.models.v1.types import DeliveryReceiptStatusCodeType
from sinch.domains.sms.models.v1.types import DeliveryStatusType
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class ListDeliveryReportsRequest(BaseModelConfigurationRequest):
    page: Optional[StrictInt] = None
    page_size: Optional[StrictInt] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[conlist(DeliveryStatusType)] = None
    code: Optional[conlist(DeliveryReceiptStatusCodeType)] = None
    client_reference: Optional[StrictStr] = None
