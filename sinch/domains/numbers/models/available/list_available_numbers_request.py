from typing import Optional
from pydantic import Field, StrictInt, StrictStr
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest
from sinch.domains.numbers.models.numbers import (
    CapabilityTypeValuesList, NumberTypeValues, NumberSearchPatternTypeValues
)


class ListAvailableNumbersRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberTypeValues = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="size")
    capabilities: Optional[CapabilityTypeValuesList] = Field(default=None)
    number_search_pattern: Optional[NumberSearchPatternTypeValues] = (
        Field(default=None, alias="numberPattern.searchPattern"))
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")
