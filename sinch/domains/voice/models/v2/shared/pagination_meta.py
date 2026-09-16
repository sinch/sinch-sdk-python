from pydantic import Field, StrictInt

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class PaginationMeta(BaseModelConfiguration):
    total_count: StrictInt = Field(
        default=...,
        alias="totalCount",
        description="Total number of items across all pages.",
    )
    page_count: StrictInt = Field(
        default=...,
        alias="pageCount",
        description="Total number of pages.",
    )
