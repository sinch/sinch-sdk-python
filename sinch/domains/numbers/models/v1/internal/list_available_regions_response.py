from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, conlist
from sinch.domains.numbers.models.v1.response import AvailableRegion


class ListAvailableRegionsResponse(BaseModel):
    available_regions: Optional[conlist(AvailableRegion)] = Field(
        default=None, alias="availableRegions"
    )

    model_config = ConfigDict(populate_by_name=True)

    @property
    def content(self):
        """Returns the available regions as part of the response object to be used in the pagination."""
        return self.available_regions or []
