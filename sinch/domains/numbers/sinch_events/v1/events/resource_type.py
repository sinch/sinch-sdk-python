from typing import Literal, Union

from pydantic import StrictStr

ResourceType = Union[
    Literal["ACTIVE_NUMBER", "NUMBER_ORDER"],
    StrictStr,
]
