from typing import Optional
from pydantic import Field, StrictInt, StrictStr, field_validator
from sinch.domains.numbers.models.v1.capability_type import CapabilityType
from sinch.domains.numbers.models.v1.internal import BaseModelConfigRequest
from sinch.domains.numbers.models.v1.number_search_pattern_type import NumberSearchPatternTypeValues
from sinch.domains.numbers.models.v1.number_type import NumberTypeValues
from sinch.domains.numbers.models.v1.order_by_values import OrderByValues


class ListActiveNumbersRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberTypeValues = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="pageSize")
    capabilities: Optional[CapabilityType] = Field(default=None)
    number_search_pattern: Optional[NumberSearchPatternTypeValues] = (
        Field(default=None, alias="numberPattern.searchPattern")
    )
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")
    page_token: Optional[StrictStr] = Field(default=None, alias="pageToken")
    order_by: Optional[OrderByValues] = Field(default=None, alias="orderBy")

    @field_validator("order_by", mode="before")
    @classmethod
    def convert_order_by(cls, value):
        if isinstance(value, str):
            return cls._to_camel_case(value)
        return value
