from typing import Annotated, Union, Literal
from pydantic import StrictStr, Field

StatusScheduledProvisioning = Annotated[
    Union[Literal["WAITING", "IN_PROGRESS", "FAILED", "PROVISIONING_STATUS_UNSPECIFIED"], StrictStr],
    Field(default=None)
]
