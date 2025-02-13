from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, StrictStr, StrictInt
from sinch.domains.numbers.models.numbers import ActiveNumber


class ListActiveNumbersResponse(BaseModel):
    active_numbers: Optional[List[ActiveNumber]] = Field(default=None, alias="activeNumbers")
    next_page_token: Optional[StrictStr] = Field(default=None, alias="nextPageToken")
    total_size: Optional[StrictInt] = Field(default=None, alias="totalSize")

    model_config = ConfigDict(
            populate_by_name=True
        )
