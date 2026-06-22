from enum import Enum
from typing import Literal, Union

from pydantic import StrictStr


class ResourceTypeEnum(str, Enum):
    ACTIVE_NUMBER = "ACTIVE_NUMBER"
    NUMBER_ORDER = "NUMBER_ORDER"


ResourceType = Union[
    Literal[ResourceTypeEnum.ACTIVE_NUMBER, ResourceTypeEnum.NUMBER_ORDER],
    StrictStr,
]
