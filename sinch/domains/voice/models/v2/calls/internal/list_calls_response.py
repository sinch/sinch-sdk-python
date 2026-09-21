from pydantic import Field, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.shared.pagination_links import (
    PaginationLinks,
)
from sinch.domains.voice.models.v2.shared.pagination_meta import (
    PaginationMeta,
)


class ListCallsResponse(BaseModelConfiguration):
    calls: conlist(Call) = Field(
        default=..., description="Array of call resources"
    )
    links: PaginationLinks = Field(default=...)
    meta: PaginationMeta = Field(default=...)

    @property
    def content(self):
        """Returns the calls as part of the response object for pagination compatibility."""
        return self.calls or []
