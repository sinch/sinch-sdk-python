from typing import Optional
from datetime import datetime
from pydantic import Field, StrictStr, conlist, conint, constr
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class ListBatchesRequest(BaseModelConfigurationRequest):
    page: Optional[conint(strict=True, ge=0)] = 0
    page_size: Optional[conint(strict=True, le=100, ge=1)] = 30
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    from_: Optional[conlist(StrictStr)] = Field(default=None, alias="from")
    client_reference: Optional[
        constr(strict=True, max_length=2048, min_length=0)
    ] = None
