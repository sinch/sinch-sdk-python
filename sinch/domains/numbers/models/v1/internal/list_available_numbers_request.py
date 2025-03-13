from typing import Optional
from pydantic import Field, StrictInt, StrictStr
from sinch.domains.numbers.models.v1.internal import BaseModelConfigRequest
from sinch.domains.numbers.models.v1.shared_params import (
    CapabilityTypeValuesList, NumberType, NumberSearchPatternTypeValues
)


class ListAvailableNumbersRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberType = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="size")
    capabilities: Optional[CapabilityTypeValuesList] = Field(default=None)
    number_search_pattern: Optional[NumberSearchPatternTypeValues] = (
        Field(default=None, alias="numberPattern.searchPattern"))
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")
