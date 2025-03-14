from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, StrictStr, StrictInt
from sinch.domains.numbers.models.v1.shared.active_number import ActiveNumber


class ListActiveNumbersResponse(BaseModel):
    active_numbers: Optional[List[ActiveNumber]] = Field(default=None, alias="activeNumbers")
    next_page_token: Optional[StrictStr] = Field(default=None, alias="nextPageToken")
    total_size: Optional[StrictInt] = Field(default=None, alias="totalSize")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )

    @property
    def content(self):
        """Returns the active numbers as part of the response object to be used in the pagination."""
        return self.active_numbers or []
