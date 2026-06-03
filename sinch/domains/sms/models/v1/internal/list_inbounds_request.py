from typing import Optional
from datetime import datetime
from pydantic import StrictInt, StrictStr, conlist
from sinch.domains.sms.models.v1.internal.base import BaseModelConfigurationRequest


class ListInboundsRequest(BaseModelConfigurationRequest):
    page: Optional[StrictInt] = None
    page_size: Optional[StrictInt] = None
    to: Optional[conlist(StrictStr)] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    client_reference: Optional[StrictStr] = None
