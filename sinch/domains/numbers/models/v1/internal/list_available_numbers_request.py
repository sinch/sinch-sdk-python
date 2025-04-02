from typing import Optional
from pydantic import Field, StrictInt, StrictStr
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.types import CapabilityTypeValuesList, NumberSearchPatternTypeValues, NumberType


class ListAvailableNumbersRequest(BaseModelConfigurationRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberType = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="size")
    capabilities: Optional[CapabilityTypeValuesList] = Field(default=None)
    number_search_pattern: Optional[NumberSearchPatternTypeValues] = (
        Field(default=None, alias="numberPattern.searchPattern"))
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")
