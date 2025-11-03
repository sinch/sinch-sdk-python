from typing import Optional
from pydantic import Field, StrictInt, conlist
from sinch.domains.sms.models.v1.types import BatchResponse
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class ListBatchesResponse(BaseModelConfigurationResponse):
    count: Optional[StrictInt] = Field(
        default=None,
        description="The total number of entries matching the given filters.",
    )
    page: Optional[StrictInt] = Field(
        default=None, description="The requested page."
    )
    batches: Optional[conlist(BatchResponse)] = Field(
        default=None,
        description="The page of batches matching the given filters.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="The number of entries returned in this request.",
    )

    @property
    def content(self):
        """Returns the content of batches list."""
        return self.batches or []
