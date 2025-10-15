from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.numbers.models.v1.types import NumberSearchPatternType


class NumberPattern(BaseModelConfigurationRequest):
    pattern: Optional[StrictStr]
    search_pattern: Optional[NumberSearchPatternType] = Field(
        alias="searchPattern"
    )
