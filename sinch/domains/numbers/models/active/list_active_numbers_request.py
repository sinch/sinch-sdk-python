from typing import Optional
from pydantic import Field, StrictInt, StrictStr, field_validator
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest
from sinch.domains.numbers.models.numbers import (CapabilityTypeValuesList, NumberTypeValues,
                                                  NumberSearchPatternTypeValues, OrderByValues)


class ListActiveNumbersRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberTypeValues = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="pageSize")
    capabilities: Optional[CapabilityTypeValuesList] = Field(default=None)
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
