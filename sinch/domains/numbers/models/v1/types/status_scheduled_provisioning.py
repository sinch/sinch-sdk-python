from typing import Union, Literal
from pydantic import StrictStr


StatusScheduledProvisioning = Union[Literal[
    "WAITING",
    "IN_PROGRESS",
    "FAILED",
    "PROVISIONING_STATUS_UNSPECIFIED"
], StrictStr]
