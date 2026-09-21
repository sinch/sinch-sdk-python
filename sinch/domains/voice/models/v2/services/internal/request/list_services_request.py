from typing import Optional

from pydantic import Field, StrictBool, StrictInt, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListServicesRequest(BaseModelConfiguration):
    filter: Optional[StrictStr] = Field(
        default=None,
        description="Filter services by name or description. Returns all services where either the name or description contains the specified value (case-insensitive partial match).",
    )
    is_default: Optional[StrictBool] = Field(
        default=None,
        alias="isDefault",
        description="Return only the default service.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        alias="pageSize",
        description="Number of items to be returned on each page.",
    )
    page: Optional[StrictInt] = Field(
        default=None,
        description="Page number (1-based)",
    )
