from pydantic import Field, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.services.response.service_short_response import (
    ServiceShortResponse,
)
from sinch.domains.voice.models.v2.shared.pagination_links import (
    PaginationLinks,
)
from sinch.domains.voice.models.v2.shared.pagination_meta import (
    PaginationMeta,
)


class ListServicesResponse(BaseModelConfiguration):
    services: conlist(ServiceShortResponse) = Field(
        default=..., description="Array of service resources"
    )
    links: PaginationLinks = Field(default=...)
    meta: PaginationMeta = Field(default=...)

    @property
    def content(self):
        """Returns the services as part of the response object for pagination compatibility."""
        return self.services or []
