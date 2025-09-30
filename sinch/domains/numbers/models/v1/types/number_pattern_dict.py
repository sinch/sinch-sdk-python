from typing import TypedDict
from typing_extensions import NotRequired
from sinch.domains.numbers.models.v1.types import NumberSearchPatternType


class NumberPatternDict(TypedDict):
    pattern: NotRequired[str]
    search_pattern: NotRequired[NumberSearchPatternType]
