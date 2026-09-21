from typing import Literal, Union
from pydantic import StrictStr


ChannelIntegrationStatusType = Union[
    Literal["PENDING", "ACTIVE", "FAILING"], StrictStr
]
