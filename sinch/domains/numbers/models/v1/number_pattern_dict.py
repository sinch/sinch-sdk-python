from typing import TypedDict
from typing_extensions import NotRequired
from sinch.domains.numbers.models.v1.number_search_pattern_type import NumberSearchPatternTypeValues


class NumberPatternDict(TypedDict):
    pattern: NotRequired[str]
    search_pattern: NotRequired[NumberSearchPatternTypeValues]
