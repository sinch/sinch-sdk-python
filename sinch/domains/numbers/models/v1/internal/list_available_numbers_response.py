from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from sinch.domains.numbers.models.v1.shared.response import AvailableNumber


class ListAvailableNumbersResponse(BaseModel):
    available_numbers: Optional[List[AvailableNumber]] = Field(default=None, alias="availableNumbers")

    model_config = ConfigDict(
        populate_by_name=True
    )
