from typing import Optional
from pydantic import Field, StrictInt, StrictStr
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest
from sinch.domains.numbers.models.numbers import CapabilityType, NumberType, NumberSearchPatternType


class ListAvailableNumbersRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberType = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="size")
    capabilities: Optional[CapabilityType] = Field(default=None)
    number_search_pattern: Optional[NumberSearchPatternType] = (
        Field(default=None, alias="numberPattern.searchPattern"))
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")
