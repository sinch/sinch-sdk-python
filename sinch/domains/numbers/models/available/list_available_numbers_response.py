from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from sinch.domains.numbers.models.numbers import Number


class ListAvailableNumbersResponse(BaseModel):
    available_numbers: Optional[List[Number]] = Field(default=None, alias="availableNumbers")

    model_config = ConfigDict(
        populate_by_name=True
    )
