from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class PaginationLinks(BaseModelConfiguration):
    first: StrictStr = Field(
        default=..., description="Absolute URI of the first page."
    )
    last: StrictStr = Field(
        default=..., description="Absolute URI of the last page."
    )
    next: Optional[StrictStr] = Field(
        default=None,
        description="Absolute URI of the next page (omitted if this is the last page).",
    )
    prev: Optional[StrictStr] = Field(
        default=None,
        description="Absolute URI of the previous page (omitted if this is the first page).",
    )
    self_: StrictStr = Field(
        default=...,
        alias="self",
        description="Absolute URI of the current page.",
    )
