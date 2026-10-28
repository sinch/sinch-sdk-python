from typing import Literal, Union

from pydantic import StrictStr

SentimentType = Union[Literal["positive", "negative", "neutral"], StrictStr]
