from typing import Optional
from pydantic import Field, StrictInt, StrictStr, field_validator, conlist
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.numbers.models.v1.types import (
    CapabilityType,
    OrderByType,
    NumberSearchPatternType,
    NumberType,
)


class ListActiveNumbersRequest(BaseModelConfigurationRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberType = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="pageSize")
    capabilities: Optional[conlist(CapabilityType)] = Field(default=None)
    number_search_pattern: Optional[NumberSearchPatternType] = Field(
        default=None, alias="numberPattern.searchPattern"
    )
    number_pattern: Optional[StrictStr] = Field(
        default=None, alias="numberPattern.pattern"
    )
    page_token: Optional[StrictStr] = Field(default=None, alias="pageToken")
    order_by: Optional[OrderByType] = Field(default=None, alias="orderBy")

    @field_validator("order_by", mode="before")
    @classmethod
    def convert_order_by(cls, value):
        if isinstance(value, str):
            return cls._to_camel_case(value)
        return value
