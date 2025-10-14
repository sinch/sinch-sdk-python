from typing import Optional
from pydantic import Field, StrictInt, StrictStr, conlist
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.types import CapabilityType, NumberSearchPatternType, NumberType


class ListAvailableNumbersRequest(BaseModelConfigurationRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberType = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="size")
    capabilities: Optional[conlist(CapabilityType)] = Field(default=None)
    number_search_pattern: Optional[NumberSearchPatternType] = Field(default=None, alias="numberPattern.searchPattern")
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")
