from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.internal import BaseModelConfigRequest
from sinch.domains.numbers.models.v1.number_search_pattern_type import NumberSearchPatternType


class NumberPattern(BaseModelConfigRequest):
    pattern: Optional[StrictStr]
    search_pattern: Optional[NumberSearchPatternType] = Field(alias="searchPattern")
