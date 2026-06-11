from typing import Optional

from pydantic import Field, StrictInt

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class ListGroupsRequest(BaseModelConfigurationRequest):
    page: Optional[StrictInt] = Field(
        default=None, description="The requested page."
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="The number of entries returned in this request.",
    )
