from typing import Optional
from datetime import datetime
from pydantic import Field, StrictStr, conlist, StrictInt
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class ListBatchesRequest(BaseModelConfigurationRequest):
    page: Optional[StrictInt] = None
    page_size: Optional[StrictInt] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    from_: Optional[conlist(StrictStr)] = Field(default=None, alias="from")
    client_reference: Optional[StrictStr] = None
