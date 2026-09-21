from typing import Literal, Union

from pydantic import StrictStr

ConversationMergeStrategyType = Union[Literal["MERGE"], StrictStr]
