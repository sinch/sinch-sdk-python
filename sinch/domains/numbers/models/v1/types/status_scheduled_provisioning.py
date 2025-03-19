from typing import Annotated, Union, Literal
from pydantic import StrictStr, Field

StatusScheduledProvisioning = Annotated[
    Union[Literal["WAITING", "IN_PROGRESS", "FAILED"], StrictStr],
    Field(default=None)
]
