from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, conlist
from sinch.domains.numbers.models.v1.response import AvailableNumber


class ListAvailableNumbersResponse(BaseModel):
    available_numbers: Optional[conlist(AvailableNumber)] = Field(
        default=None, alias="availableNumbers"
    )

    model_config = ConfigDict(populate_by_name=True)

    @property
    def content(self):
        """Returns the available numbers as part of the response object to be used in the pagination."""
        return self.available_numbers or []
